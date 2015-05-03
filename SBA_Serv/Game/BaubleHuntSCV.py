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
from GUI.Helpers import debugfont
from ThreadStuff.ThreadSafe import ThreadSafeDict
import logging
import pygame
import random
import thread
from operator import attrgetter

class BaubleHuntSCVGame(BasicGame):
    
    def __init__(self, cfgobj):
        bb = cfgobj.getfloat("BaubleHuntSCV", "bluebaubles")
        yb = cfgobj.getfloat("BaubleHuntSCV", "yellowbaubles")
        rb = cfgobj.getfloat("BaubleHuntSCV", "redbaubles")
        self.__valuetable = [(bb, 1), (bb+yb, 3), (bb+yb+rb, 5)]

        self.__bases = ThreadSafeDict()
        self.__baubles = ThreadSafeDict()
        
        super(BaubleHuntSCVGame, self).__init__(cfgobj)

        self.__highscore = 0
        self.__deathpenalty = self.cfg.getint("BaubleHunt", "deathpenalty")
        self.__maxcarry = self.cfg.getint("BaubleHuntSCV", "maxcarry")

    def GUICFG(self):
        super(BaubleHuntSCVGame, self).GUICFG()

        self.__dfont = debugfont()

    def createWorld(self, pys=True):
        w = ConfiguredWorld(self, self.cfg, pys)
        
        # Add some initial small Baubles
        self.__addBaubles(w, self.cfg.getint("BaubleHunt", "initialbaubles"))

        return w

    def getInitialInfoParameters(self):
        return {"GAMENAME": "BaubleHuntSCV"}

    def registerPlayer(self, name, color, imgindex, netid):
        return super(BaubleHuntSCVGame, self).registerPlayer(name, color, imgindex, netid)

    def playerDisconnected(self, netid):
        if netid in self.__bases:
            logging.info("Removing Player %d Base", netid)
            self.world.remove(self.__bases[netid])
            del self.__bases[netid]
        else:
            logging.info("Trying to remove player %d that was already disconnected?", netid)
        return super(BaubleHuntSCVGame, self).playerDisconnected(netid)

    def resetWorld(self):
        self.__bases = ThreadSafeDict()
        self.__baubles = ThreadSafeDict()
        super(BaubleHuntSCVGame, self).resetWorld()

    # TODO: remove, clean start procedure? Add to start??
    def addPlayerAttributes(self, player):
        player.score = 0
        player.deaths = 0
        player.totalcollected = 0
        player.carrying = []
        player.homebase = None

        return player

    def newRoundForPlayer(self, player):
        super(BaubleHuntSCVGame, self).newRoundForPlayer(player)
        player = self.addPlayerAttributes(player)

        self.__addHomeBase(player)
        self.__addBaubles(self.world, self.cfg.getint("BaubleHunt", "extrabaublesperplayer"))

    def __addHomeBase(self, player, force=False):
        logging.info("Add HomeBase (%s) for Player %d", repr(force), player.netid)
        # add player bauble
        b = HomeBase(self.getHomeBasePosition(), player.object)

        self.__bases[player.netid] = b
        player.homebase = b
        
        self.world.append(b)
        logging.info("Done Adding HomeBase")
        
    # Ignores Baubles
    def getHomeBasePosition(self):       
        pos = (0,0)
        x = 0
        n = 1
        while n > 0 and x < 15:        
            x += 1
            pos = (random.randint(100, self.world.width - 100),
                   random.randint(100, self.world.height - 100))

            objs = self.world.getObjectsInArea(pos, 200)
            for i in xrange(len(objs)-1, -1, -1):
                if isinstance(objs[i], Bauble):
                    del objs[i]
            n = len(objs)
            
        return pos        

    def __addBaubles(self, w, num, force=False):
        logging.info("Adding %d Baubles (%s)", num, repr(force))
        for i in xrange(num):
            r = random.random()
            v = 0
            for ent in self.__valuetable:
                if r < ent[0]:
                    v = ent[1]
                    break
            b = Bauble(getPositionAwayFromOtherObjects(w, 80, 30, force), v)
            if v == 5:
                self.__baubles[b.id] = b
            w.append(b)
        logging.info("Done Adding Baubles")

    def worldObjectPreCollision(self, shapes):
        types = []
        objs = []
        for shape in shapes:
            objs.append(self.world[shape.id])
            types.append(friendly_type(objs[-1]))

        if "Ship" in types and "HomeBase" in types:
            ship = None
            myhome = None
            homes = []
            for obj in objs:
                if isinstance(obj, HomeBase):
                    homes.append(obj)
                elif isinstance(obj, Ship):
                    ship = obj            
            if ship != None:
                logging.info("Ship #%d hit bases %d owner id #%d", ship.id, len(homes), homes[0].owner.id)
                for h in homes:
                    if ship.id == h.owner.id:
                        myhome = h
                        logging.info("Ship #%d hit their base", ship.id)
                        break
                    #eif
                #next
            else:
                logging.error("Ship not found after collision with Ship?")
            #eif
            if myhome != None:
                return [ False, [ [self.depositBaubles, ship, myhome] ] ]
            else:
                logging.info("Ship #%d hit some other base", ship.id)
                return [ False, [] ]            
        if "Ship" in types and "Bauble" in types:
            b = []
            ship = None
            for obj in objs:
                if isinstance(obj, Bauble):
                    b.append(obj)
                elif isinstance(obj, Ship):
                    ship = obj
                #eif
            #next

            return [ False, [ [self.collectBaubles, ship, b] ] ]
        elif "HomeBase" in types or "Bauble" in types:
            return [ False, [] ]
        
        return super(BaubleHuntSCVGame, self).worldObjectPreCollision(shapes)

    def collectBaubles(self, ship, para):
        logging.info("Collected Baubles Ship #%d", ship.id)
        sound = True
        for bauble in para[0]:
            if len(ship.player.carrying) < self.__maxcarry:
                ship.player.carrying.append(bauble)
                if sound:
                    sound = False
                    ship.player.sound = "BAUBLE"

                if self.__baubles.has_key(bauble.id):
                    del self.__baubles[bauble.id]

                self.world.remove(bauble)
                bauble.destroyed = True
                
                self.__addBaubles(self.world, 1, True)
            #eif
        logging.info("Done Collecting Baubles #%d", ship.id)

    def depositBaubles(self, ship, para):
        home = para[0]
        logging.info("Player Depositing Baubles #%d", ship.id)
        for b in ship.player.carrying:
            ship.player.score += b.value
            home.stored += b.value
        ship.player.totalcollected += len(ship.player.carrying)
        
        if len(ship.player.carrying) > 0:
            ship.player.sound = "COLLECT"
            
        ship.player.carrying = []
                
        if ship.player.score > self.__highscore:
            self.__highscore = ship.player.score
            logging.info("New Highscore: %s %d", ship.player.name, self.__highscore)
        
    def worldAddRemoveObject(self, wobj, added):        
        if isinstance(wobj, Ship) and (wobj.disconnected or wobj.killed):
            logging.info("BH Add Object - Ship Disconnected(%s): #%d (%s) [%d]", repr(added), wobj.id, friendly_type(wobj), thread.get_ident())
            if self.__bases.has_key(wobj.player.netid):
                self.world.remove(self.__bases[wobj.player.netid])
                del self.__bases[wobj.player.netid]
            return super(BaubleHuntSCVGame, self).worldAddRemoveObject(wobj, added)               
        if not added and isinstance(wobj, Ship) and wobj.player.netid in self._players:
            logging.info("BH Add Object - Ship Destroyed #%d [%d]", wobj.id, thread.get_ident())
            nid = wobj.player.netid           

            # if ship destroyed, put baubles stored back
            for b in self._players[nid].carrying:
                b.body.position = (self._players[nid].object.body.position[0] + random.randint(-10, 10), self._players[nid].object.body.position[1] + random.randint(-10, 10))
                if b.value == 5:
                    self.__baubles[b.id] = b
                self.world.append(b)
                
            #clear list of carried baubles!
            self._players[nid].carrying = []

            self.world.causeExplosion(self._players[nid].object.body.position, 32, 1000)

            self._players[nid].object = None                     

            self._players[nid].score -= self.__deathpenalty
            self._players[nid].deaths += 1
            if self._players[nid].score < 0:
                self._players[nid].score = 0

            # readd
            newship = self._addShipForPlayer(nid)
            
            if self.__bases.has_key(nid):
                self.__bases[nid].newOwner(newship)

    def getExtraEnvironment(self, player):
        if player.netid in self.__bases: # Check if Player still around?
            v = 0
            for b in player.carrying:
                v += b.value
            baubles = []
            for b in self.__baubles:
                baubles.append(intpos(b.body.position))
            return {"POSITION": intpos(self.__bases[player.netid].body.position), "BAUBLES": baubles,
                    "SCORE": player.score, "HIGHSCORE": self.__highscore, "DEATHS": player.deaths, 
                    "STORED": len(player.carrying), "STOREDVALUE": v, "COLLECTED": player.totalcollected}
        else:
            return {}

    """
    Called by the World when the obj is being radared
    """
    def getExtraRadarInfo(self, obj, objdata):
        super(BaubleHuntSCVGame, self).getExtraRadarInfo(obj, objdata)
        if hasattr(obj, "player"):
            objdata["NUMSTORED"] = len(obj.player.carrying)

    def getPlayerStats(self, current=False):
        if current:
            p = self.getCurrentPlayers() #.itervalues()
        else:
            p = self._players.itervalues()
        #eif
        stat = sorted(p, key=attrgetter("totalcollected"))
        stat = sorted(stat, key=attrgetter("score"), reverse=True)
        sstat = []
        for player in stat:
            sstat.append(str(player.score) + " " + str(player.totalcollected) + " : " + player.name)
        return sstat
        
        #stat.append("Player "+player.name + ": "+str(player.score))

    def roundOver(self):
        logging.info("Round Over")
        self.__btimer.cancel() # prevent more baubles from being spawned!

        stat = sorted(self.getCurrentPlayers(), key=attrgetter("totalcollected"))
        stat = sorted(stat, key=attrgetter("score"), reverse=True)

        if not self._tournamentfinalround:
            # get winner
            for x in xrange(self.cfg.getint("BaubleHunt", "numtofinalround")):
                logging.info("Adding player to final round %s", stat[x].name)
                self.addPlayerToFinalRound(stat[x])
            #next
        else:
            #TODO: Clean up
            logging.info("Final Round Winner %s", stat[0].name)
            self._tournamentfinalwinner = stat[0]

        super(BaubleHuntSCVGame, self).roundOver()

    def drawInfo(self, surface, flags):
        for player in self._players:
            if player.object != None:
                # draw line between player and HomeBase
                text = debugfont().render(repr(len(player.carrying)), False, player.color)
                surface.blit(text, (player.object.body.position[0]+30, player.object.body.position[1]-4))
                if flags["DEBUG"] and self.__bases.has_key(player.netid):
                    pygame.draw.line(surface, player.color, intpos(player.object.body.position), intpos(self.__bases[player.netid].body.position))                

        # draw number of baubles carried by player

    def drawGameData(self, screen, flags):
        if self._tournament and self._tournamentinitialized:
            super(BaubleHuntSCVGame, self).drawGameData(screen, flags)
            stat = sorted(self.getCurrentPlayers(), key=attrgetter("totalcollected"))
            stat = sorted(stat, key=attrgetter("score"), reverse=True)
            x = len(stat) - 1
            for player in stat:                
                screen.blit(self.__dfont.render(str(player.score) + " : " + str(player.totalcollected) + " " + player.name, False, (255, 192, 192)), (screen.get_width()-300, screen.get_height() - 64 - 12*x))
                x -= 1

    def start(self):
        logging.info("Game Start")
        super(BaubleHuntSCVGame, self).start()

        # start Bauble Spawn Timer
        self.newBaubleTimer()    
        
    def newBaubleTimer(self):
        ntime = self.cfg.getint("BaubleHunt", "timefornewbauble")
        if ntime > 0:
            self.__btimer = RoundTimer(ntime, self.spawnBauble)
            self.__btimer.start()

    def spawnBauble(self):
        logging.info("Spawn Bauble Timer [%d]", thread.get_ident())
        self.__addBaubles(self.world, self.cfg.getint("BaubleHunt", "baublesperspawn"))
        
        self.newBaubleTimer()

    """
    def start(self):
        super(BaubleHuntSCVGame, self).start()

        for player in self.getCurrentPlayers():
            player.score = 0
            player.deaths = 0

            self.__addBauble(player)
            self.__addBaubles(self.world, self.cfg.getint("BaubleHunt", "extrabaublesperplayer"))
    """


class BaubleWrapper(GUIEntity):
    def __init__(self, obj, world):
        super(BaubleWrapper, self).__init__(obj, world)
        self.surface = Cache().getImage("Games/Bauble" + str(obj.value))

    def draw(self, surface, flags):
        surface.blit(self.surface, intpos((self._worldobj.body.position[0] - 8, self._worldobj.body.position[1] - 8)))

        super(BaubleWrapper, self).draw(surface, flags)

class Bauble(Entity):
    WRAPPERCLASS = BaubleWrapper
    """
    Baubles are small prizes worth different amounts of points
    """
    def __init__(self, pos, value=1):
        super(Bauble, self).__init__(2000, 8, pos)
        self.shape.elasticity = 0.8
        self.health = PlayerStat(0)

        self.shape.group = 1

        self.value = value

    def getExtraInfo(self, objData):
        objData["VALUE"] = self.value

class HomeBaseWrapper(GUIEntity):
    def __init__(self, obj, world):
        super(HomeBaseWrapper, self).__init__(obj, world)
        self.surface = Cache().getImage("Games/HomeBase")

    def draw(self, surface, flags):
        bp = intpos(self._worldobj.body.position)
        surface.blit(self.surface, (bp[0] - 16, bp[1] - 16))

        # TODO: Owner ID Display

        if flags["NAMES"]:
            # HACK TODO: Ship name should be from team
            text = debugfont().render(self._worldobj.owner.player.name, False, self._worldobj.owner.player.color)
            surface.blit(text, (bp[0]-text.get_width()/2, bp[1]-18))

        if flags["STATS"]:
            text = debugfont().render(repr(self._worldobj.stored), False, self._worldobj.owner.player.color)
            surface.blit(text, (bp[0]-text.get_width()/2, bp[1]+4))

        super(HomeBaseWrapper, self).draw(surface, flags)

class HomeBase(Entity):
    WRAPPERCLASS = HomeBaseWrapper
    """
    Baubles are small prizes worth different amounts of points
    """
    def __init__(self, pos, owner):
        super(HomeBase, self).__init__(2000, 20, pos)
        self.shape.elasticity = 0.8
        self.health = PlayerStat(0)

        self.body.velocity_limit = 0
        
        self.shape.group = 1

        self.owner = owner
        self.stored = 0

    def getExtraInfo(self, objData):
        objData["OWNERID"] = self.owner.id
        
    def newOwner(self, ship):
        self.owner = ship
