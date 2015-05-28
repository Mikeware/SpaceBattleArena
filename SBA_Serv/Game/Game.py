"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2015 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from World.WorldGenerator import ConfiguredWorld
from World.WorldEntities import Ship, BlackHole, Nebula
from Players import Player
import random, logging, time
from World.WorldMath import friendly_type
from World.WorldCommands import RaiseShieldsCommand
from threading import Thread
from ThreadStuff.ThreadSafe import ThreadSafeDict
import pygame, thread
from pymunk import Vec2d
from GUI.Helpers import debugfont
from operator import attrgetter

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
    The BasicGame defines all notions of the basic mechanics of Space Battle as well as an infrastructure to build upon.

    The BasicGame provides information about a player's 'score', 'bestscore', 'deaths' by default.
    It also keeps track of the 'highscore' in a variety of manners and can run a tournament to advance players to a final round.

    Public Attributes:
        world: world object
        server: server object
        laststats: previous rounds scores

    Protected Attributes:
        _players: dictionary of players keyed by their network id (player.netid)
        _tournament: boolean True if playing tournament
        _tournamentinitialized: boolean True if tournament has been setup
        _highscore: current highscore of the game based on primary_victory_attr
        _leader: current leader of the game
    """
    _ADD_REASON_REGISTER_ = 0
    _ADD_REASON_START_ = 1
    _ADD_REASON_RESPAWN_ = 2

    def __init__(self, cfgobj):
        self.cfg = cfgobj
        self.__started = False

        # Load Config
        self.__autostart = cfgobj.getboolean("Game", "auto_start")
        self.__allowafterstart = cfgobj.getboolean("Game", "allow_after_start")
        self.__allowreentry = cfgobj.getboolean("Server", "allow_re-entry")
        self.__resetworldround = self.cfg.getboolean("Tournament", "reset_world_each_round")
        self.__roundtime = cfgobj.getint("Tournament", "round_time")

        self._disconnect_on_death = cfgobj.getboolean("Game", "disconnect_on_death")
        self._reset_score_on_death = cfgobj.getboolean("Game", "reset_score_on_death")
        self._points_lost_on_death = cfgobj.getint("Game", "points_lost_on_death")
        self._points_initial = cfgobj.getint("Game", "points_initial")        

        self._primary_victory = cfgobj.get("Game", "primary_victory_attr")
        self._primary_victory_high = cfgobj.getboolean("Game", "primary_victory_highest")

        self._secondary_victory = cfgobj.get("Game", "secondary_victory_attr")
        self._secondary_victory_high = cfgobj.getboolean("Game", "secondary_victory_highest")     
        
        # TODO: Create Tournament Class
        self._tournament = cfgobj.getboolean("Tournament", "tournament")
        self._tournamentinitialized = False
        if self._tournament:
            self.__autostart = False
        else:
            self.__roundtime = 0 # don't want to return a big round time set in a config, if it's not used.
        self._tournamentnumgroups = cfgobj.getint("Tournament", "tournament_groups")        
        self._tournamentgroups = []
        self._tournamentcurrentgroup = 0
        self._tournamentfinalgroup = []
        self._tournamentfinalround = False
        self._tournamentfinalwinner = None
        self.laststats = None
        self._highscore = 0 # highest score achieved during game
        self._leader = None # player object of who's in lead

        self.server = None # set when server created
        self.__teams = ThreadSafeDict()
        self._players = ThreadSafeDict()
        self.__aiships = ThreadSafeDict()
        self.__timer = None
        
        self.__leaderboard_cache = self.game_get_current_player_list()

        # Load World
        self.world = self.world_create()
        self.world.registerObjectListener(self.world_add_remove_object)   

        if self.__autostart:
            self.round_start()
            
    def end(self):
        """
        Called when exiting GUI to terminate game.
        """
        logging.info("Ending Game")
        self._tournament = True # force it to not restart timers again
        self.round_over()

        logging.info("Ending World")
        self.world.endGameLoop()

    #region Round/Timing Functions
    def _round_start_timer(self):
        """
        Called automatically by round_start.
        """
        if self.__roundtime > 0 and self._tournament:
            self.__timer = RoundTimer(self.__roundtime, self.round_over)
            self.__timer.start()        

    def round_get_time_remaining(self):
        """
        Returns the amount of time remaining in a tournament round or zero
        """
        if self.__timer == None:
            return 0

        return self.__timer.timeLeft

    def round_start(self):
        """
        Called by GUI client to start a synchronized game start, or automatically when the game is initialized if auto_start = true

        Called every time a new round starts or once if a tournament is not being played.
        """
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
            

                # we'll reset the world here so it's "fresh" and ready as soon as the game starts
                if self.__resetworldround:
                    self._world_reset()
            #eif

            for player in self.game_get_current_player_list():
                self._game_add_ship_for_player(player.netid, roundstart=True)
            #next

            self._round_start_timer()   

    
    def player_added(self, player, reason):
        """
        player_added is called in three separate cases
            0) When the server first registers a ship on the server and adds them to the game
            1) When a round starts and a player is added to the game round
            2) When a player dies and is respawned in the world.
            
        cases 0 and 1 may occur one after another if auto_start is set to true. 

        The ship object will have been created, but not added to the physics world yet, so no callback to world_add_remove_object may have occured yet.
        This is also before any commands are requested for the player (i.e. before the first environment is sent).

        You should add and initialize any new properties that you want on a player here.

        Reason values:
        _ADD_REASON_REGISTER_ = 0
        _ADD_REASON_START_ = 1
        _ADD_REASON_RESPAWN_ = 2

        Analog to player_died
        """
        if reason == 1:
            player.score = self._points_initial
            player.bestscore = self._points_initial
            player.deaths = 0

    
    def player_get_start_position(self, force=False):
        """
        Should return a position for a player to start at in the world.
        """
        pos = (random.randint(100, self.world.width - 100),
               random.randint(100, self.world.height - 100))
        x = 0
        while len(self.world.getObjectsInArea(pos, 150)) > 0 and x < 15:
            x += 1
            pos = (random.randint(100, self.world.width - 100),
                   random.randint(100, self.world.height - 100))
        return pos

    def round_over(self):
        """
        Called in a tournament when the round time expires.
        Will automatically advance the top players to the next round.
        """
        if self.__timer != None:
            self.__timer.cancel() # if we get a round-over prematurely or do to some other condition, we should cancel this current timer
            self.__timer = None

        logging.debug("[Game] Round Over")
        self.game_update(0) # make sure we do one last update to sync and refresh the leaderboard cache
        
        # Get Stats for only the players in the round
        self.laststats = self.gui_get_player_stats()

        logging.info("[Game] Stats: %s", repr(self.laststats))

        if len(self.laststats) > 0:
            if not self._tournamentfinalround:
                # get winner(s)
                for x in xrange(self.cfg.getint("Tournament", "number_to_final_round")):
                    logging.info("Adding player to final round %s stats: %s", self.__leaderboard_cache[x].name, self.laststats[x])
                    self._player_add_to_final_round(self.__leaderboard_cache[x])
                #next
            else:
                logging.info("Final Round Winner %s stats: %s", self._leader.name, self.laststats[0])
                self._tournamentfinalwinner = self._leader
            #eif
        #eif
        
        for player in self._players:
            player.roundover = True
            if player.object != None:
                #player.object.destroyed = True
                self.world.remove(player.object) # here we're forcibly removing them as we're clearing the game

        # overwritten by allowafterstart
        self.__autostart = self.cfg.getboolean("Game", "auto_start")
        # TODO: figure out a better way to tie these together
        if self._tournament:
            self.__autostart = False
            self._tournamentcurrentgroup += 1
            logging.debug("[Tournament] Group Number Now %d", self._tournamentcurrentgroup)
        if not self.__autostart:
            # If not autostart, wait for next round to start
            self.__started = False
        else:
            self.round_start()

    def world_create(self, pys=True):
        """
        Called by constructor to create world and when world reset, defaults to the standard world configuration from the config file definitions.
        """
        return ConfiguredWorld(self, self.cfg, pys, objlistener=self.world_add_remove_object)
    
    def _world_reset(self):
        """
        Recreates a world, called when the reset_world_each_round property is set.
        """
        self.world.newWorld(self.world_create(False))

    def round_get_has_started(self):
        """
        Returns True when game has started.
        """
        return self.__started    

    def game_update(self, t):
        """
        Called by the World to notify the passage of time

        The default game uses this update to cache the current leaderboard to be used by the GUI and the game to determine the leader info to send out.

        Note: This is called from the core game loop, best not to delay much here
        """
        self.__leaderboard_cache = sorted(sorted(self.game_get_current_player_list(), key=attrgetter(self._secondary_victory), reverse=self._secondary_victory_high), 
                                          key=attrgetter(self._primary_victory), reverse=self._primary_victory_high)
        if len(self.__leaderboard_cache) > 0:
            self._leader = self.__leaderboard_cache[0]
            self._highscore = getattr(self._leader, self._primary_victory)
        #eif
    #endregion
    
    #region Network driven functions
    def server_register_player(self, name, color, imgindex, netid, aiship=None):
        """
        Called by the server when a new client registration message is received
        Has all information pertaining to a player entity

        Parameters:
            ship: Ship object - used to register AI Ships to the game world
        """
        if not self._players.has_key(netid):
            if (self.__started and self.__allowafterstart) or not self.__started:
                # create new player
                #
                p = Player(name, color, imgindex, netid, None)
                self.player_added(p, BasicGame._ADD_REASON_REGISTER_)
                self._players[netid] = p

                if aiship != None:
                    self.__aiships[netid] = aiship
                
                if self.__autostart:
                    self._game_add_ship_for_player(netid, roundstart=True)

                logging.info("Registering Player: %s %d", name, netid)
                    
                return True

        return False

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
        pass

    def server_process_command(self, ship, command):
        """
        Called by the server after a Command object has been formed from a network message.
        This includes the command processed by a game in server_process_network_message.
        This function would allow the game to interact with the built-in commands.

        Parameters:
            ship: Ship object to process this command
            command: Command object that will be added to the ship's computer by the server

        Return:
            This method should return the command or a string indicating an error.
            Returning None would cause a silent failure on the client.
            In the case of a string, the message would be printed out in the client console.
            In both error cases, another standard request for a command is made on the client.
        """
        return command

    def _game_add_ship_for_player(self, netid, force=False, roundstart=False):
        """
        Called internally when a player registers if autostart is true, or when round_start is called
        Also called when a player respawns.

        Look to override player_added instead.

        Also, sends initial environment to start RPC loop with client
        """
        if netid < -2: # AI Ship
            self._players[netid].object = self.__aiships[netid]
            # reset AI Ship to look like new ship, though reuse object 
            # TODO: this doesn't work, need 'new' object to add to world, or queue the add to occur after the remove...boo
            self.__aiships[netid].health.full()
            self.__aiships[netid].energy.full()
            self.__aiships[netid].shield.full()
            self.__aiships[netid].destroyed = False
            self.__aiships[netid].killed = False
            self.__aiships[netid].timealive = 0
            self.__aiships[netid].body.velocity = Vec2d(0, 0)
            if not roundstart: # ai ship will be initialized with a starting position for round entry, but if killed, will randomize
                self.__aiships[netid].body.position = self.player_get_start_position(True)

            self._players[netid].object.ship_added() # tell AI ship to start
        else:
            self._players[netid].object = Ship(self.player_get_start_position(True), self.world)
        logging.info("Adding Ship for Player %d (%s) id #%d with Name %s", netid, repr(force), self._players[netid].object.id, self._players[netid].name)
        self._players[netid].object.player = self._players[netid]
        self._players[netid].object.owner = self._players[netid].object # Make ships owners of themselves for easier logic with ownership?
        self._players[netid].roundover = False

        if not self.cfg.getboolean("World", "collisions"):
            self._players[netid].object.shape.group = 1

        if roundstart:
            self.player_added(self._players[netid], BasicGame._ADD_REASON_START_)
        else:
            self.player_added(self._players[netid], BasicGame._ADD_REASON_RESPAWN_)
        #eif

        self.world.append(self._players[netid].object)

        logging.info("Sending New Ship #%d Environment Info", self._players[netid].object.id)
        if netid >= 0 and not self._players[netid].waiting:
            self.server.sendEnvironment(self._players[netid].object, netid)
        return self._players[netid].object
    
    def game_get_info(self):
        """
        Called when a client is connected and appends this data to the default image number, world width and world height
        Should at least return a key "GAMENAME" with the name of the game module.

        Your game name should be "Basic" if you don't want to return anything in game_get_extra_environment to the player
            besides Score, Bestscore, Deaths, Highscore, Time left, and Round time.

        Note: The client doesn't expose a way to get anything besides the game name right now.
        """
        return {"GAMENAME": "Basic"}    
    
    def game_get_extra_environment(self, player):
        """
        Called by World to return extra environment info to a player when they need to return a command (for just that player).

        If you desire to return more information to the client, you can create an extended BasicGameInfo class there and repackage the jar.
        See info in the server docs on adding a subgame.
        """
        return {"SCORE": player.score, "BESTSCORE": player.bestscore, "DEATHS": player.deaths, 
                "HIGHSCORE": self._highscore, "TIMELEFT": int(self.round_get_time_remaining()), "ROUNDTIME": self.__roundtime,
                "LSTDSTRBY": player.lastkilledby}

    
    def game_get_extra_radar_info(self, obj, objdata, player):
        """
        Called by the World when the obj is being radared, should add new properties to the objdata.

        Note: it is not supported to pick up these values directly by the client, it is best to use the existing properties that make sense.
        """
        if hasattr(obj, "player") and self.cfg.getboolean("World", "radar_include_name"):
            objdata["NAME"] = obj.player.name

    def server_disconnect_player(self, netid):        
        """
        Called by the server when a disconnect message is received by a player's client

        player_died should also be called, so it is recommended to override that method instead.
        """
        for player in self._players:
            if player.netid == netid and player.object != None:
                logging.debug("Player %s Disconnected", player.name)
                player.disconnected = True
                player.object.killed = True # terminate
                self.world.remove(player.object)
                player.object = None

                if self.__allowreentry:
                    if self._players.has_key(player.netid):
                        del self._players[player.netid] # should be handled by world part
                    return True

        logging.debug("Couldn't find player with netid %d to disconnect", netid);
        return False

    def player_get_by_name(self, name):
        """
        Retrieves a player by their name.
        """
        for player in self._players.values():
            if player.name == name:
                return player

        return None    
    
    def player_get_by_network_id(self, netid):
        """
        Used by the server to retrieve a player by their network id.
        """
        if self._players.has_key(netid):
            return self._players[netid]
        return None

    #endregion

    #region Player Scoring / Leaderboard Functions
    def player_update_score(self, player, amount):
        """
        Should be called to manipulate a player's score, will do extra bookkeeping and sanity for you.
        """
        player.score += amount

        # scores can't be negative
        if player.score < 0:
            player.score = 0

        # TODO: should probably check if primary highest flag to see if we want to keep track of lowest or highest score here
        # update if this is a new personal best
        if player.score > player.bestscore:
            player.bestscore = player.score
        
    def player_died(self, player, gone):
        """
        Will be called when a player dies, will adjust score appropriately based on game rules.
        Called before player object removed from player.

        gone will be True if the player is disconnected or killed (they won't respawn)

        Analog to player_added
        """
        player.deaths += 1
        if self._points_lost_on_death > 0:
            self.player_update_score(player, -self._points_lost_on_death)

        if self._reset_score_on_death:
            self._player_reset_score(player)

    def _player_reset_score(self, player):
        """
        Used to reset a players score and determine the new leader.

        Will be called by the default implementation of player_died if the reset_score_on_death configuration property is true.
        """
        player.score = self._points_initial

    def _player_add_to_final_round(self, player):
        """
        Add the player to the final round.  Will be automatically called by the default implementation for round_over.
        """
        self._tournamentfinalgroup.append(player)

    def game_get_current_leader_list(self, all=False):
        """
        Gets the list of players sorted by their score (highest first) (or all players)
        """
        # secondary victory first, primary second
        if all:
            return sorted(sorted(self.game_get_current_player_list(all), key=attrgetter(self._secondary_victory), reverse=self._secondary_victory_high), 
                   key=attrgetter(self._primary_victory), reverse=self._primary_victory_high)

        # TODO: Cache this and regen, update leader and highscore value there too, should I do this once every game update?
        return self.__leaderboard_cache

    def game_get_current_player_list(self, all=False):
        """
        Returns a list of player objects for players in the current round
        Returns all players if no tournament running or requested
        """
        if all or not self._tournament:
            return self._players
        else:
            if self._tournamentfinalround:
                return self._tournamentfinalgroup
            else:
                if self._tournamentcurrentgroup < len(self._tournamentgroups):
                    return self._tournamentgroups[self._tournamentcurrentgroup]
                else:
                    return []
            #eif
        #eif

    def player_get_stat_string(self, player):
        """
        Should return a string with information about the player and their current score.

        Defaults to:
        primary_score  secondary_score : player_name
        """
        return "%.1f" % getattr(player, self._primary_victory) + "  " + str(getattr(player, self._secondary_victory)) + " : " + player.name
    
    def tournament_is_running(self):
        """
        Returns true if a tournament is running.
        """
        return self._tournament
    #endregion
    
    #region World/Collision Functions
    def world_add_remove_object(self, wobj, added):
        """
        Called by world when an object is added or destroyed (before added (guaranteed to not have update) and after removed (though may receive last update))

        For simple tasks involving players look to the player_died or player_added methods

        killed ships will not return (used to prevent respawn)
        """
        logging.debug("[Game] Add Object(%s): #%d (%s)", repr(added), wobj.id, friendly_type(wobj))
        if not added and isinstance(wobj, Ship) and wobj.player.netid in self._players:
            nid = wobj.player.netid

            # if we were given an expiration time, means we haven't issued a command, so kill the ship
            if wobj.has_expired() and self.cfg.getboolean("Server", "disconnect_on_idle"):
                logging.info("Ship #%d killed due to timeout.", wobj.id)
                wobj.killed = True

            if hasattr(wobj, "killedby") and wobj.killedby != None:
                if isinstance(wobj.killedby, Ship):
                    self._players[nid].lastkilledby = wobj.killedby.player.name
                else:
                    self._players[nid].lastkilledby = friendly_type(wobj.killedby) + " #" + str(wobj.killedby.id)

            self.player_died(self._players[nid], (self._players[nid].disconnected or wobj.killed))

            self._players[nid].object = None

            if not self._players[nid].disconnected:
                if self._disconnect_on_death or wobj.killed:
                    if self.__allowreentry:
                        del self._players[nid]

                    # TODO: disconnect AI?
                    if nid >= 0:
                        self.server.sendDisconnect(nid)
                else:
                    if not self._players[nid].roundover:
                        # if the round isn't over, then re-add the ship
                        self._game_add_ship_for_player(nid, True)
    
    def world_physics_pre_collision(self, obj1, obj2):
        """
        Called by the physics engine when two objects just touch for the first time

        return [True/False, [func, obj, para...]... ]

        use False to not process collision in the physics engine, the function callback will still be called

        return a list with lists of function callback requests for the function, and object, and extra parameters

        The default game prevents anything from colliding with (BlackHole, Nebula, or Star) collide returns False.
        """
        logging.debug("Object #%d colliding with #%d", obj1.id, obj2.id)
        return obj1.collide_start(obj2) and obj2.collide_start(obj1)

    def world_physics_collision(self, obj1, obj2, damage):
        """
        Called by the physics engine when two objects collide

        Return [[func, obj, parameter]...]

        The default game handles inflicting damage on entities in this step.  
    
        It is best to override world_physics_pre_collision if you want to prevent things from occuring in the first place.
        """
        logging.debug("Object #%d collided with #%d for %f damage", obj1.id, obj2.id, damage)
        r = []

        obj1.take_damage(damage, obj2)
        obj2.take_damage(damage, obj1)

        for gobj in (obj1, obj2): # check both objects for callback
            if gobj.health.maximum > 0 and gobj.health.value <= 0:
                logging.info("Object #%d destroyed by %s", gobj.id, repr(gobj.killedby))
                r.append([self.world_physics_post_collision, gobj, damage])
            #eif
        if r == []: return None
        return r

    def world_physics_post_collision(self, dobj, damage):
        """
        Setup and called by world_physics_collision to process objects which have been destroyed as a result of taking too much damage.

        The default game causes an explosion force based on the strength of the collision in the vicinity of the collision.

        dobj: the object destroyed
        para: extra parameters from a previous step, by default collision passes the strength of the collision only
        """
        strength = damage
        logging.info("Destroying Object: #%d, Force: %d [%d]", dobj.id, strength, thread.get_ident())
        dobj.destroyed = True # get rid of object

        self.world.causeExplosion(dobj.body.position, dobj.radius * 5, strength, True) #Force in physics step

    def world_physics_end_collision(self, obj1, obj2):
        """
        Called by the physics engine after two objects stop overlapping/colliding.

        This is still called even if the pre_collision returned 'False' and no actual collision was processed
        """
        logging.debug("Object #%d no longer colliding with #%d", obj1.id, obj2.id)
        # notify each object of the finalization of the collision
        obj1.collide_end(obj2)
        obj2.collide_end(obj1)

    #endregion

    #region GUI Drawing
    def gui_initialize(self):
        """
        Used to initialize GUI resources at the appropriate time after the graphics engine has been initialized.
        """
        self._tfont = pygame.font.Font("freesansbold.ttf", 18)
        self._dfont = debugfont()

    def gui_draw_game_world_info(self, surface, flags, trackplayer):
        """
        Called by GUI to have the game draw additional (optional) info in the world when toggled on 'G'.
        (coordinates related to the game world)
        """
        pass

    def gui_draw_game_screen_info(self, screen, flags, trackplayer):
        """
        Called by GUI to have the game draw additional (optional) info on screen when toggled on 'G'.
        (coordinates related to the screen)
        """
        pass

    def gui_get_player_stats(self, all=False):
        """
        Called by GUI to get the sorted list of player stats.

        GUI expects a list of strings, you should usually override player_get_stat_string.
        """
        sstat = []
        for player in self.game_get_current_leader_list(all):
            sstat.append(self.player_get_stat_string(player))
        return sstat

    def gui_draw_tournament_bracket(self, screen, flags, trackplayer):
        """
        Called by GUI to draw info about the round/tournament (optional) when toggled on 'T'.
        (coordinates related to the screen)
        """
        if self._tournament and self._tournamentinitialized:
            # draw first Bracket
            y = 100
            for x in xrange(self._tournamentnumgroups):
                py = y
                for player in self._tournamentgroups[x]:
                    c = (128, 128, 128)
                    if x == self._tournamentcurrentgroup:
                        c = (255, 255, 255)
                    if trackplayer != None and player == trackplayer:
                        c = trackplayer.color
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
                c = (255, 255, 128)
                if trackplayer != None and player == trackplayer:
                    c = trackplayer.color
                screen.blit(self._tfont.render(player.name, False, c), (435, y))
                y += 24
            pygame.draw.line(screen, (192, 192, 192), (800, py), (810, py))
            pygame.draw.line(screen, (192, 192, 192), (810, py), (810, y))
            pygame.draw.line(screen, (192, 192, 192), (800, y), (810, y))

            if self._tournamentfinalwinner:
                screen.blit(self._tfont.render(self._tournamentfinalwinner.name, False, (128, 255, 255)), (835, py + (y - py) / 2))
        #eif
    #endregion
