"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2016 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from Game import BasicGame
from World.Entities import PhysicalEllipse
from World.WorldEntities import Nebula
from GUI.ObjWrappers.GUIEntity import GUIEntity
from World.WorldMath import intpos, PlayerStat, friendly_type, getPositionAwayFromOtherObjects, cfg_rand_min_max
from GUI.GraphicsCache import Cache
from GUI.Helpers import wrapcircle, debugfont
from ThreadStuff.ThreadSafe import ThreadSafeDict
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
        self._outposts = ThreadSafeDict()

        super(DiscoveryQuestGame, self).__init__(cfgobj)

        self._missions = cfgobj.get("DiscoveryQuest", "mission_objectives").split(",")
        self.scantime = cfgobj.getfloat("DiscoveryQuest", "scan_time")
        self.scanrange = cfgobj.getint("DiscoveryQuest", "scan_range")
        self.outpostdist = cfgobj.getint("DiscoveryQuest", "ship_spawn_dist")
        self.limitwarp = cfgobj.getboolean("DiscoveryQuest", "disable_warp_in_nebula")

    def game_get_info(self):
        return {"GAMENAME": "DiscoveryQuest"}

    def player_reset_mission(self, player):
        # get a number of missions for each thing
        player.mission = []
        player.scanned = []
        player.failed = False
        for i in xrange(cfg_rand_min_max(self.cfg, "DiscoveryQuest", "mission_num")):
            player.mission.append(random.choice(self._missions)) # TODO: validate that this player can still scan those types of objects

    def player_added(self, player, reason):
        if reason == BasicGame._ADD_REASON_REGISTER_:
            player.buffervalue = 0
            player.outpost = None
            player.lastids = []
            
        player.mission = []
        player.scanned = []
        player.failed = True

        return super(DiscoveryQuestGame, self).player_added(player, reason)

    def player_get_start_position(self, force = False):
        # pick a random outpost to spawn the player besides
        out = intpos(random.choice(self._outposts.values()).body.position)

        pos = (random.randint(out[0]-self.outpostdist, out[0]+self.outpostdist),
               random.randint(out[1]-self.outpostdist, out[1]+self.outpostdist))
        x = 0
        while len(self.world.getObjectsInArea(pos, self.outpostdist / 2)) > 0 and x < 15:
            x += 1
            pos = (random.randint(out[0]-self.outpostdist, out[0]+self.outpostdist),
                   random.randint(out[1]-self.outpostdist, out[1]+self.outpostdist))
        
        return pos

    def player_died(self, player, gone):
        if gone and player.outpost != None:
            player.outpost.home_for.remove(player)
            player.outpost = None

        if gone:
            for obj in self.world:
                if player in obj.scanned_by:
                    obj.scanned_by.remove(player)

        return super(DiscoveryQuestGame, self).player_died(player, gone)

    def player_get_stat_string(self, player):
        """
        Should return a string with information about the player and their current score.

        Defaults to:
        primary_score  secondary_score : player_name
        """
        if player.buffervalue > 0:
            return "%d %s B: %d" % (getattr(player, self._primary_victory), player.name, getattr(player, self._secondary_victory))
        else:
            return "%d %s" % (getattr(player, self._primary_victory), player.name)

    def world_add_remove_object(self, wobj, added):
        if isinstance(wobj, Outpost):
            if not added:
                del self._outposts[wobj.id]
            else:
                self._outposts[wobj.id] = wobj

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
            env["POSITION"] = intpos(player.outpost.body.position)
        env["FAILED"] = player.failed
        env["MISSION"] = player.mission
        obj = player.object
        if obj != None:
            cur = []
            for cmd in obj.commandQueue:
                if isinstance(cmd, ScanCommand):
                    cur.append(cmd.target)
            env["CURIDS"] = cur

        env["SUCIDS"] = player.lastids
        player.lastids = []

        return env

    def game_get_extra_radar_info(self, obj, objdata, player):
        super(DiscoveryQuestGame, self).game_get_extra_radar_info(obj, objdata, player)

        # return object's value for scanning
        if hasattr(obj, "value"):
            objdata["VALUE"] = obj.value

        objdata["SUCCESS"] = player in obj.scanned_by

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
        #logging.info("Checking Command %s %s", repr(command), repr(ship.in_celestialbody))
        if self.limitwarp and isinstance(command, WarpCommand):
            for body in ship.in_celestialbody:
                if isinstance(body, Nebula):
                    logging.info("Preventing Ship #%d From Warping As In Nebula", ship.id)
                    return "Discovery Quest Rule - Can't warp when in Nebula"

        return command

    def dq_finished_scan(self, ship, obj, success):
        if obj != None:
            logging.info("Ship #%d finished scan of object #%d and was successful? [%s]", ship.id, obj.id, repr(success))
        else:
            logging.info("Ship #%d finished scan of unknown object (never saw id)", ship.id)

        if success:
            ship.player.lastids.append(obj.id)

            if isinstance(obj, Outpost) and (ship.player in obj.home_for or ship.player.outpost == None):
                # scanned player's own Outpost, do Mission Stuff HERE
                if ship.player.outpost == None:
                    # establish as ship's Outpost
                    ship.player.outpost = obj
                    obj.home_for.append(ship.player)
                    ship.player.update_score(ship.player.buffervalue + obj.value * 2) # Score initial points + 2*outpost value for establishing base
                    ship.player.buffervalue = 0
                    ship.player.sound = "SUCCESS"
                
                if not ship.player.failed and len(ship.player.mission) == 0: # completed mission exactly
                    points = 0
                    # tally points of scanned objects
                    for obj in ship.player.scanned:
                        points += obj.value
                    ship.player.sound = "MISSION"
                    ship.player.update_score(points * self.cfg.getfloat("DiscoveryQuest", "mission_bonus_multiplier"))

                self.player_reset_mission(ship.player)

            elif ship.player in obj.scanned_by:
                logging.info("Ship #%d has ALREADY scanned object #%d", ship.id, obj.id)
            else:
                # mission checks
                if friendly_type(obj) in ship.player.mission:
                    ship.player.mission.remove(friendly_type(obj))
                else:
                    ship.player.failed = True
                ship.player.scanned.append(obj)

                # update scores
                obj.scanned_by.append(ship.player)
                ship.player.sound = "SUCCESS"
                if ship.player.outpost != None:                    
                    ship.player.update_score(obj.value)
                else: #haven't found outpost, need to buffer points
                    ship.player.buffervalue += obj.value
    #end dq_finished_scan

    def gui_draw_game_world_info(self, surface, flags, trackplayer):
        for player in self.game_get_current_player_list():
            obj = player.object
            if obj != None:
                bp = intpos(obj.body.position)
                wrapcircle(surface, (0, 255, 255), bp, self.scanrange, self.world.size, 1) # Scan Range
                text = debugfont().render("%s [%s]" % (repr(player.mission), player.failed), False, (0, 255, 255))
                surface.blit(text, (bp[0]-text.get_width()/2, bp[1] - 6))

        if trackplayer != None:
            curs = []
            curf = []
            obj = trackplayer.object
            if obj != None:
                for cmd in obj.commandQueue:
                    if isinstance(cmd, ScanCommand):
                        if cmd.success:
                            curs.append(cmd.target)
                        else:
                            curf.append(cmd.target)

            for obj in self.world:
                if trackplayer in obj.scanned_by:
                    wrapcircle(surface, (0, 255, 255), intpos(obj.body.position), obj.radius + 4, self.world.size, 4)
                if obj.id in curs:
                    wrapcircle(surface, (255, 255, 0), intpos(obj.body.position), obj.radius + 5, self.world.size, 2)
                elif obj.id in curf:
                    wrapcircle(surface, (255, 0, 0), intpos(obj.body.position), obj.radius + 5, self.world.size, 2)

class ScanCommand(Command):
    """
    The ScanCommand lets you research objects to complete missions in Discovery Quest.

    The ID of the object to scan is required and must be within a third of your radar range for a full duration of 2.5 seconds in order to be successfully scanned.
    """
    NAME = GAME_CMD_SCAN

    def __init__(self, obj, game, id):
        super(ScanCommand, self).__init__(obj, ScanCommand.NAME, game.scantime, required=4)
        self.energycost = 4
        self.target = id
        self.targetobj = None
        self.game = game
        self.success = True
        self.sound = False

    def isExpired(self):
        done = super(ScanCommand, self).isExpired()
        # hook back to game when done scanning
        if done:
            self.game.dq_finished_scan(self._obj, self.targetobj, self.success)
        return done

    def execute(self, t):
        if self.success:
            for wobj in self.game.world.getObjectsInArea(self._obj.body.position, self.game.scanrange):
                if wobj.id == self.target:
                    if not self.sound:
                        self._obj.player.sound = "SCAN"
                        self.sound = True
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
    Outposts are bases for research.
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

    @staticmethod
    def spawn(world, cfg, pos=None):
        if pos == None:
            pos = getPositionAwayFromOtherObjects(world, cfg.getint("Outpost", "buffer_object"), cfg.getint("Outpost", "buffer_edge"))
        o = Outpost(pos)
        world.append(o)
        return o

    #def getExtraInfo(self, objData, player):
    #    objData["OWNERID"] = self.owner.id
        
    #def newOwner(self, ship):
    #    self.owner = ship
