"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2016 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from BaubleGame import *
from Utils import CallbackTimer
from World.Entities import Entity, PhysicalRound
from World.WorldEntities import Ship
from GUI.ObjWrappers.GUIEntity import GUIEntity, wrapcircle
from World.WorldMath import intpos, friendly_type, PlayerStat, aligninstances, getPositionAwayFromOtherObjects
from GUI.GraphicsCache import Cache
from GUI.Helpers import debugfont
from ThreadStuff.ThreadSafe import ThreadSafeDict
import logging
import pygame
import random
import thread
import math
from operator import attrgetter

class TheHungerBaublesGame(BaseBaubleGame):
    def __init__(self, cfgobj):

        self._respawn = cfgobj.getboolean("TheHungerBaubles", "respawn_bauble_on_collect")
        self.__maxcarry = cfgobj.getint("TheHungerBaubles", "ship_cargo_size")
        self.__cornucopia_position = (0, 0)
        self.__cornucopia_radius = cfgobj.getint("TheHungerBaubles", "cornucopia_radius")
        self.__spawned_num = 0

        super(TheHungerBaublesGame, self).__init__(cfgobj)

    def game_get_info(self):
        return {"GAMENAME": "TheHungerBaubles"}

    def player_added(self, player, reason):
        super(TheHungerBaublesGame, self).player_added(player, reason)
        player.carrying = []
        player.collected = 0

    def player_get_start_position(self):
        if self.cfg.getboolean("Tournament", "tournament"):
            div = 360 / (len(self._players) / self.cfg.getint("Tournament", "groups"))
        else:
            div = 200

        ang = div * self.__spawned_num
        self.__spawned_num += 1
        dist = self.__cornucopia_radius + 64
        return (min(max(32, self.__cornucopia_position[0] + math.cos(math.radians(ang)) * dist), self.world.width - 32), 
                min(max(32, self.__cornucopia_position[1] + math.sin(math.radians(ang)) * dist), self.world.height - 32))

    def world_add_remove_object(self, wobj, added):
        # Check if this is a high-value bauble to add to our list of ones to pass to the client

        # TODO: If an Asteroid or Dragon is destroyed, deposit bauble

        return super(TheHungerBaublesGame, self).world_add_remove_object(wobj, added)

    def world_physics_pre_collision(self, obj1, obj2):
        ship, other = aligninstances(obj1, obj2, Ship, Entity)

        if ship != None:
            #if isinstance(other, Outpost):
            #    logging.info("Ship #%d hit their base", ship.id)
            #    return [ False, [self.depositBaubles, ship, other] ]
            if isinstance(other, Bauble):
                return [ False, [self.collectBaubles, ship, other] ]
        
        return super(TheHungerBaublesGame, self).world_physics_pre_collision(obj1, obj2)

    def get_player_cargo_value(self, player):
        return sum(b.value for b in player.carrying)

    def get_player_cargo_weight(self, player):
        return sum(b.weight for b in player.carrying)

    def collectBaubles(self, ship, bauble):
        logging.info("Collected Baubles Ship #%d", ship.id)
        if self.get_player_cargo_weight(ship.player) + bauble.weight <= self.__maxcarry:
            ship.player.carrying.append(bauble)
            ship.player.collected += 1
            ship.player.update_score(bauble.value)
            ship.player.sound = "BAUBLE"

            bauble.destroyed = True

            if self._respawn:
                Bauble.spawn(self.world, self.cfg)
        else:
            logging.info("Player #%d Cargo Full", ship.id)
        #eif
        logging.info("Done Collecting Baubles #%d", ship.id)

    def player_died(self, player, gone):
        # if ship destroyed, put baubles stored back
        for b in player.carrying:
            b.body.position = (player.object.body.position[0] + random.randint(-36, 36), player.object.body.position[1] + random.randint(-36, 36))
            b.destroyed = False # reset so that it won't get cleaned up

            self.world.append(b)

        return super(TheHungerBaublesGame, self).player_died(player, gone)

    def game_get_extra_environment(self, player):
        v = 0
        w = 0
        for b in player.carrying:
            v += b.value
            w += b.weight
        baubles = []
        for b in player.carrying:
            baubles.append({ "MASS": b.weight, "VALUE": b.value, "ID": b.id})

        env = super(TheHungerBaublesGame, self).game_get_extra_environment(player)
        env.update({"POSITION": self.__cornucopia_position, "BAUBLES": baubles})

        return env
    
    def game_get_extra_radar_info(self, obj, objdata, player):
        """
        Called by the World when the obj is being radared
        """
        super(TheHungerBaublesGame, self).game_get_extra_radar_info(obj, objdata, player)
        if hasattr(obj, "player"):
            objdata["NUMSTORED"] = len(obj.player.carrying)
            objdata["VALUE"] = self.get_player_cargo_value(obj.player)

    def player_get_stat_string(self, player):
        return str(int(player.bestscore)) + " - " + str(int(player.score)) + " in " + str(player.collected) + " : " + player.name + " w. " + str(self.get_player_cargo_weight(player))

    def gui_draw_game_world_info(self, surface, flags, trackplayer):
        for player in self.game_get_current_player_list():
            obj = player.object
            if obj != None:
                # draw number of objects carried
                text = debugfont().render(repr(len(player.carrying)), False, player.color)
                surface.blit(text, (obj.body.position[0]-30, obj.body.position[1]-4))
                text = debugfont().render(repr(self.get_player_cargo_weight(player)), False, player.color)
                surface.blit(text, (obj.body.position[0]+30, obj.body.position[1]-4))
                # draw line between player and HomeBase
                #if flags["DEBUG"] and self.__bases.has_key(player.netid):
                #pygame.draw.line(surface, player.color, intpos(obj.body.position), intpos(self.__bases[player.netid].body.position))
        wrapcircle(surface, (255, 255, 0), self.__cornucopia_position, self.__cornucopia_radius, self.world.size, 3)

        # draw number of baubles carried by player

    def round_start(self):
        logging.info("Game Start")

        self.__spawned_num = 0

        super(TheHungerBaublesGame, self).round_start()

    def world_create(self):
        super(TheHungerBaublesGame, self).world_create()

        self.__cornucopia_position = getPositionAwayFromOtherObjects(self.world, self.cfg.getint("TheHungerBaubles", "cornucopia_buffer_object"), self.cfg.getint("TheHungerBaubles", "cornucopia_buffer_edge"))

        #TODO: Remove anything left inside cornucopia?
