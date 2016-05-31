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
from World.WorldEntities import Ship, Weapon, Torpedo, SpaceMine, Dragon, Asteroid
from GUI.ObjWrappers.GUIEntity import GUIEntity, wrapcircle
from World.WorldMath import intpos, friendly_type, PlayerStat, aligninstances, getPositionAwayFromOtherObjects
from GUI.GraphicsCache import Cache
from GUI.Helpers import debugfont
from ThreadStuff.ThreadSafe import ThreadSafeDict
from World.WorldCommands import FireTorpedoCommand, DeploySpaceMineCommand
from World.Messaging import OneTimeCommand
import logging
import pygame
import random
import thread
import math
from operator import attrgetter

GAME_CMD_COLLECT = "COLCT"
GAME_CMD_EJECT = "EJECT"

class TheHungerBaublesGame(BaseBaubleGame):
    def __init__(self, cfgobj):

        self._respawn = cfgobj.getboolean("TheHungerBaubles", "respawn_bauble_on_collect")
        self.__maxcarry = cfgobj.getint("TheHungerBaubles", "ship_cargo_size")
        self.__cornucopia_position = (0, 0)
        self.__cornucopia_radius = cfgobj.getint("TheHungerBaubles", "cornucopia_radius")
        self.__spawned_num = 0

        self.collect_radius = cfgobj.getint("TheHungerBaubles", "collect_radius")
        self.__limit_weapons = cfgobj.getboolean("TheHungerBaubles", "limit_weapons")

        super(TheHungerBaublesGame, self).__init__(cfgobj)

    def game_get_info(self):
        return {"GAMENAME": "TheHungerBaubles"}

    def player_added(self, player, reason):
        super(TheHungerBaublesGame, self).player_added(player, reason)
        player.carrying = []
        player.collected = 0
        player.torpedo = False
        player.mine = False

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

        if isinstance(wobj, Weapon) and wobj.owner != None and wobj.owner.player != None:
            if isinstance(wobj, Torpedo):
                wobj.owner.player.torpedo = added
            elif isinstance(wobj, SpaceMine):
                wobj.owner.player.mine = added

        return super(TheHungerBaublesGame, self).world_add_remove_object(wobj, added)

    def get_player_cargo_value(self, player):
        return sum(b.value for b in player.carrying)

    def get_player_cargo_weight(self, player):
        return sum(b.weight for b in player.carrying)

    def collectBaubles(self, ship, bauble):
        logging.info("Collected Baubles Ship #%d bauble #%d", ship.id, bauble.id)
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

    def ejectBauble(self, player, bauble, died=False):
        logging.info("Ejecting Bauble Player %d Bauble #%d", player.netid, bauble.id)
        bauble.body.position = (player.object.body.position[0] + random.randint(-36, 36), player.object.body.position[1] + random.randint(-36, 36))
        bauble.destroyed = False # reset so that it won't get cleaned up
        player.carrying.remove(bauble)
        if not died:
            player.collected -= 1
            player.update_score(-bauble.value)

        self.world.append(bauble)
        logging.info("Done Ejecting Baubles Player %d", player.netid)

    def player_died(self, player, gone):
        # if ship destroyed, put baubles stored back
        for b in player.carrying[:]:
            self.ejectBauble(player, b, True)

        return super(TheHungerBaublesGame, self).player_died(player, gone)

    def server_process_network_message(self, ship, cmdname, cmddict={}):
        if cmdname == GAME_CMD_COLLECT:
            if cmddict.has_key("ID") and isinstance(cmddict["ID"], int) and cmddict["ID"] > 0:
                return CollectCommand(ship, self, cmddict["ID"])
            else:
                return "The Hunger Baubles Collect Command requires an id."
        elif cmdname == GAME_CMD_EJECT:
            if cmddict.has_key("ID") and isinstance(cmddict["ID"], int) and cmddict["ID"] > 0:
                return EjectCommand(ship, self, cmddict["ID"])
            else:
                return "The Hunger Baubles Eject Command requires an id."

    def server_process_command(self, ship, command):
        # The Hunger Baubles prevents firing while another torpedo of your exists
        #logging.info("Checking Command %s %s", repr(command), repr(ship.in_celestialbody))
        if self.__limit_weapons and hasattr(ship, "player"):
            if isinstance(command, FireTorpedoCommand) and ship.player.torpedo:
                logging.info("Preventing Ship #%d From Firing Torpedo", ship.id)
                return "The Hunger Baubles Rule - Can only fire one torpedo at a time"
            elif isinstance(command, DeploySpaceMineCommand) and ship.player.mine:
                logging.info("Preventing Ship #%d From Deploying Space Mine", ship.id)
                return "The Hunger Baubles Rule - Can only fire one space mine at a time"

        return command

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
        env.update({"POSITION": self.__cornucopia_position, "BAUBLES": baubles,
                    "TORPEDO": player.torpedo, "MINE": player.mine })

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
                bp = intpos(obj.body.position)
                text = debugfont().render(repr(len(player.carrying)), False, player.color)
                surface.blit(text, (bp[0]-36, bp[1]-4))
                text = debugfont().render(repr(self.get_player_cargo_weight(player)), False, player.color)
                surface.blit(text, (bp[0]+32, bp[1]-4))
                wrapcircle(surface, (0, 255, 255), bp, self.collect_radius, self.world.size, 1) # Pick up Range

        # Cornucopia
        wrapcircle(surface, (255, 255, 0), self.__cornucopia_position, self.__cornucopia_radius, self.world.size, 3)

    def round_start(self):
        logging.info("Game Start")

        self.__spawned_num = 0

        super(TheHungerBaublesGame, self).round_start()

    def world_create(self):
        super(TheHungerBaublesGame, self).world_create()

        self.__cornucopia_position = getPositionAwayFromOtherObjects(self.world, self.cfg.getint("TheHungerBaubles", "cornucopia_buffer_object"), self.cfg.getint("TheHungerBaubles", "cornucopia_buffer_edge"))

        #TODO: Remove anything left inside cornucopia?

class CollectCommand(OneTimeCommand):
    """
    The CollectCommand lets you pick up baubles in The Hunger Baubles Game.

    The ID of the object to pick up is required and must be within a specific distance from your ship.
    """
    NAME = GAME_CMD_COLLECT

    def __init__(self, obj, game, id):
        super(CollectCommand, self).__init__(obj, CollectCommand.NAME, required=8)
        self.target = id
        self.game = game

    def onetime(self):
        for wobj in self.game.world.getObjectsInArea(self._obj.body.position, self.game.collect_radius):
            if wobj.id == self.target and isinstance(wobj, Bauble):
                self.game.collectBaubles(self._obj, wobj)

    def __repr__(self):
        return super(CollectCommand, self).__repr__() + " ID: #%d" % (self.target)

class EjectCommand(OneTimeCommand):
    """
    The EjectCommand lets you eject baubles in The Hunger Baubles Game.

    The ID of the object to pick up is required and must be within a specific distance from your ship.
    """
    NAME = GAME_CMD_EJECT

    def __init__(self, obj, game, id):
        super(EjectCommand, self).__init__(obj, EjectCommand.NAME, required=24)
        self.target = id
        self.game = game

    def onetime(self):
        for wobj in self._obj.player.carrying:
            if wobj.id == self.target:
                self._obj.player.sound = "EJECT"
                self.game.ejectBauble(self._obj.player, wobj)
                return

    def __repr__(self):
        return super(EjectCommand, self).__repr__() + " ID: #%d" % (self.target)