"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2020 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from .BaubleGame import *
from .Utils import CallbackTimer
from World.WorldEntities import Ship
from World.WorldMath import intpos, friendly_type, PlayerStat, aligninstances, getPositionAwayFromOtherObjects
from GUI.GraphicsCache import Cache
from GUI.Helpers import debugfont
import logging
import pygame
from operator import attrgetter

class HungryHungryBaublesGame(BaseBaubleGame):
    
    def __init__(self, cfgobj):
        self.__points_gold = cfgobj.getint("HungryHungryBaubles", "bauble_extra_value")
        self.__points_extra = cfgobj.getint("HungryHungryBaubles", "bauble_points_extra")
        self.__assign_specific_bauble = cfgobj.getboolean("HungryHungryBaubles", "assign_specific_bauble")

        self.__baubles = {}

        super(HungryHungryBaublesGame, self).__init__(cfgobj)

    def player_added(self, player, reason):
        if reason == BasicGame._ADD_REASON_START_ and self.__assign_specific_bauble:
            self.__addBauble(player) # Add Golden Bauble

        super(HungryHungryBaublesGame, self).player_added(player, reason)

    def __addBauble(self, player, force=False):
        logging.info("Add Bauble (%s) for Player %d", repr(force), player.netid)
        # add player bauble
        b = Bauble(getPositionAwayFromOtherObjects(self.world, self.cfg.getint("Bauble", "buffer_object"), self.cfg.getint("Bauble", "buffer_edge")), self.__points_gold)

        self.__baubles[player.netid] = b

        self.world.append(b)
        logging.info("Done Adding Bauble")

    def world_physics_pre_collision(self, obj1, obj2):
        ship, bauble = aligninstances(obj1, obj2, Ship, Bauble)

        if ship != None:
            return [ False, [self.collectBaubles, ship, bauble] ]

        return super(HungryHungryBaublesGame, self).world_physics_pre_collision(obj1, obj2)

    def collectBaubles(self, space, ship, bauble):
        logging.info("Collected Baubles Ship #%d", ship.id)
        # collect own Bauble?
        if self.__assign_specific_bauble and bauble == self.__baubles[ship.player.netid]:
            logging.info("Collected Own Bauble #%d", ship.id)
            ship.player.update_score(self.__points_extra)
            ship.player.sound = "COLLECT"
            # add new bauble
            self.__addBauble(ship.player, True)
        elif self.__assign_specific_bauble and bauble in list(self.__baubles.values()):
            logging.info("Collected Gold Bauble #%d", ship.id)
            # someone else's bauble
            for key, value in self.__baubles.items():
                if key in self._players and value == bauble:
                    self.__addBauble(self._players[key], True)
                elif value == bauble:
                    # Gold Bauble no longer owned, add back a regular one
                    Bauble.spawn(self.world, self.cfg)
                #eif
            ship.player.sound = "BAUBLE"
        else:
            logging.info("Collected Regular Bauble #%d", ship.id)
            ship.player.sound = "BAUBLE"
            Bauble.spawn(self.world, self.cfg)
        #eif
        ship.player.update_score(bauble.value)
        bauble.destroyed = True

        logging.info("Done Collecting Baubles #%d", ship.id)

    def game_get_extra_environment(self, player):
        env = super(HungryHungryBaublesGame, self).game_get_extra_environment(player)
        if self.__assign_specific_bauble:
            env["POSITION"] = self.__baubles[player.netid].body.position.int_tuple

        return env

    def gui_draw_game_world_info(self, surface, flags, trackplayer):
        if self.__assign_specific_bauble:
            for player in self.game_get_current_player_list():
                obj = player.object
                if obj != None and player.netid in self.__baubles:
                    # draw line between player and Bauble
                    pygame.draw.line(surface, player.color, obj.body.position.int_tuple, self.__baubles[player.netid].body.position.int_tuple)
