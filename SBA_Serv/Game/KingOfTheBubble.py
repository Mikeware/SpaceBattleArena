"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2015 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from Game import BasicGame
from World.Entities import Entity, PhysicalRound
from World.WorldEntities import Ship
from GUI.ObjWrappers.GUIEntity import GUIEntity
from World.WorldMath import intpos, friendly_type, PlayerStat
from GUI.GraphicsCache import Cache
from GUI.Helpers import debugfont, wrapcircle, namefont
import logging, random
import pygame
from operator import attrgetter

# 'Bubbles' appear in the world.  Players earn points while in the bubble.
# Points are distributed across the players in the bubble (so more players = less points)
# I.E. The amount of points earned also slows down with more people in the bubble
# Each bubble has specific number of points to give and shrinks in size as points are depleted

# If a ship dies, a bubble is created with some of their points (percent or min) create a new bubble
#   If the ship was in a bubble, those points may be added to the existing bubble

class KingOfTheBubbleGame(BasicGame):
    
    def __init__(self, cfgobj):
        self.__bubbles = {}
        self.__sizebase = float(cfgobj.getint("KingOfTheBubble", "bubble_radius_min"))
        self.__sizemin = cfgobj.getint("KingOfTheBubble", "bubble_points_min")
        self.__sizemax = cfgobj.getint("KingOfTheBubble", "bubble_points_max")
        self.__pointspeed = cfgobj.getint("KingOfTheBubble", "bubble_points_drain_speed")
        self.__maxbubbles = cfgobj.getint("KingOfTheBubble", "bubble_number_max")
        self.__bubbletime = cfgobj.getint("KingOfTheBubble", "bubble_time_alive_min")
        self.__bubbletimevar = cfgobj.getint("KingOfTheBubble", "bubble_time_alive_variance")

        super(KingOfTheBubbleGame, self).__init__(cfgobj)
        
        self.__pointatleast = self.cfg.getint("KingOfTheBubble", "steal_points_min")
        self.__pointpercent = float(self.cfg.getint("KingOfTheBubble", "steal_points_percent"))

    def world_create(self, pys=True):
        w = ConfiguredWorld(self, self.cfg, pys)
        
        # Add some initial small Baubles
        self.addBubbles(w, self.__maxbubbles)

        return w

    def game_get_info(self):
        return {"GAMENAME": "KingOfTheBubble"}

    def addBubbles(self, w, num, setpoints=None, pos=None, pname=None, force=False):
        logging.info("Adding %d Bubbles (%s)", num, repr(force))
        for i in xrange(num):
            points = random.randint(self.__sizemin, self.__sizemax)
            if setpoints != None:
                points = setpoints
            if pos == None:
                npos = getPositionAwayFromOtherObjects(w, 100, 30, force)
            else:
                npos = pos
            bt = self.__bubbletime
            if bt > 0: 
                bt += random.randint(0, self.__bubbletimevar)
            if hasattr(self, "world"):
                # NOTE: This doesn't follow the paradigm, but we need the latest reference to the world as this gets screwed up resetting the world...
                b = Bubble(npos, self.__sizebase, points, self.__pointspeed, bt, pname, self.world, self) 
            else:
                b = Bubble(npos, self.__sizebase, points, self.__pointspeed, bt, pname, w, self) # this should only be the case for the initial world
            # The Whole Lifecycle of the Game and Rounds needs to be redefined for V2
            w.append(b)
            self.__bubbles[b.id] = b
        logging.info("Done Adding Bubbles")

    def player_died(self, player, gone):
        # calculate points to lose
        addyum = player.score * (self.__pointpercent / 100.0) > self.__pointatleast
        stealpoints = max(player.score * (self.__pointpercent / 100.0), self.__pointatleast)
        self.player_update_score(player, -stealpoints)
            
        # see if a Bubble is near us
        added = False
        for obj in self.world.getObjectsInArea(player.object.body.position, 64): # look within a certain range of a ship area
            if isinstance(obj, Bubble) and obj.TTL == None:
                added = True
                obj.size += stealpoints
                obj.pname = player.name
                break

        if not added and addyum:            
            self.addBubbles(self.world, 1, stealpoints, intpos(player.object.body.position), player.name)

        super(KingOfTheBubbleGame, self).player_died(player, gone)

    def world_add_remove_object(self, wobj, added):
        logging.debug("BH Add Object(%s): #%d (%s)", repr(added), wobj.id, friendly_type(wobj))
        if isinstance(wobj, Bubble) and not added:
            del self.__bubbles[wobj.id]
            # Bubble was removed, we should add a new one
            if len(self.__bubbles) < self.__maxbubbles:
                self.addBubbles(self.world, 1)

        super(KingOfTheBubbleGame, self).world_add_remove_object(wobj, added)

    def game_get_extra_environment(self, player):
        bub = []
        for b in self.__bubbles.values():
            bub.append(intpos(b.body.position))

        env = super(KingOfTheBubbleGame, self).game_get_extra_environment(player)
        env["BUBBLES"] = bub

        return env
        
    def game_get_extra_radar_info(self, obj, objdata, player):
        super(KingOfTheBubbleGame, self).game_get_extra_radar_info(obj, objdata, player)
        if hasattr(obj, "player"):
            objdata["VALUE"] = obj.player.score

class BubbleWrapper(GUIEntity):
    def __init__(self, obj, world):
        super(BubbleWrapper, self).__init__(obj, world)
        self._world = world

    def draw(self, surface, flags):
        # Check if Thrusting or Braking
        #surface.blit(self.surface, intpos((self._worldobj.body.position[0] - 8, self._worldobj.body.position[1] - 8)))        
        bp = intpos(self._worldobj.body.position)
        wrapcircle(surface, (0, 255, 255), bp, int(self._worldobj.size), self._world.size, 1) # Radar

        if flags["GAME"]:
            text = namefont().render("Points: %.1f" % (self._worldobj.size - self._worldobj.basesize), False, (0, 255, 255))
            surface.blit(text, (bp[0]-text.get_width()/2, bp[1]-44))
            if self._worldobj.pname != None:
                text = namefont().render("From %s" % self._worldobj.pname, False, (0, 255, 255))
                surface.blit(text, (bp[0]-text.get_width()/2, bp[1]+44))
        
        super(BubbleWrapper, self).draw(surface, flags)

class Bubble(PhysicalRound):
    WRAPPERCLASS = BubbleWrapper
    """
    Baubles are small prizes worth different amounts of points
    """
    def __init__(self, pos, basesize, size, speed, time, pname, world, game):
        super(Bubble, self).__init__(2, 2000, pos)
        self.shape.elasticity = 0.8
        self.health = PlayerStat(0)

        self.shape.group = 1
        
        self.explodable = False
        self.pname = pname
        
        self.basesize = basesize
        self.size = basesize + size
        
        self.timetoshrink = time
        
        self.pointspeed = speed
        self.__world = world
        self.__game = game

    def collide_start(self, otherobj):
        return False
        
    def update(self, t):
        super(Bubble, self).update(t)
        
        ships = []
        for obj in self.__world.getObjectsInArea(self.body.position, self.size + 28): # add the ship radius so it looks like you get points if you overlap
            if isinstance(obj, Ship):
                ships.append(obj)
        
        for ship in ships:
            self.__game.player_update_score(ship.player, t * self.pointspeed)
            #logging.info("Player %s getting points %d", ship.player.name, ship.player.score)
        
        self.size -= (t * self.pointspeed * len(ships))
        if self.size < 0:
            self.size = 0
        
        if self.timetoshrink > 0 and self.timealive > self.timetoshrink and len(ships) == 0:
            self.size -= (t * self.pointspeed)
        
        if self.size <= self.basesize:
            self.TTL = self.timealive - 1 # schedule this object for removal        

    def getExtraInfo(self, objData, player):
        objData["VALUE"] = (self.size - self.basesize)
        # Overwrite the 'radius' to show where you can be hit
        objData["HITRADIUS"] = self.size + 28
