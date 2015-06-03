
import logging
import time

from random import randint
from threading import Thread
from importlib import import_module

import World.WorldEntities
from World.WorldMath import intpos, friendly_type
from World.WorldGenerator import *
from World.Entities import Entity

class CallbackTimer(Thread):
    """
    CallbackTimer is a class which will call a function after a given interval of time (in a positive integer number of seconds)

    It starts when start() is called and cannot be adjusted after starting.
    It can be cancelled by calling cancel().

    The function will be called with no parameters (by default) after the allotted time has elapsed.

    Parameters:
        seconds: number of seconds to wait before calling the callback
        callback: function to call when time elapsed
        parameter: optional parameter to pass into the callback
    """
    def __init__(self, seconds, callback, parameter=None):
        self.time_total = seconds
        self.time_left = self.time_total
        self.__parameter = parameter
        self.__callback = callback
        self.__cancel = False
        self.__done = False
        Thread.__init__(self)

    def iscomplete(self):
        return self.__done

    def cancel(self):
        self.__cancel = True

    def run(self):
        for sec in xrange(self.time_total, -1, -1):
            time.sleep(1.0)
            self.time_left = sec
            if self.__cancel:
                return
        if self.__parameter == None:
            self.__done = True
            self.__callback()
        else:
            self.__done = True
            self.__callback(self.__parameter)

class SpawnConfig:
    """
    Class used to track the individual spawning properties of a given Entity Type
    """
    def __init__(self, name, ctype):
        self.name = name
        self.type = ctype
        self._timed = False
        self._min = False
        self._max = False
        self._player = False

    def add_timed_spawn(self, time_num, time_min, time_max): # int, int, int
        if time_num > 0 and time_min > 0 and time_max > time_min:
            self._timed = True
            self.time_num = time_num
            self._time_min = time_min
            self._time_max = time_max
        else:
            logging.error("Check time parameters for spawning %s", self.name)

    def is_timed(self):
        return self._timed

    def get_next_time(self):
        return random.randint(self._time_min, self._time_max)

    def add_minimum(self, keep_min): #int : number of minimum 
        if keep_min > 0:
            self._min = True
            self.num_min = keep_min
        else:
            logging.error("Check minimum parameters for spawning %s", self.name)

    def is_min(self):
        return self._min

    def add_maximum(self, keep_max): #int : number of maximum
        if keep_max > 0:
            self._max = True
            self.num_max = keep_max
        else:
            logging.error("Check maximum parameters for spawning %s", self.name)

    def is_max(self):
        return self._max

    def add_player_spawn(self, on_player_num, on_player_start, on_player_respawn): # int, bool, bool
        if on_player_num > 0 and (on_player_start or on_player_respawn):
            self._player = True
            self.player_num = on_player_num
            self._player_start = on_player_start
            self._player_respawn = on_player_respawn
        else:
            logging.error("Check player parameters for spawning %s", self.name)

    def is_player(self, reason):
        return self._player and ((reason == 1 and self._player_start) or (reason == 2 and self._player_respawn))

class SpawnManager:
    ENTITY_TYPES = None
    """
    Class used to manage the lifecycles of different entities.
    """
    def __init__(self, cfg, world):
        if SpawnManager.ENTITY_TYPES == None:
            # Auto Load Entity Type Names
            logging.info("Spawn Manager Initializing Game Object Types")
            SpawnManager.ENTITY_TYPES = {}
            for obj in World.WorldEntities.__dict__.itervalues():
                if isinstance(obj, type) and Entity in obj.__mro__: # Is this object an Entity
                    SpawnManager.ENTITY_TYPES[obj.__name__] = obj

            rungame = cfg.get("Game", "game")
            if rungame != "Basic" and rungame != None and rungame.strip() != "":
                mod = import_module("Game."+rungame)
                for obj in mod.__dict__.itervalues():
                    if isinstance(obj, type) and Entity in obj.__mro__ and obj.__name__ not in SpawnManager.ENTITY_TYPES: # Is this object an Entity we haven't seen before?
                        SpawnManager.ENTITY_TYPES[obj.__name__] = obj

            for obj in World.Entities.__dict__.itervalues():
                if isinstance(obj, type) and Entity in obj.__mro__ and obj.__name__ in SpawnManager.ENTITY_TYPES: # Is this object a base Entity we should ignore?
                    del SpawnManager.ENTITY_TYPES[obj.__name__] # Get rid of physical base entities

            logging.info("Spawn Manager Found Types: %s", repr(SpawnManager.ENTITY_TYPES.keys()))

            print SpawnManager.ENTITY_TYPES

        self._cfg = cfg
        self._world = world
        self._spawns = {}
        for entity, ctype in SpawnManager.ENTITY_TYPES.iteritems():
            # Check each section for the properties we want!
            if cfg.has_section(entity):
                sc = SpawnConfig(entity, ctype)
                # do we want to spawn any entities over time?
                if cfg.has_option(entity, "spawn_time_num"):
                    sc.add_timed_spawn(cfg.getint(entity, "spawn_time_num"),
                                       cfg.getint(entity, "spawn_time_min"),
                                       cfg.getint(entity, "spawn_time_max"))
                # do we want to keep a minimum around?
                if cfg.has_option(entity, "spawn_keep_min"):
                    sc.add_minimum(cfg.getint(entity, "spawn_keep_min"))
                # do we want to keep a maximum around?
                if cfg.has_option(entity, "spawn_keep_max"):
                    sc.add_maximum(cfg.getint(entity, "spawn_keep_max"))
                # do we want to spawn any entities when a player logins?
                if cfg.has_option(entity, "spawn_on_player_num"):
                    sc.add_player_spawn(cfg.getint(entity, "spawn_on_player_num"),
                                        self.bool(cfg.get(entity, "spawn_on_player_start")),
                                        self.bool(cfg.get(entity, "spawn_on_player_respawn")))

                self._spawns[entity] = sc

        self._timers = {}
        self._running = False

    def bool(self, value):
        return value.lower() == "true"

    def player_added(self, reason):
        """
        Called when a player is added to the world
        """
        if self._running:
            for sc in self._spawns.itervalues():
                if sc.is_player(reason):
                    self.spawn_entity(sc.name, respawntimer=False, number=sc.player_num)

    def start(self):
        """
        Start object spawn timers (if any)
        """
        self._running = True
        for sc in self._spawns.itervalues():
            if self._should_spawn(sc):
                self.add_timer(sc.name)

    def _should_spawn(self, sc):
        """
        Check maximum boundry of a configuration
        """
        return sc.is_timed() and (not sc.is_max() or (sc.is_max() and self._world.get_count_of_objects(sc.type) < sc.num_max)) and not self.has_timer(sc.name)

    def add_timer(self, entityname):
        if self._running and self._spawns.has_key(entityname):
            sc = self._spawns[entityname]
            if not self._timers.has_key(entityname):
                self._timers[entityname] = []
            logging.info("Adding Spawn Timer for %s", entityname)
            timer = CallbackTimer(sc.get_next_time(), self.spawn_entity, entityname)
            self._timers[entityname].append(timer)
            timer.start()
            logging.debug("Now %d Spawn Timers for %s", len(self._timers[entityname]), entityname)

    def has_timer(self, entityname):
        if not self._timers.has_key(entityname):
            return False

        for x in xrange(len(self._timers[entityname]) - 1, -1, -1):
            if not self._timers[entityname][x].iscomplete():
                return True

        return False

    def clean_timer(self, entityname):
        """
        Clean up any completed timers for the given entity name
        """
        for x in xrange(len(self._timers[entityname]) - 1, -1, -1):
            if self._timers[entityname][x].iscomplete():
                del self._timers[entityname][x]

        if len(self._timers[entityname]) == 0:
            del self._timers[entityname]

    def stop(self):
        """
        Stop all timers
        """
        self._running = False
        logging.info("Stopping Spawn Timers")
        for lst in self._timers.values():
            for timer in lst:
                timer.cancel()

        self._timers = {}

    def check_number(self, wobj):
        """
        Checks the number of objects in the world to see if more need to be added over minimum.
        """
        name = friendly_type(wobj)
        if self._running and self._spawns.has_key(name):            
            sc = self._spawns[name]

            if sc.is_min():
                count = self._world.get_count_of_objects(type(wobj))
                logging.info("Found %d %s Entities", count, name)
                if count < sc.num_min:
                    self.spawn_entity(name, respawntimer=self._should_spawn(sc), number = sc.num_min - count)

            elif self._should_spawn(sc):
                self.add_timer(sc.name)

    def spawn_entity(self, typename, pos=None, respawntimer=True, number=1):
        """
        Spawns a type of entity with the given name into the world associated with the Spawn Manager.

        number overwritten if respawntimer
        """
        logging.info("Spawning Entity %s", typename)
        sc = self._spawns[typename]

        if pos == None:
            count = number
            
            if number == 1 and respawntimer and sc.is_timed():
                count = sc.time_num
        
            for i in xrange(count):
                eval("spawn_" + typename + "(self._world, self._cfg)")
        else:
            eval("spawn_" + typename + "(self._world, self._cfg, " + repr(intpos(pos)) + ")")

        # readd a timer now that its expired if we haven't hit the max number of objects in world
        if respawntimer and self._should_spawn(sc):
            self.clean_timer(typename)
            self.add_timer(typename)

