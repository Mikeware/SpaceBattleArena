"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2015 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from Game import BasicGame
from World.WorldGenerator import getPositionAwayFromOtherObjects
from World.Entities import PhysicalEllipse
from World.WorldEntities import Nebula
from GUI.ObjWrappers.GUIEntity import GUIEntity
from World.WorldMath import intpos, PlayerStat, friendly_type
from GUI.GraphicsCache import Cache
from GUI.Helpers import wrapcircle, debugfont
from World.WorldCommands import WarpCommand
from World.Commanding import Command
import logging, random

GAME_CMD_SCAN = "DQSCN"

class DiscoveryQuestGame(BasicGame):
    """
    Discovery Quest is a game of exploration.

    Ships must 'Scan' various objects in order to accumulate points.  Every type of object in the game is worth a different number of points.
    Scanning is different from Radar, and requires a precise ID and takes more time and energy to perform.  It also has a limited range which you must stay within for the whole duration of the scan.
    You CANNOT scan the same object more than once for points.

    Ships must establish an 'Outpost' by scanning it.  Once they have done so, they will start to receive 'Missions'.  They initially won't score points for scanned objects until an Outpost is established.
    All points for things scanned before making an Outpost will be awarded when an Outpost is established.

    A Mission dictates which objects a ship should go scan.  If a ship goes and scans ONLY those things, bonus points will be awarded when they return to their outpost and Scan it again.

    Scanning their outpost will always give them a new mission.

    Your Ship being destroyed clears/fails your mission, so you must return to your established outpost if you want a new one.
    """
    def __init__(self, cfgobj):
        super(DiscoveryQuestGame, self).__init__(cfgobj)

    def game_get_info(self):
        return {"GAMENAME": "DiscoveryQuest"}

    def player_added(self, player, reason):
        if reason == BasicGame._ADD_REASON_REGISTER_:
            player.buffervalue = 0
            player.outpost = None
        return super(DiscoveryQuestGame, self).player_added(player, reason)

    def player_died(self, player, gone):
        if gone and player.outpost != None:
            player.outpost.home_for.remove(player)
            player.outpost = None

        if gone:
            for obj in self.world:
                if player in obj.scanned_by:
                    obj.scanned_by.remove(player)

        return super(DiscoveryQuestGame, self).player_died(player, gone)

    def world_create(self, pys = True):
        world = super(DiscoveryQuestGame, self).world_create(pys)
        for x in xrange(self.cfg.getint("DiscoveryQuest", "outpost_number")):
            world.append(Outpost(getPositionAwayFromOtherObjects(world, 80, 30)))
        return world

    def world_add_remove_object(self, wobj, added):
        if added:
            wobj.scanned_by = [] # objects keep track of who scans them

            # give object point value
            opt = "points_" + friendly_type(wobj).lower()
            if self.cfg.has_option("DiscoveryQuest", opt):
                wobj.value = self.cfg.getint("DiscoveryQuest", opt)

        return super(DiscoveryQuestGame, self).world_add_remove_object(wobj, added)

    def game_get_extra_environment(self, player):
        env = super(DiscoveryQuestGame, self).game_get_extra_environment(player)

        if player.outpost != None:
            env["OUTPOST"] = intpos(player.outpost.body.position)
        env["FAILED"] = True
        env["MISSION"] = []

        return env

    def game_get_extra_radar_info(self, obj, objdata):
        super(DiscoveryQuestGame, self).game_get_extra_radar_info(obj, objdata)

        # return object's value for scanning
        if hasattr(obj, "value"):
            objdata["VALUE"] = obj.value

    def server_process_network_message(self, ship, cmdname, cmddict={}):
        """
        Called by the server when it doesn't know how to convert a network message into a Ship Command.
        This function is used to create commands custom to the game itself.
        
        Parameters:
            ship: Ship object which will process the Command
            cmdname: string network shortcode for command, set overriding getName in ShipCommand on Client
            cmddict: dictionary of properties of a command, set using private fields on ShipCommand class

        Return:
            return a server 'Command' object, a string indicating an error, or None
        """
        if cmdname == GAME_CMD_SCAN:
            if cmddict.has_key("TARGET") and isinstance(cmddict["TARGET"], int) and cmddict["TARGET"] > 0:
                return ScanCommand(ship, self, cmddict["TARGET"])
            else:
                return "Discovery Quest Scan Command requires a target id."

    def server_process_command(self, ship, command):
        # Discovery Quest prevents warp in a nebula
        if isinstance(command, WarpCommand):
            for body in ship.in_celestialbody:
                if isinstance(body, Nebula):
                    return "Discovery Quest Rule - Can't warp when in Nebula"

        return command

    def dq_finished_scan(self, ship, obj, success):
        if obj != None:
            logging.info("Ship #%d finished scan of object #%d and was successful? [%s]", ship.id, obj.id, repr(success))
        else:
            logging.info("Ship #%d finished scan of unknown object (never saw id)", ship.id)

        if success:
            if isinstance(obj, Outpost) and (ship.player in obj.home_for or ship.player.outpost == None):
                # scanned player's own Outpost, do Mission Stuff HERE
                if ship.player.outpost == None:
                    # establish as ship's Outpost
                    ship.player.outpost = obj
                    obj.home_for.append(ship.player)
                    self.player_update_score(ship.player, ship.player.buffervalue) # Score initial points
                    ship.player.buffervalue = 0

                pass
            elif ship.player in obj.scanned_by:
                logging.info("Ship #%d has ALREADY scanned object #%d", ship.id, obj.id)
            else:
                obj.scanned_by.append(ship.player)
                if ship.player.outpost != None:
                    self.player_update_score(ship.player, obj.value)
                else: #haven't found outpost, need to buffer points
                    ship.player.buffervalue += obj.value
    #end dq_finished_scan

    def gui_draw_game_world_info(self, surface, flags, trackplayer):
        for player in self.game_get_current_player_list():
            if player.object != None:
                wrapcircle(surface, (0, 255, 255), intpos(player.object.body.position), player.object.radarRange / 3, self.world.size, 1) # Scan Range

        if trackplayer != None:
            for obj in self.world:
                if trackplayer in obj.scanned_by:
                    wrapcircle(surface, (0, 255, 255), intpos(obj.body.position), obj.radius + 4, self.world.size, 4)

class ScanCommand(Command):
    """
    The ScanCommand lets you research objects to complete missions in Discovery Quest.

    The ID of the object to scan is required and must be within a third of your radar range for a full duration of 2.5 seconds in order to be successfully scanned.
    """
    NAME = GAME_CMD_SCAN

    def __init__(self, obj, game, id):
        super(ScanCommand, self).__init__(obj, ScanCommand.NAME, 2.5, required=4)
        self.energycost = 4
        self.target = id
        self.targetobj = None
        self.game = game
        self.success = True

    def isExpired(self):
        done = super(ScanCommand, self).isExpired()
        # hook back to game when done scanning
        if done:
            self.game.dq_finished_scan(self._obj, self.targetobj, self.success)
        return done

    def execute(self, t):
        if self.success:
            for wobj in self.game.world.getObjectsInArea(self._obj.body.position, self._obj.radarRange / 3):
                if wobj.id == self.target:
                    self.targetobj = wobj
                    return super(ScanCommand, self).execute(t)

            self.success = False

        return super(ScanCommand, self).execute(t)

    def __repr__(self):
        return super(ScanCommand, self).__repr__() + " ID: #%d [%s]" % (self.target, str(self.success))

class OutpostWrapper(GUIEntity):
    def __init__(self, obj, world):
        super(OutpostWrapper, self).__init__(obj, world)
        self.surface = Cache().getImage("Games/Outpost" + str(random.randint(1, Cache().getMaxImages("Games/Outpost"))))

    def draw(self, surface, flags):
        bp = intpos(self._worldobj.body.position)
        surface.blit(self.surface, (bp[0] - 32, bp[1] - 64))

        # TODO: Owner ID Display

        if flags["NAMES"]:
            text = ""
            for player in self._worldobj.home_for:
                text += player.name + " "
            text = debugfont().render(text, False, (0, 255, 255))
            surface.blit(text, (bp[0]-text.get_width()/2, bp[1]-18))

        #if flags["NAMES"]:
            # HACK TODO: Ship name should be from team
            #text = debugfont().render(self._worldobj.owner.player.name, False, self._worldobj.owner.player.color)
            #surface.blit(text, (bp[0]-text.get_width()/2, bp[1]-18))

        #if flags["STATS"]:
        #    text = debugfont().render(repr(self._worldobj.stored), False, self._worldobj.owner.player.color)
        #    surface.blit(text, (bp[0]-text.get_width()/2, bp[1]+4))

        super(OutpostWrapper, self).draw(surface, flags)

class Outpost(PhysicalEllipse):
    WRAPPERCLASS = OutpostWrapper
    """
    Baubles are small prizes worth different amounts of points
    """
    def __init__(self, pos):
        super(Outpost, self).__init__((60, 120), 4000, pos)
        self.shape.elasticity = 0.8
        self.health = PlayerStat(0)

        self.body.velocity_limit = 0
        
        self.shape.group = 1

        self.home_for = []

    def collide_start(self, otherobj):
        return False

    #def getExtraInfo(self, objData):
    #    objData["OWNERID"] = self.owner.id
        
    #def newOwner(self, ship):
    #    self.owner = ship
