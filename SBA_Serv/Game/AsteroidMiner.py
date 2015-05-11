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

        self.__torpedopoints = self.cfg.getint("AsteroidMiner", "points_torpedo")
        self.__shippoints = self.cfg.getint("AsteroidMiner", "points_ship")
    
    def player_added(self, player, reason):
        super(AsteroidMinerGame, self).player_added(player, reason)

        if reason == BasicGame._ADD_REASON_START_:
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
    def world_physics_pre_collision(self, shapes):
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
                self.player_update_score(torpedo.owner.player, 1)

                # add new asteroid
                self.__addAsteroid(True)
            #eif

        logging.info("Done checkAsteroid #%d", torpedo.id)            
        
    """

    def world_add_remove_object(self, wobj, added):
        logging.debug("BH Add Object(%s): #%d (%s)", repr(added), wobj.id, friendly_type(wobj))
        if not added and isinstance(wobj, Asteroid) and hasattr(wobj, "killedby") and wobj.killedby != None:
            obj = wobj.killedby
            if isinstance(obj, Torpedo):
                self.player_update_score(obj.owner.player, self.__torpedopoints)
                    
                logging.info("Torpedo Owner (#%d) Destroyed Asteroid", obj.owner.id)
            elif isinstance(obj, Ship) and obj.health.value > 0:
                self.player_update_score(obj.player, self.__shippoints)
                    
                logging.info("Ship (#%d) Destroyed Asteroid", obj.id)
        else:
            super(AsteroidMinerGame, self).world_add_remove_object(wobj, added)


    def round_over(self):
        self.__btimer.cancel() # prevent more asteroids from being spawned!

        super(AsteroidMinerGame, self).round_over()

    def round_start(self):
        super(AsteroidMinerGame, self).round_start()

        # start Bauble Spawn Timer
        self.newAsteroidTimer()    
        
    def newAsteroidTimer(self):
        self.__btimer = RoundTimer(self.cfg.getint("AsteroidMiner", "spawn_time"), self.spawnAsteroid)
        self.__btimer.start()

    def spawnAsteroid(self):
        self.__addAsteroids(self.world, self.cfg.getint("AsteroidMiner", "spawn_number"))
        
        self.newAsteroidTimer()
