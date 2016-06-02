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
from World.WorldEntities import Ship, Weapon, Torpedo, SpaceMine, Dragon, Asteroid, Planet, WormHole
from GUI.ObjWrappers.GUIEntity import GUIEntity, wrapcircle
from World.WorldMath import intpos, friendly_type, PlayerStat, aligninstances, getPositionAwayFromOtherObjects, cfg_rand_min_max
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

        self.__asteroid_bonus = cfgobj.getfloat("TheHungerBaubles", "asteroid_bauble_percent")
        self.__asteroid_values = map(int, cfgobj.get("TheHungerBaubles", "asteroid_bauble_points").split(","))

        self.__dragon_bonus = cfgobj.getfloat("TheHungerBaubles", "dragon_bauble_percent")
        self.__dragon_values = map(int, cfgobj.get("TheHungerBaubles", "dragon_bauble_points").split(","))

        self.__bauble_spawner = None

        self.__spawn_success = 0
        self.__spawn_fail = 0

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
        # If an Asteroid or Dragon is destroyed, deposit bauble
        if (isinstance(wobj, Asteroid) or isinstance(wobj, Dragon)) and hasattr(wobj, "killedby") and wobj.killedby != None:
            obj = wobj.killedby
            logging.info("Object #%d Killed By: #%d", wobj.id, obj.id)
            if isinstance(obj, Torpedo) and hasattr(obj, "owner") and obj.owner != None and isinstance(obj.owner, Ship):
                logging.info("Was Torpedoed")
                v = 0
                if isinstance(wobj, Asteroid) and random.random() < self.__asteroid_bonus:
                    v = random.choice(self.__asteroid_values)
                elif isinstance(wobj, Dragon) and random.random() < self.__dragon_bonus:
                    v = random.choice(self.__dragon_values)
                
                if v > 0:
                    b = Bauble.spawn(self.world, self.cfg, wobj.body.position, v)
                    logging.info("Spawned Bonus Bauble #%d with value %d and weight %d", b.id, b.value, b.weight)

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
        # if ship destroyed (not disconnected), put baubles stored back
        if gone:
            player.carrying = []
        else:
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

        # Cornucopia (draw it smaller as we detect midpoint of ship, but will look like when ships enter)
        c = (255 - int(self.__spawn_success * 85), 255 - int(self.__spawn_fail * 85), 0)
        wrapcircle(surface, c, self.__cornucopia_position, self.__cornucopia_radius - 28, self.world.size, 3)

    def round_start(self):
        logging.info("Game Start")

        self.__spawned_num = 0

        super(TheHungerBaublesGame, self).round_start()

        # spawn a high-value bauble and start our perpetual timer
        self.__cornucopia_bauble_spawn(True)

        # spawn some dragons
        for num in xrange(self.cfg.getint("TheHungerBaubles", "cornucopia_spawn_initial_dragons")):
            pos = (self.__cornucopia_position[0] + random.randint(-64, 64), self.__cornucopia_position[1] + random.randint(-64, 64))
            Dragon.spawn(self.world, self.cfg, pos)

    def __start_bauble_timer(self):
        self.__bauble_spawner = CallbackTimer(cfg_rand_min_max(self.cfg, "TheHungerBaubles", "cornucopia_spawn_time"), self.__cornucopia_bauble_spawn)
        self.__bauble_spawner.start()

    def world_create(self):
        super(TheHungerBaublesGame, self).world_create()

        self.__cornucopia_position = getPositionAwayFromOtherObjects(self.world, self.cfg.getint("TheHungerBaubles", "cornucopia_buffer_object"), self.cfg.getint("TheHungerBaubles", "cornucopia_buffer_edge"))

        for obj in self.world.getObjectsInArea(self.__cornucopia_position, self.__cornucopia_radius + 128):
            # remove planets in Cornucopia
            if isinstance(obj, Planet):
                logging.info("Removing Planet from Middle of Cornucopia #%d", obj.id)
                self.world.remove(obj)
            # try and move worm holes away from center
            elif isinstance(obj, WormHole):
                logging.info("Moving WormHole from Middle of Cornucopia #%d", obj.id)
                ang = obj.body.position.get_angle_between(self.__cornucopia_position)
                dist = random.randint(self.__cornucopia_radius + 128, self.__cornucopia_radius + 256)
                obj.body.position = (min(max(32, self.__cornucopia_position[0] + math.cos(ang) * dist), self.world.width - 32), 
                                     min(max(32, self.__cornucopia_position[1] + math.sin(ang) * dist), self.world.height - 32))

    def round_over(self):
        # Stop Spawning Baubles
        if self.__bauble_spawner != None:
            self.__bauble_spawner.cancel()
            self.__bauble_spawner = None

        super(TheHungerBaublesGame, self).round_over()

    def __cornucopia_bauble_spawn(self, init=False):
        logging.info("Trying to Spawn Bauble in Cornucopia")
        self.__start_bauble_timer()

        # if we see a ship in the middle don't spawn
        for obj in self.world.getObjectsInArea(self.__cornucopia_position, self.__cornucopia_radius):
            if isinstance(obj, Ship):
                logging.info("Ship Detected in Cornucopia #%d", obj.id)
                self.__spawn_fail = 3
                if self.cfg.getboolean("TheHungerBaubles", "cornucopia_spawn_dragon"):
                    d = Dragon.spawn(self.world, self.cfg, self.__cornucopia_position)
                    logging.info("Spawned Dragon #%d in Cornucopia", d.id)
                return

        values = map(int, self.cfg.get("TheHungerBaubles", "cornucopia_spawn_points").split(","))
        
        if init:
            num = self.cfg.getint("TheHungerBaubles", "cornucopia_spawn_initial_num")
        else:
            num = self.cfg.getint("TheHungerBaubles", "cornucopia_spawn_time_num")

        for i in xrange(num):
            ang = random.randint(0, 359)
            dist = random.randint(0, int(self.__cornucopia_radius / 2))
            pos = (self.__cornucopia_position[0] + math.cos(math.radians(ang)) * dist,
                   self.__cornucopia_position[1] + math.sin(math.radians(ang)) * dist)
            b = Bauble.spawn(self.world, self.cfg, pos, random.choice(values))
            logging.info("Spawned Bauble in Cornucopia #%d with value %d and weight %d", b.id, b.value, b.weight)

        self.__spawn_success = 3

    def game_update(self, t):
        super(TheHungerBaublesGame, self).game_update(t)
        
        # decrement visual effect counters
        if self.__spawn_fail > 0:
            self.__spawn_fail = max(self.__spawn_fail - t, 0)
        if self.__spawn_success > 0:
            self.__spawn_success = max(self.__spawn_success - t, 0)

class CollectCommand(OneTimeCommand):
    """
    The CollectCommand lets you pick up baubles in The Hunger Baubles Game.

    The ID of the object to pick up is required and must be within a specific distance from your ship.
    """
    NAME = GAME_CMD_COLLECT

    def __init__(self, obj, game, id):
        self.target = id
        self.game = game

        super(CollectCommand, self).__init__(obj, CollectCommand.NAME, True, 0.2, required=8)

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
        self.target = id
        self.game = game

        for wobj in obj.player.carrying:
            if wobj.id == self.target:
                weight = wobj.weight
                value = wobj.value

        super(EjectCommand, self).__init__(obj, EjectCommand.NAME, ttl=0.5*weight, required=value*3)

    def onetime(self):
        for wobj in self._obj.player.carrying:
            if wobj.id == self.target:
                self._obj.player.sound = "EJECT"
                self.game.ejectBauble(self._obj.player, wobj)
                return

    def __repr__(self):
        return super(EjectCommand, self).__repr__() + " ID: #%d" % (self.target)