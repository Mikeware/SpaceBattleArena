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
from World.WorldMath import intpos, PlayerStat
from GUI.GraphicsCache import Cache
from GUI.Helpers import wrapcircle
from World.WorldCommands import WarpCommand
from World.Commanding import Command
import logging, random

GAME_CMD_SCAN = "DQSCN"

class DiscoveryQuestGame(BasicGame):
    """
    Discovery Quest is an exploration game.


    """
    
    def __init__(self, cfgobj):
        super(DiscoveryQuestGame, self).__init__(cfgobj)

        self.world.append(Outpost(getPositionAwayFromOtherObjects(self.world, 80, 30)))


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

    def dq_finished_scan(self, ship, id, success):
        logging.info("Ship #%d finished scan of object #%d and was successful? [%s]", ship.id, id, repr(success))
        self.player_update_score(ship.player, 5)


    def gui_draw_game_world_info(self, surface, flags):
        for player in self.game_get_current_player_list():
            if player.object != None:
                wrapcircle(surface, (0, 255, 255), intpos(player.object.body.position), player.object.radarRange / 3, self.world.size, 1) # Scan Range

        return super(DiscoveryQuestGame, self).gui_draw_game_world_info(surface, flags)

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
        self.game = game
        self.success = True

    def isExpired(self):
        done = super(ScanCommand, self).isExpired()
        # hook back to game when done scanning
        if done:
            self.game.dq_finished_scan(self._obj, self.target, self.success)
        return done

    def execute(self, t):
        if self.success:
            for wobj in self.game.world.getObjectsInArea(self._obj.body.position, self._obj.radarRange / 3):
                if wobj.id == self.target:
                    return super(ScanCommand, self).execute(t)

            self.success = False

        return super(ScanCommand, self).execute(t)

class OutpostWrapper(GUIEntity):
    def __init__(self, obj, world):
        super(OutpostWrapper, self).__init__(obj, world)
        self.surface = Cache().getImage("Games/Outpost" + str(random.randint(1, Cache().getMaxImages("Games/Outpost"))))

    def draw(self, surface, flags):
        bp = intpos(self._worldobj.body.position)
        surface.blit(self.surface, (bp[0] - 32, bp[1] - 64))

        # TODO: Owner ID Display

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

        self.stored = 0

    def collide_start(self, otherobj):
        return False

    #def getExtraInfo(self, objData):
    #    objData["OWNERID"] = self.owner.id
        
    #def newOwner(self, ship):
    #    self.owner = ship
