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
from World.WorldEntities import Entity, Ship
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
        self.__sizebase = float(cfgobj.getint("KingOfTheBubble", "bubbleminradius"))
        self.__sizemin = cfgobj.getint("KingOfTheBubble", "bubbleminpoints")
        self.__sizemax = cfgobj.getint("KingOfTheBubble", "bubblemaxpoints")
        self.__pointspeed = cfgobj.getint("KingOfTheBubble", "bubblepointspeed")
        self.__maxbubbles = cfgobj.getint("KingOfTheBubble", "numbubbles")
        self.__bubbletime = cfgobj.getint("KingOfTheBubble", "bubbletime")
        self.__bubbletimevar = cfgobj.getint("KingOfTheBubble", "bubbletimevar")

        super(KingOfTheBubbleGame, self).__init__(cfgobj)
        
        self.__highscore = 0
        #self.__deathpenalty = self.cfg.getint("KingOfTheBubble", "deathpenalty")
        self.__initialpoints = self.cfg.getint("KingOfTheBubble", "initialpoints")
        self.__pointatleast = self.cfg.getint("KingOfTheBubble", "stealminpoints")
        self.__pointpercent = float(self.cfg.getint("KingOfTheBubble", "stealpercent"))

    def GUICFG(self):
        super(KingOfTheBubbleGame, self).GUICFG()

        self.__dfont = debugfont()

    def createWorld(self, pys=True):
        w = ConfiguredWorld(self, self.cfg, pys)
        
        # Add some initial small Baubles
        self.addBubbles(w, self.__maxbubbles)

        return w

    def getInitialInfoParameters(self):
        return {"GAMENAME": "KingOfTheBubble"}

    def registerPlayer(self, name, color, imgindex, netid):
        return super(KingOfTheBubbleGame, self).registerPlayer(name, color, imgindex, netid)

    def addPlayerAttributes(self, player):
        player.score = self.__initialpoints
        player.deaths = 0

        return player

    def addBubbles(self, w, num, setpoints=None, pos=None, pname=None, force=False):
        logging.info("Adding %d Baubles (%s)", num, repr(force))
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
                b = Bubble(npos, self.__sizebase, points, self.__pointspeed, bt, pname, self.world) 
            else:
                b = Bubble(npos, self.__sizebase, points, self.__pointspeed, bt, pname, w) # this should only be the case for the initial world
            # The Whole Lifecycle of the Game and Rounds needs to be redefined for V2
            w.append(b)
            self.__bubbles[b.id] = b
        logging.info("Done Adding Baubles")

    def worldAddRemoveObject(self, wobj, added):
        logging.debug("BH Add Object(%s): #%d (%s)", repr(added), wobj.id, friendly_type(wobj))
        if isinstance(wobj, Ship) and (wobj.disconnected or wobj.killed):
            return super(KingOfTheBubbleGame, self).worldAddRemoveObject(wobj, added)               
        if not added and isinstance(wobj, Ship) and wobj.player.netid in self._players:
            nid = wobj.player.netid

            self._players[nid].object = None                     

            # calculate points to lose
            addyum = self._players[nid].score * (self.__pointpercent / 100.0) > self.__pointatleast
            stealpoints = max(self._players[nid].score * (self.__pointpercent / 100.0), self.__pointatleast)            
            self._players[nid].score -= stealpoints
            
            # see if a Bubble is near us
            added = False
            for obj in self.world.getObjectsInArea(wobj.body.position, 64): # look within a certain range of a ship area
                if isinstance(obj, Bubble) and obj.TTL == None:
                    added = True
                    obj.size += stealpoints
                    obj.pname = self._players[nid].name
                    break

            if not added and addyum:            
                self.addBubbles(self.world, 1, stealpoints, intpos(wobj.body.position), self._players[nid].name)
            
            #self._players[nid].score -= self.__deathpenalty
            self._players[nid].deaths += 1
            if self._players[nid].score < 0:
                self._players[nid].score = 0

            # readd
            self._addShipForPlayer(nid, True)
        
        if isinstance(wobj, Bubble) and not added:
            del self.__bubbles[wobj.id]
            # Bubble was removed, we should add a new one
            if len(self.__bubbles) < self.__maxbubbles:
                self.addBubbles(self.world, 1)

    # Ignore anything that hits a bubble
    def worldObjectPreCollision(self, shapes):
        types = []
        objs = []
        for shape in shapes:
            objs.append(self.world[shape.id])
            types.append(friendly_type(objs[-1]))

        if "Bubble" in types:
            return [ False, [] ]
            
        return super(KingOfTheBubbleGame, self).worldObjectPreCollision(shapes)
        
    def getExtraEnvironment(self, player):
        bub = []
        for b in self.__bubbles.values():
            bub.append(intpos(b.body.position))

        return {"BUBBLES": bub, "SCORE": player.score, "HIGHSCORE": self.__highscore, "DEATHS": player.deaths}
        
    def getExtraRadarInfo(self, obj, objdata):
        super(KingOfTheBubbleGame, self).getExtraRadarInfo(obj, objdata)
        if hasattr(obj, "player"):
            objdata["VALUE"] = obj.player.score

    def getPlayerStats(self, current=False):
        if current:
            p = self.getCurrentPlayers() #.itervalues()
        else:
            p = self._players.itervalues()
        #eif
        stat = sorted(p, key=attrgetter("deaths"))
        stat = sorted(stat, key=attrgetter("score"), reverse=True)
        sstat = []
        for player in stat:
            sstat.append(("%.1f" % player.score) + " " + str(player.deaths) + " : " + player.name)
        return sstat
        
        #stat.append("Player "+player.name + ": "+str(player.score))

    def roundOver(self):
        #self.__btimer.cancel() # prevent more baubles from being spawned!

        stat = sorted(self.getCurrentPlayers(), key=attrgetter("deaths"))
        stat = sorted(stat, key=attrgetter("score"), reverse=True)

        if not self._tournamentfinalround:
            # get winner
            for x in xrange(self.cfg.getint("KingOfTheBubble", "numtofinalround")):
                logging.info("Adding player to final round %s %d", stat[x].name, stat[x].score)
                self.addPlayerToFinalRound(stat[x])
            #next
        else:
            #TODO: Clean up
            logging.info("Final Round Winner %s %d", stat[0].name, stat[0].score)
            self._tournamentfinalwinner = stat[0]

        super(KingOfTheBubbleGame, self).roundOver()

    def drawInfo(self, surface, flags):
        pass
        #for player in self._players.values():
        #    if player.object != None:
        #        # draw line between player and Bauble
        #        pygame.draw.line(surface, player.color, intpos(player.object.body.position), intpos(self.__baubles[player.netid].body.position))

    def drawGameData(self, screen, flags):
        if self._tournament and self._tournamentinitialized:
            super(KingOfTheBubbleGame, self).drawGameData(screen, flags)
            stat = sorted(self.getCurrentPlayers(), key=attrgetter("deaths"))
            stat = sorted(stat, key=attrgetter("score"), reverse=True)
            x = len(stat) - 1
            for player in stat:                
                screen.blit(self.__dfont.render(("%.1f" % player.score) + " : " + str(player.deaths) + " " + player.name, False, (255, 192, 192)), (screen.get_width()-300, screen.get_height() - 64 - 12*x))
                x -= 1

    def start(self):
        # reset world so bubbles start fresh - TODO: think about how to do this better... (as will reset twice each time now)
        self.resetWorld()
        
        super(KingOfTheBubbleGame, self).start()
        
        # start Bauble Spawn Timer
        #self.newBaubleTimer()    

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

class Bubble(Entity):
    WRAPPERCLASS = BubbleWrapper
    """
    Baubles are small prizes worth different amounts of points
    """
    def __init__(self, pos, basesize, size, speed, time, pname, world):
        super(Bubble, self).__init__(2000, 2, pos)
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
        
    def update(self, t):
        super(Bubble, self).update(t)         
        
        ships = []
        for obj in self.__world.getObjectsInArea(self.body.position, self.size + 28): # add the ship radius so it looks like you get points if you overlap
            if isinstance(obj, Ship):
                ships.append(obj)
        
        for ship in ships:
            ship.player.score += (t * self.pointspeed)
            #logging.info("Player %s getting points %d", ship.player.name, ship.player.score)
        
        self.size -= (t * self.pointspeed * len(ships))
        if self.size < 0:
            self.size = 0
        
        if self.timetoshrink > 0 and self.timealive > self.timetoshrink and len(ships) == 0:
            self.size -= (t * self.pointspeed)
        
        if self.size <= 50.0:
            self.TTL = self.timealive - 1 # schedule this object for removal        

    def getExtraInfo(self, objData):
        objData["VALUE"] = (self.size - self.basesize)
        # Overwrite the 'radius' to show where you can be hit
        objData["HITRADIUS"] = self.size + 28