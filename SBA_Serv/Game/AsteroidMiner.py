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
from World.WorldEntities import Ship, Asteroid, Torpedo
from GUI.ObjWrappers.GUIEntity import GUIEntity
from World.WorldMath import intpos, friendly_type, PlayerStat
from GUI.GraphicsCache import Cache
from GUI.Helpers import debugfont
import logging
import pygame
from operator import attrgetter

class AsteroidMinerGame(BasicGame):
    
    def __init__(self, cfgobj):
        super(AsteroidMinerGame, self).__init__(cfgobj)

        self.__highscore = 0
        self.__deathpenalty = self.cfg.getint("AsteroidMiner", "deathpenalty")
        self.__torpedopoints = self.cfg.getint("AsteroidMiner", "torpedopoints")
        self.__shippoints = self.cfg.getint("AsteroidMiner", "shippoints")

    def GUICFG(self):
        super(AsteroidMinerGame, self).GUICFG()

        self.__dfont = debugfont()

    def createWorld(self, pys=True):
        w = ConfiguredWorld(self, self.cfg, pys)
        
        return w

    def registerPlayer(self, name, color, imgindex, netid):
        return super(AsteroidMinerGame, self).registerPlayer(name, color, imgindex, netid)

    # TODO: remove, clean start procedure? Add to start??
    def addPlayerAttributes(self, player):
        player.score = 0
        player.deaths = 0

        return player

    def newRoundForPlayer(self, player):
        super(AsteroidMinerGame, self).newRoundForPlayer(player)
        player.score = 0
        player.deaths = 0

        self.__addAsteroid()

    def __addAsteroid(self, force=False):
        logging.info("Add Asteroid (%s)", repr(force))
        # add player bauble
        self.world.append(Asteroid(getPositionAwayFromOtherObjects(self.world, 80, 30, force)))

        logging.info("Done Adding Asteroid")

    def __addAsteroids(self, w, num, force=False):
        logging.info("Adding %d Asteroids (%s)", num, repr(force))
        for i in xrange(num):
            w.append(Asteroid(getPositionAwayFromOtherObjects(w, 100, 30, force)))
        logging.info("Done Adding Asteroids")

    """
    def worldObjectPreCollision(self, shapes):
        types = []
        objs = []
        for shape in shapes:
            objs.append(self.world[shape.id])
            types.append(friendly_type(objs[-1]))
        
        if "Asteroid" in types and "Torpedo" in types:
            b = []
            ship = None
            for i in xrange(len(objs)-1, -1, -1):
                if isinstance(objs[i], Asteroid):
                    b.append(objs[i])
                    del objs[i]
                elif isinstance(objs[i], Torpedo):
                    ship = objs[i]

            return [ True, [ [self.checkAsteroid, ship, b] ] ]

    def checkAsteroid(self, torpedo, para):
        logging.info("checkAsteroid Torpedo #%d", torpedo.id)
        for ast in para[0]:
            if ast.destroyed:
                torpedo.owner.player.score += 1

                # add new asteroid
                self.__addAsteroid(True)
            #eif
        if torpedo.owner.player.score > self.__highscore:
            self.__highscore = torpedo.owner.player.score
        logging.info("Done checkAsteroid #%d", torpedo.id)            
        
    """

    def worldAddRemoveObject(self, wobj, added):
        logging.debug("BH Add Object(%s): #%d (%s)", repr(added), wobj.id, friendly_type(wobj))
        if not added and isinstance(wobj, Asteroid) and wobj.killedby != None:
            obj = wobj.killedby
            if isinstance(obj, Torpedo):
                obj.owner.player.score += self.__torpedopoints
                if obj.owner.player.score > self.__highscore:
                    self.__highscore = obj.owner.player.score
                    
                logging.info("Torpedo Owner (#%d) Destroyed Asteroid", obj.owner.id)
            elif isinstance(obj, Ship) and obj.health.value > 0:
                obj.player.score += self.__shippoints
                if obj.player.score > self.__highscore:
                    self.__highscore = obj.player.score
                    
                logging.info("Ship (#%d) Destroyed Asteroid", obj.id)
                
        if isinstance(wobj, Ship) and (wobj.disconnected or wobj.killed):
            return super(AsteroidMinerGame, self).worldAddRemoveObject(wobj, added)               
        if not added and isinstance(wobj, Ship) and wobj.player.netid in self._players:
            nid = wobj.player.netid

            self._players[nid].object = None                     

            self._players[nid].score -= self.__deathpenalty
            self._players[nid].deaths += 1
            if self._players[nid].score < 0:
                self._players[nid].score = 0

            # readd
            self._addShipForPlayer(nid, True)

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
            sstat.append(str(player.score) + " " + str(player.deaths) + " : " + player.name)
        return sstat
        
        #stat.append("Player "+player.name + ": "+str(player.score))

    def roundOver(self):
        self.__btimer.cancel() # prevent more baubles from being spawned!

        stat = sorted(self.getCurrentPlayers(), key=attrgetter("deaths"))
        stat = sorted(stat, key=attrgetter("score"), reverse=True)

        if not self._tournamentfinalround:
            # get winner
            for x in xrange(self.cfg.getint("AsteroidMiner", "numtofinalround")):
                logging.info("Adding player to final round %s", stat[x].name)
                self.addPlayerToFinalRound(stat[x])
            #next
        else:
            #TODO: Clean up
            logging.info("Final Round Winner %s", stat[0].name)
            self._tournamentfinalwinner = stat[0]

        super(AsteroidMinerGame, self).roundOver()

    def drawInfo(self, surface, flags):
        pass

    def drawGameData(self, screen, flags):
        if self._tournament and self._tournamentinitialized:
            super(AsteroidMinerGame, self).drawGameData(screen, flags)
            stat = sorted(self.getCurrentPlayers(), key=attrgetter("deaths"))
            stat = sorted(stat, key=attrgetter("score"), reverse=True)
            x = len(stat) - 1
            for player in stat:                
                screen.blit(self.__dfont.render(str(player.score) + " : " + str(player.deaths) + " " + player.name, False, (255, 192, 192)), (screen.get_width()-300, screen.get_height() - 64 - 12*x))
                x -= 1

    def start(self):
        super(AsteroidMinerGame, self).start()

        # start Bauble Spawn Timer
        self.newAsteroidTimer()    
        
    def newAsteroidTimer(self):
        self.__btimer = RoundTimer(self.cfg.getint("AsteroidMiner", "timefornewasteroid"), self.spawnAsteroid)
        self.__btimer.start()

    def spawnAsteroid(self):
        self.__addAsteroids(self.world, self.cfg.getint("AsteroidMiner", "asteroidsperspawn"))
        
        self.newAsteroidTimer()