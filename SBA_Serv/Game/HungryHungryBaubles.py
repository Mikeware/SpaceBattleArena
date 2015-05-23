"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2015 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from Game import BasicGame, RoundTimer
from World.WorldGenerator import ConfiguredWorld, getPositionAwayFromOtherObjects
from World.Entities import PhysicalRound, Entity
from World.WorldEntities import Ship
from GUI.ObjWrappers.GUIEntity import GUIEntity
from World.WorldMath import intpos, friendly_type, PlayerStat
from GUI.GraphicsCache import Cache
from GUI.Helpers import debugfont
import logging
import pygame
from operator import attrgetter

class HungryHungryBaublesGame(BasicGame):
    
    def __init__(self, cfgobj):
        self.__points_blue = cfgobj.getint("HungryHungryBaubles", "bauble_points_blue")
        self.__points_gold = cfgobj.getint("HungryHungryBaubles", "bauble_points_gold")
        self.__points_extra = cfgobj.getint("HungryHungryBaubles", "bauble_points_extra")

        self.__baubles = {}

        super(HungryHungryBaublesGame, self).__init__(cfgobj)

    def world_create(self, pys=True):
        w = ConfiguredWorld(self, self.cfg, pys)
        
        # Add some initial small Baubles
        self.__addBaubles(w, self.cfg.getint("HungryHungryBaubles", "bauble_initial"))

        return w

    def game_get_info(self):
        return {"GAMENAME": "HungryHungryBaubles"}

    def player_added(self, player, reason):
        if reason == BasicGame._ADD_REASON_START_:
            self.__addBauble(player)
            self.__addBaubles(self.world, self.cfg.getint("HungryHungryBaubles", "bauble_per_player"))

        super(HungryHungryBaublesGame, self).player_added(player, reason)

    def __addBauble(self, player, force=False):
        logging.info("Add Bauble (%s) for Player %d", repr(force), player.netid)
        # add player bauble
        b = Bauble(getPositionAwayFromOtherObjects(self.world, 80, 30, force), self.__points_gold)

        self.__baubles[player.netid] = b

        self.world.append(b)
        logging.info("Done Adding Bauble")

    def __addBaubles(self, w, num, force=False):
        logging.info("Adding %d Baubles (%s)", num, repr(force))
        for i in xrange(num):
            w.append(Bauble(getPositionAwayFromOtherObjects(w, 100, 30, force), self.__points_blue))
        logging.info("Done Adding Baubles")

    def world_physics_pre_collision(self, obj1, obj2):
        if isinstance(obj1, Ship) and isinstance(obj2, Bauble):
            return [ False, [self.collectBaubles, obj1, obj2] ]
        elif isinstance(obj2, Ship) and isinstance(obj1, Bauble):
            return [ False, [self.collectBaubles, obj2, obj1] ]

        return super(HungryHungryBaublesGame, self).world_physics_pre_collision(obj1, obj2)

    def collectBaubles(self, ship, bauble):
        logging.info("Collected Baubles Ship #%d", ship.id)
        # collect own Bauble?
        if bauble == self.__baubles[ship.player.netid]:
            logging.info("Collected Own Bauble #%d", ship.id)
            self.player_update_score(ship.player, self.__points_extra)

            # add new bauble
            self.__addBauble(ship.player, True)
        elif bauble in self.__baubles.values():
            logging.info("Collected Gold Bauble #%d", ship.id)
            # someone else's bauble
            for key, value in self.__baubles.iteritems():
                if self._players.has_key(key) and value == bauble:
                    self.__addBauble(self._players[key], True)
                elif value == bauble:
                    # Gold Bauble no longer owned, add back a regular one
                    self.__addBaubles(self.world, 1, True)
                #eif
        else:
            logging.info("Collected Regular Bauble #%d", ship.id)
            self.__addBaubles(self.world, 1, True)
        #eif
        self.player_update_score(ship.player, bauble.value)
        bauble.destroyed = True
        self.world.remove(bauble)

        logging.info("Done Collecting Baubles #%d", ship.id)

    def game_get_extra_environment(self, player):
        env = super(HungryHungryBaublesGame, self).game_get_extra_environment(player)
        env["POSITION"] = intpos(self.__baubles[player.netid].body.position)

        return env

    def round_over(self):
        self.__btimer.cancel() # prevent more baubles from being spawned!

        super(HungryHungryBaublesGame, self).round_over()

    def gui_draw_game_world_info(self, surface, flags, trackplayer):
        for player in self.game_get_current_player_list():
            if player.object != None and self.__baubles.has_key(player.netid):
                # draw line between player and Bauble
                pygame.draw.line(surface, player.color, intpos(player.object.body.position), intpos(self.__baubles[player.netid].body.position))

    def round_start(self):
        super(HungryHungryBaublesGame, self).round_start()

        # start Bauble Spawn Timer
        self.newBaubleTimer()    
        
    def newBaubleTimer(self):
        self.__btimer = RoundTimer(self.cfg.getint("HungryHungryBaubles", "bauble_timer"), self.spawnBauble)
        self.__btimer.start()

    def spawnBauble(self):
        self.__addBaubles(self.world, self.cfg.getint("HungryHungryBaubles", "bauble_timer_spawns"))
        
        self.newBaubleTimer()


class BaubleWrapper(GUIEntity):
    def __init__(self, obj, world):
        super(BaubleWrapper, self).__init__(obj, world)
        self.surface = Cache().getImage("Games/Bauble" + str(obj.value))

    def draw(self, surface, flags):
        # Check if Thrusting or Braking
        surface.blit(self.surface, intpos((self._worldobj.body.position[0] - 8, self._worldobj.body.position[1] - 8)))

        super(BaubleWrapper, self).draw(surface, flags)

class Bauble(PhysicalRound):
    WRAPPERCLASS = BaubleWrapper
    """
    Baubles are small prizes worth different amounts of points
    """
    def __init__(self, pos, value=1):
        super(Bauble, self).__init__(8, 2000, pos)
        self.shape.elasticity = 0.8
        self.health = PlayerStat(0)

        self.shape.group = 1

        self.value = value

    def collide_start(self, otherobj):
        return False

    def getExtraInfo(self, objData):
        objData["VALUE"] = self.value
