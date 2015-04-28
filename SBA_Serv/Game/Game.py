
from World.WorldGenerator import ConfiguredWorld
from World.Entities import Ship, BlackHole
from Players import Player
import random, logging, time
from World.WorldMath import friendly_type
from World.WorldCommands import RaiseShieldsCommand
from threading import Thread
from ThreadStuff.ThreadSafe import ThreadSafeDict
import pygame, thread

class RoundTimer(Thread):
    def __init__(self, seconds, callback):
        self.totalTime = seconds
        self.timeLeft = self.totalTime
        self.__callback = callback
        self.__cancel = False
        Thread.__init__(self)

    def cancel(self):
        self.__cancel = True

    def run(self):
        for sec in xrange(self.totalTime, -1, -1):            
            time.sleep(1.0)
            self.timeLeft = sec
            if self.__cancel:
                return
        self.__callback()

class BasicGame(object):
    """
    Container Class which keeps track of world, teams
    and dictates the game rules in effect
    Handles Delegation between Network on World???
    What allowed Commands in Game Rules?
    """   

    def __init__(self, cfgobj):
        self.cfg = cfgobj
        self.__started = False
        self.world = self.createWorld()
        self.world.registerObjectListener(self.worldAddRemoveObject)   
        self.server = None # set when server created
        self.__teams = ThreadSafeDict()
        self._players = ThreadSafeDict()
        self.__autostart = cfgobj.getboolean("Game", "autostart")
        self.__allowafterstart = cfgobj.getboolean("Game", "allowafterstart")
        self.__allowreentry = cfgobj.getboolean("Game", "allowreentry")
        self.__resetworldround = self.cfg.getboolean("Game", "resetworldeachround")
        self.__disconnectplayersafterround = self.cfg.getboolean("Game", "disconnectplayersafterround")         
        self.__roundtime = cfgobj.getint("Game", "roundtime")
        self.__timer = None
        # TODO: Create Tournament Class
        self._tournament = cfgobj.getboolean("Game", "tournament")
        self._tournamentinitialized = False
        if self._tournament:
            self.__autostart = False
        self._tournamentnumgroups = cfgobj.getint("Game", "tournamentgroups")        
        self._tournamentgroups = []
        self._tournamentcurrentgroup = 0
        self._tournamentfinalgroup = []
        self._tournamentfinalround = False
        self._tournamentfinalwinner = None
        self.laststats = None
        #self.__gamerules = gamerules
        if self.__autostart:
            self.start()

    def GUICFG(self):
        self._tfont = pygame.font.Font("freesansbold.ttf", 18)
            
    def _startRoundTimer(self):
        if self.__roundtime > 0 and self._tournament:
            self.__timer = RoundTimer(self.__roundtime, self.roundOver)
            self.__timer.start()        

    def getRoundTimeRemaining(self):
        if self.__timer == None:
            return 0

        return self.__timer.timeLeft

    def roundOver(self):
        logging.debug("[Game] Round Over")
        
        # Get Stats for only the players in the round
        self.laststats = self.getPlayerStats(current=True)
        
        logging.info("[Game] Stats: %s", repr(self.laststats))
        
        self.__timer = None
        for player in self._players:
            player.roundover = True
            if player.object != None:
                player.object.killed = True            
                self.world.remove(player.object)

        if self.__resetworldround:
            self.resetWorld()

        # overwritten by allowafterstart
        self.__autostart = self.cfg.getboolean("Game", "autostart")
        # TODO: figure out a better way to tie these together
        if self._tournament:
            self.__autostart = False
            self._tournamentcurrentgroup += 1
            logging.debug("[Tournament] Group Number Now %d", self._tournamentcurrentgroup)
        if not self.__autostart:
            # If not autostart, wait for next round to start
            self.__started = False
        else:
            self.start()

    """
    Called by constructor to create world
    """
    def createWorld(self, pys=True):
        return ConfiguredWorld(self, self.cfg, pys)

    """
    Recreates a world...?
    """
    def resetWorld(self):
        # Remove All Objects
        #for obj in self.world:
        #    self.world.remove(obj)

        # Create new world
        #self.world = None
        #self.world = self.createWorld()
        #self.world.registerObjectListener(self.worldAddRemoveObject)
        self.world.newWorld(self.createWorld(False))

        # Copy objects from new world to original world
        #objlist = []
        #for obj in w:
        #    objlist.append(obj)

        #for obj in objlist:
        #    w.remove(obj) # need to remove object from space before adding to another
        #    self.world.append(obj)

        #w = None

    """
    Returns True when game has started
    """
    def hasStarted(self):
        return self.__started    

    # Called when a client is connected and appends this data to the default image number, world width and world height
    # Should at least return a key "GAMENAME" with the name of the game module
    def getInitialInfoParameters(self):
        return {"GAMENAME": "Basic"}    

    """
    Called by GUI to display Player Info
    """
    def getPlayerStats(self, current=False):
        if current:
            p = self._players
        else:
            p = self.getCurrentPlayers()
        #eif
        stat = []
        for player in p:
            stat.append("Player "+player.name)
        return stat

    """
    Called by the server when a new client registration message is received
    Has all information pertaining to a player entity
    """
    def registerPlayer(self, name, color, imgindex, netid):        
        if not self._players.has_key(netid):
            if (self.__started and self.__allowafterstart) or not self.__started:
                # create new player
                #
                p = Player(name, color, imgindex, netid, None)
                p = self.addPlayerAttributes(p)
                self._players[netid] = p

                if self.__autostart:
                    self._addShipForPlayer(netid, roundstart=True)                                   

                logging.info("Registering Player: %s %d", name, netid)
                    
                return True

        return False

    """
    Called by registerPlayer and newRoundForPlayer to add custom attributes to players for games
    """
    def addPlayerAttributes(self, player):
        return player

    """
    Called by the server when a disconnect message is received by a player's client
    """
    def playerDisconnected(self, netid):        
        for player in self._players:
            if player.netid == netid and player.object != None:
                logging.debug("Player %s Disconnected", player.name)
                player.object.disconnected = True
                self.world.remove(player.object)
                player.object = None

                if self.__allowreentry:
                    if self._players.has_key(player.netid):
                        del self._players[player.netid] # should be handled by world part
                    return True

        logging.debug("Couldn't find player with netid %d to disconnect", netid);
        return False

    """
    Called by world when a ship is destroyed
    """
    def worldAddRemoveObject(self, wobj, added):
        logging.debug("[Game] Add Object(%s): #%d (%s)", repr(added), wobj.id, friendly_type(wobj))
        if not added and isinstance(wobj, Ship) and wobj.player.netid in self._players:
            nid = wobj.player.netid

            self._players[nid].object = None                     

            r = self._players[nid].roundover

            if not r or (r and self.__disconnectplayersafterround):
                if self.__allowreentry:
                    del self._players[nid]

                self.server.sendDisconnect(nid)

    """
    Called by the physics engine when two objects just touch

    return [T/F, [[func, obj, para...]... ] ]

    return False to not process collision
    """
    def worldObjectPreCollision(self, shapes):
        for shape in shapes:
            if isinstance(self.world[shape.id], BlackHole):
                return [ False, [] ]                

    """
    Called by the physics engine when two objects collide

    Return [[func, obj, para...]...]
    """
    def worldObjectCollision(self, shapes, damage):
        r = []
        for shape in shapes:
            #print shape.id, ":",
            gobj = self.world[shape.id]
            if isinstance(gobj, Ship) and gobj.commandQueue.containstype(RaiseShieldsCommand) and gobj.shield.value > 0:
                gobj.shield -= damage * gobj.shieldDamageReduction
                gobj.health -= damage * (1.0 - gobj.shieldDamageReduction)
            else:
                gobj.health -= damage
            #eif

            if gobj.health.maximum > 0 and gobj.health.value <= 0:
                gobj.killedby = None
                r.append([self.worldObjectAfterCollision, gobj, damage])
                if len(shapes) == 2:
                    for s2 in shapes:
                        if s2 != shape:
                            gobj.killedby = self.world[s2.id]
                            break
                #space.add_post_step_callback(self.worldObjectAfterCollision, gobj, damage)
                if isinstance(gobj, Ship):
                    gobj.player.sound = "EXPLODE"
            elif isinstance(gobj, Ship):
                gobj.player.sound = "HIT"
            #eif
        if r == []: return None
        return r

    def worldObjectAfterCollision(self, dobj, para):
        strength = para[0] / 75.0
        logging.info("Destroying Object: #%d, Force: %d [%d]", dobj.id, strength, thread.get_ident())
        dobj.destroyed = True

        self.world.causeExplosion(dobj.body.position, dobj.radius * 5, strength / 75.0, True) #Force in physics step

        self.world.remove(dobj)

    # returns true if the game already has a player with this name
    def hasPlayer(self, name):
        for player in self._players.values():
            if player.name == name:
                return True 

        return False    
    
    def getPlayerByNetId(self, netid):
        return self._players[netid]    

    """
    Called internally when a player registers if autostart is true, or when start is called

    Also, sends initial environment to start RPC loop with client
    """
    def _addShipForPlayer(self, netid, force=False, roundstart=False):        
        self._players[netid].object = Ship(self.getPlayerStartPosition(True), self.world)        
        logging.info("Adding Ship for Player %d (%s) id #%d with Name %s", netid, repr(force), self._players[netid].object.id, self._players[netid].name)
        self._players[netid].object.player = self._players[netid]
        self._players[netid].roundover = False

        if not self.cfg.getboolean("Game", "collisions"):
            self._players[netid].object.shape.group = 1

        if roundstart:
            self.newRoundForPlayer(self._players[netid])

        self.world.append(self._players[netid].object)

        logging.info("Sending New Ship #%d Environment Info", self._players[netid].object.id)
        if not self._players[netid].waiting:
            self.server.sendEnvironment(self._players[netid].object, netid)
        return self._players[netid].object

    """
    Called when a new ship is added to the world for the first time as the round starts
    It will have been created, but not added to the physics world yet, so no callback about it being added will have occured.
    """
    def newRoundForPlayer(self, player):
        return self.addPlayerAttributes(player)

    """
    Figures out where a random player should start in the world
    """
    def getPlayerStartPosition(self, force=False):
        pos = (random.randint(100, self.world.width - 100),
               random.randint(100, self.world.height - 100))
        x = 0
        while len(self.world.getObjectsInArea(pos, 150)) > 0 and x < 15:
            x += 1
            pos = (random.randint(100, self.world.width - 100),
                   random.randint(100, self.world.height - 100))
        return pos

    """
    Called by GUI client to start a synchronized game start
    """
    def start(self):
        if not self.__started:
            logging.info("Starting Game")
            self.__started = True
            self.__autostart = self.__allowafterstart

            if self._tournament:
                logging.info("[Tournament] Round %d of %d", self._tournamentcurrentgroup+1, self._tournamentnumgroups)
                if not self._tournamentinitialized:
                    logging.info("[Tournament] Initialized with %d players", len(self._players))
                    self._tournamentgroups = []
                    for x in xrange(self._tournamentnumgroups):
                        self._tournamentgroups.append([])
                    #next
                    x = 0
                    for player in self._players.values():
                        self._tournamentgroups[x % self._tournamentnumgroups].append(player)
                        x += 1
                    #next               
                    self._tournamentinitialized = True                     
                elif self._tournamentcurrentgroup == self._tournamentnumgroups:
                    logging.info("[Tournament] Final Round")
                    self._tournamentfinalround = True
                #eif
            #eif

            for player in self.getCurrentPlayers():
                self._addShipForPlayer(player.netid, roundstart = True)
            #next

            self._startRoundTimer()       
            
    """
    Returns a list of player objects for players in the current round
    Returns all players if no tournament running
    """
    def getCurrentPlayers(self):
        if self._tournament:
            if self._tournamentfinalround:
                return self._tournamentfinalgroup
            else:
                if self._tournamentcurrentgroup < len(self._tournamentgroups):
                    return self._tournamentgroups[self._tournamentcurrentgroup]
                else:
                    return []
            #eif
        else:
            return self._players
        #eif

    def addPlayerToFinalRound(self, player):
        self._tournamentfinalgroup.append(player)

    """
    Called by World to return extra environment info to a player when they need to return a command (for just that player)
    """
    def getExtraEnvironment(self, player):
        pass

    """
    Called by the World when the obj is being radared
    """
    def getExtraRadarInfo(self, obj, objdata):
        if hasattr(obj, "player") and self.cfg.getboolean("Game", "radarname"):
            objdata["NAME"] = obj.player.name

    """
    Called by the World to notify the passage of time

    Note: This is called from the core game loop, best not to delay much here
    """
    def update(self, t):
        pass

    """
    Called by GUI to have game draw additional info on screen
    (related to the game world)
    """
    def drawInfo(self, surface, flags):
        pass                

    """
    Called by GUI to draw info about the round/tournament
    (related to the screen)
    """
    def drawGameData(self, screen, flags):
        if self._tournament and self._tournamentinitialized:
            # draw first Bracket
            y = 100
            for x in xrange(self._tournamentnumgroups):
                c = (128, 128, 128)
                if x == self._tournamentcurrentgroup:
                    c = (255, 255, 255)
                py = y
                for player in self._tournamentgroups[x]:
                    screen.blit(self._tfont.render(player.name, False, c), (100, y))
                    y += 24
                                
                # draw bracket lines
                pygame.draw.line(screen, (192, 192, 192), (400, py), (410, py))
                pygame.draw.line(screen, (192, 192, 192), (410, py), (410, y))
                pygame.draw.line(screen, (192, 192, 192), (400, y), (410, y))
                pygame.draw.line(screen, (192, 192, 192), (410, py + (y - py) / 2), (410, py + (y - py) / 2))
                                
                y += 36

            # draw Final Bracket
            y = 96 + ((y - 96) / 2) - len(self._tournamentfinalgroup) * 16
            py = y
            for player in self._tournamentfinalgroup:
                screen.blit(self._tfont.render(player.name, False, (255, 255, 128)), (435, y))
                y += 24
            pygame.draw.line(screen, (192, 192, 192), (800, py), (810, py))
            pygame.draw.line(screen, (192, 192, 192), (810, py), (810, y))
            pygame.draw.line(screen, (192, 192, 192), (800, y), (810, y))

            if self._tournamentfinalwinner:
                screen.blit(self._tfont.render(self._tournamentfinalwinner.name, False, (128, 255, 255)), (835, py + (y - py) / 2))
        #eif

# COMMAND - GAME COMMANDS?
    # COMMAND LIMITS (Thrusting, Energy, Temporary, Aux...)

# IN RANGE

# EXTRA SHIP HUD?

# LEADER BOARD?
