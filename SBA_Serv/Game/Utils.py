
import logging
import time

from random import randint
from threading import Thread

from World.WorldMath import intpos, friendly_type
from World.WorldGenerator import *

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

class SpawnManager:
    """
    Class used to manage the lifecycles of different entities.
    """
    def __init__(self, cfg, world):
        self._cfg = cfg
        self._world = world
        self._entities = []
        if cfg.has_section("Spawn"): #TODO: instead look for each Entity section for properties?
            logging.info("Spawn Manager Initializing")
            self._entities = cfg.get("Spawn", "entity_types").split(",")
            self._numtimes = map(int, cfg.get("Spawn", "time_num").split(",")) # number of entities to spawn (if 0 then no spawn timer)
            self._mintimes = map(int, cfg.get("Spawn", "time_min").split(",")) # minimum time between spawns (still required) 
            self._maxtimes = map(int, cfg.get("Spawn", "time_max").split(",")) # maximum time between spawns
            self._keepmin = map(self.bool, cfg.get("Spawn", "keep_around").split(",")) # should the initial number of entities always be around
            self._playernum = map(int, cfg.get("Spawn", "on_player_num").split(",")) # should the entity spawn when a player joins
            self._playerstart = map(self.bool, cfg.get("Spawn", "on_player_start").split(",")) # should the entity spawn when a player joins
            self._playerrespawn = map(self.bool, cfg.get("Spawn", "on_player_respawn").split(",")) # should the entity spawn when a player joins
            self._minnum = []
            # get the original starting numbers for the entities
            for entity in self._entities:
                self._minnum.append(cfg.getint(entity, "number"))

        self._timers = {}
        self._running = False

    def bool(self, value):
        return value.lower() == "true"

    def get_index(self, entityname):
        if entityname in self._entities:
            return self._entities.index(entityname)

    def player_added(self, reason):
        """
        Called when a player is added to the world
        """
        if self._running:
            for x in xrange(len(self._entities)):
                if (reason == 1 and self._playerstart[x]) or (reason == 2 and self._playerrespawn[x]):
                    self.spawn_entity(self._entities[x], respawntimer=False, number=self._playernum[x])

    def start(self):
        """
        Start object spawn timers (if any)
        """
        self._running = True
        for x in xrange(len(self._entities)):
            if self._numtimes[x] > 0:
                self.add_timer(self._entities[x])

    def add_timer(self, entityname):
        if self._running:
            index = self.get_index(entityname)
            if index != None:
                if not self._timers.has_key(entityname):
                    self._timers[entityname] = []
                logging.info("Adding Spawn Timer for %s", entityname)
                timer = CallbackTimer(randint(self._mintimes[index], self._maxtimes[index]), self.spawn_entity, entityname)
                self._timers[entityname].append(timer)
                timer.start()

    def clean_timer(self, entityname):
        """
        Clean up any completed timers for the given entity name
        """
        for x in xrange(len(self._timers[entityname]) - 1, -1, -1):
            if self._timers[entityname][x].iscomplete():
                del self._timers[entityname][x]

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
        if self._running:
            name = friendly_type(wobj)
            x = self.get_index(name)

            if x != None and self._keepmin[x]:
                count = self._world.get_count_of_objects(type(wobj))
                logging.info("Found %d %s Entities", count, name)
                if count < self._minnum[x]:
                    for i in xrange(count, self._minnum[x]):
                        self.spawn_entity(name, respawntimer=False)

    def spawn_entity(self, typename, pos=None, respawntimer=True, number=1):
        """
        Spawns a type of entity with the given name into the world associated with the Spawn Manager.

        number overwritten if respawntimer
        """
        logging.info("Spawning Entity %s", typename)
        if pos == None:
            count = number

            x = self.get_index(typename)
            if respawntimer and x != None and self._numtimes[x] > 0:
                count = self._numtimes[x]
        
            for i in xrange(count):
                eval("spawn_" + typename + "(self._world, self._cfg)")
        else:
            eval("spawn_" + typename + "(self._world, self._cfg, " + repr(intpos(pos)) + ")")

        # readd a timer now that its expired        
        if respawntimer and x != None and self._numtimes[x] > 0:
            self.clean_timer(typename)
            self.add_timer(typename)

