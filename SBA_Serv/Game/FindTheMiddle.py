from Game import BasicGame, RoundTimer
from World.WorldGenerator import ConfiguredWorld, addObjectAwayFromOthers
from World.Entities import Entity, Ship
from GUI.ObjWrappers.GUIEntity import GUIEntity
from World.WorldMath import intpos, friendly_type, PlayerStat
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

# TODO: Warp out of middle, check velocity is low (i.e. stopped), have target rings, if stopped closer to center = more points

class FindTheMiddleGame(BasicGame):
    
    def __init__(self, cfgobj):
        self.__objectiveradius = cfgobj.getint("FindTheMiddle", "objectiveradius")
        self.__objectivetime = float(cfgobj.getint("FindTheMiddle", "objectivetime"))

        super(FindTheMiddleGame, self).__init__(cfgobj)
                
        self.__highscore = 0

    def createWorld(self, pys=True):
        world = super(FindTheMiddleGame, self).createWorld(pys)
        self.midpoint = (int(world.width / 2), int(world.height / 2))
        return world

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
            for obj in self.world.getObjectsInArea(self.midpoint, self.__objectiveradius + 28): # add the ship radius so it looks like you get points if you overlap
                if isinstance(obj, Ship):
                    ships.append(obj)
        
            for ship in ships:
                ship.player.time += t
                if ship.player.time >= self.__objectivetime:
                    #TODO: warp player
                    ship.player.score += 1
                    ship.player.time = 0

    def drawInfo(self, surface, flags):
        # Draw circle in middle of world        
        pygame.draw.circle(surface, (0, 128, 255), self.midpoint, self.__objectiveradius, 2)

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
        
        # start Bauble Spawn Timer
        #self.newBaubleTimer()    
