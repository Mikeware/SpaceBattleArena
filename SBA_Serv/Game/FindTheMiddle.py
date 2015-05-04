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
from World.Entities import Entity
from World.WorldEntities import Ship
from GUI.ObjWrappers.GUIEntity import GUIEntity
from World.WorldMath import intpos, friendly_type, PlayerStat, in_circle
from GUI.GraphicsCache import Cache
from GUI.Helpers import debugfont, wrapcircle, namefont
import logging, random
import pygame
from operator import attrgetter

# Basic Game - Find The Middle
# Preliminary Exercise to introduce students to the world of Space Battle
# 
# Creates a circle in the middle of the world
# Students must create a ship to navigate to the center of the world
# Once there for a sufficient amount of time, they will be warped away, and must try again

class FindTheMiddleGame(BasicGame):
    
    def __init__(self, cfgobj):
        self.__objectiveradii = eval(cfgobj.get("FindTheMiddle", "objectiveradii"))
        self.__objectivepoints = eval(cfgobj.get("FindTheMiddle", "objectivepoints"))
        self.__objectivetime = float(cfgobj.getint("FindTheMiddle", "objectivetime"))
        self.__objectivevelocity = cfgobj.getint("FindTheMiddle", "objectivevelocity")

        super(FindTheMiddleGame, self).__init__(cfgobj)
                
        self.__highscore = 0

    def createWorld(self, pys=True):
        world = super(FindTheMiddleGame, self).createWorld(pys)
        self.midpoint = (int(world.width / 2), int(world.height / 2))
        return world
    
    def getPlayerStartPosition(self, force=False):
        # make sure player doesn't spawn in middle
        pos = (random.randint(50, self.world.width - 50),
               random.randint(50, self.world.height - 50))
        x = 0
        while (len(self.world.getObjectsInArea(pos, 75)) > 0 or in_circle(self.midpoint, self.__objectiveradii[-1], pos)) and x < 15:
            x += 1
            pos = (random.randint(50, self.world.width - 50),
                   random.randint(50, self.world.height - 50))
        return pos

    def GUICFG(self):
        super(FindTheMiddleGame, self).GUICFG()

        self.__dfont = debugfont()

    def addPlayerAttributes(self, player):
        player.score = 0
        player.time = 0
        player.deaths = 0

        return player

    def worldAddRemoveObject(self, wobj, added):
        logging.debug("BH Add Object(%s): #%d (%s)", repr(added), wobj.id, friendly_type(wobj))
        if not added and isinstance(wobj, Ship) and wobj.player.netid in self._players:
            nid = wobj.player.netid
            self._players[nid].deaths += 1

        return super(FindTheMiddleGame, self).worldAddRemoveObject(wobj, added)
        
    def getExtraEnvironment(self, player):
        return {"SCORE": player.score, "HIGHSCORE": self.__highscore, "DEATHS": player.deaths}
        
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

        super(FindTheMiddleGame, self).roundOver()

    def update(self, t):
        if self.hasStarted():
            ships = []
            for obj in self.world.getObjectsInArea(self.midpoint, self.__objectiveradii[-1] + 28): # add the ship radius so it looks like you get points if you overlap
                if isinstance(obj, Ship):
                    ships.append(obj)
        
            for ship in ships:
                if ship.body.velocity.length < self.__objectivevelocity:
                    ship.player.time += t
                    if ship.player.time >= self.__objectivetime:
                        x = 0
                        for radius in self.__objectiveradii:
                            if in_circle(self.midpoint, radius + 28, ship.body.position):                                
                                break
                            x += 1
                        ship.body.position = self.getPlayerStartPosition()
                        ship.player.score += self.__objectivepoints[x]
                        ship.player.time = 0

    def drawInfo(self, surface, flags):
        # Draw circles in middle of world
        x = 1
        inc = int(255 / len(self.__objectiveradii))
        for radius in self.__objectiveradii:
            pygame.draw.circle(surface, (0, inc * x, 255 - inc * x), self.midpoint, radius, len(self.__objectiveradii) - x + 1)
            text = debugfont().render(repr(self.__objectivepoints[x-1]) + " Points", False, (128, 128, 128))
            surface.blit(text, (self.midpoint[0]-text.get_width()/2, self.midpoint[1]-radius+18))
            x += 1

        for player in self._players.values():
            if player.object != None and player.time > 0:
                # draw time left in bubble
                text = debugfont().render("%.1f" % (self.__objectivetime - player.time), False, player.color)
                surface.blit(text, (player.object.body.position[0]+30, player.object.body.position[1]-4))

    def drawGameData(self, screen, flags):
        if self._tournament and self._tournamentinitialized:
            super(FindTheMiddleGame, self).drawGameData(screen, flags)
            stat = sorted(self.getCurrentPlayers(), key=attrgetter("deaths"))
            stat = sorted(stat, key=attrgetter("score"), reverse=True)
            x = len(stat) - 1
            for player in stat:                
                screen.blit(self.__dfont.render(("%.1f" % player.score) + " : " + str(player.deaths) + " " + player.name, False, (255, 192, 192)), (screen.get_width()-300, screen.get_height() - 64 - 12*x))
                x -= 1

    def start(self):
        # reset world so bubbles start fresh - TODO: think about how to do this better... (as will reset twice each time now)
        self.resetWorld()
        
        super(FindTheMiddleGame, self).start()
