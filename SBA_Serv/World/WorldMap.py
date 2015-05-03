"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2015 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

import logging
import thread, threading, time, math
import pymunk
import traceback
from WorldMath import in_circle, wrappos, intpos, friendly_type
from World.WorldEntities import Planet, Ship
from WorldCommands import CloakCommand
from ThreadStuff.ThreadSafe import ThreadSafeDict

MINIMUM_GAMESTEP_TIME = 0.02 #50fps

class GameWorld(object):
    """
    represents the virtual space world and the objects in it
    Provides hit detection and radar between objects in the world
    """
    def __init__(self, game, worldsize, pys=True):
        self.__game = game
        self.size = intpos(worldsize)
        self.width = worldsize[0]
        self.height = worldsize[1]
        self.__space = pymunk.Space()
        #self.__space.add_collision_handler(0, 0, post_solve=self.collideShipStellarObject)
        self.__space.set_default_collision_handler(begin=self.__beginCollideObject, post_solve=self.__collideObject)
        self.__objects = ThreadSafeDict()
        self.__addremovesem = threading.Semaphore()
        self.__planets = []
        self.__objectListener = []
        self.__toremove = []
        self.__toadd = []        
        self.__active = True
        self.__pys = pys

        if pys:
            thread.start_new_thread(self.__THREAD__gameloop, ())

    def endGameLoop(self):
        self.__active = False
            
    def newWorld(self, world):
        self.__pys = False
        time.sleep(0.2)
        
        # Remove All Objects
        for obj in self:
            self.pysremove(obj)
            
        # Copy objects from new world to original world
        for obj in world:
            #world.pysremove(obj) # need to remove object from space before adding to another
            self.append(obj, pys=True)
            
        self.__pys = True
        
    def __beginCollideObject(self, space, arbiter):
        if arbiter.is_first_contact:
            r = self.__game.worldObjectPreCollision( arbiter.shapes )
            if r != None:
                for i in r[1]:
                    space.add_post_step_callback(i[0], i[1], i[2:])
                return r[0]  

        return True       
        
    def __collideObject(self, space, arbiter):        
        if arbiter.is_first_contact:
            r = self.__game.worldObjectCollision( arbiter.shapes, arbiter.total_impulse.length / 250.0 )
            if r != None:
                for i in r:
                    space.add_post_step_callback(i[0], i[1], i[2:])            
        #eif

    def causeExplosion(self, origin, radius, strength, force=False):
        logging.debug("Start Explosion %s, %d, %d [%d]", origin, radius, strength, thread.get_ident())
        origin = pymunk.Vec2d(origin)
        for obj in self.__objects:
            if obj.explodable:
                for point in wrappos(obj.body.position, radius, self.size):
                    if in_circle(origin, radius, point):                        
                        logging.debug("Applying Explosion Force to #%d", obj.id)
                        obj.body.apply_impulse((point - origin) * strength, (0,0))
                        break        
        logging.debug("Done Explosion") 
        
    def registerObjectListener(self, callback):
        self.__objectListener.append(callback)

    def __len__(self):
        return len(self.__objects)

    def __iter__(self):
        return self.__objects.__iter__()

    def __getitem__(self, key):
        return self.__objects.__getitem__(key)

    def __setitem__(self, key, value):
        return self.__objects.__setitem__(key, value)

    # for adding to the world from other threads outside game loop
    def append(self, item, pys=False):
        logging.debug("Append Object to World %s [%d]", repr(item), thread.get_ident())
        added = False        
        logging.debug("SEMAPHORE ACQ append [%d]", thread.get_ident())
        self.__addremovesem.acquire()
        if not self.__objects.has_key(item.id):
            self.__objects[item.id] = item
            if pys:
                item.addToSpace(self.__space)
            else:
                self.__toadd.append(item)
            added = True
            if isinstance(item, Planet):
                self.__planets.append(item)
        self.__addremovesem.release()
        logging.debug("SEMAPHORE REL append [%d]", thread.get_ident())                
        if added:
            for objListener in self.__objectListener:
                objListener(item, True)
                
    def remove(self, item):
        del self[item]

    def pysremove(self, item):
        self.__delitem__(item, True)
        
    def __delitem__(self, key, pys=False):
        logging.debug("Removing Object from World %s [%d]", repr(key), thread.get_ident())
        for objListener in self.__objectListener:
            objListener(key, False)
        logging.debug("SEMAPHORE ACQ delitem [%d]", thread.get_ident())
        self.__addremovesem.acquire()            
        if self.__objects.has_key(key.id):
            if pys:
                key.removeFromSpace(self.__space)
            else:
                self.__toremove.append(key)
            
            del self.__objects[key.id]
            if key in self.__planets:
                self.__planets.remove(key)
        self.__addremovesem.release()           
        logging.debug("SEMAPHORE REL delitem [%d]", thread.get_ident())

    def __THREAD__gameloop(self):
        lasttime = MINIMUM_GAMESTEP_TIME
        try:
            while self.__active:
                if self.__pys:
                    self.__space.step(MINIMUM_GAMESTEP_TIME) # Advance Physics Engine
                
                tstamp = time.time()
                for obj in self: # self is dictionary
                    # Wrap Object in World
                    if obj.body.position[0] < 0:
                        obj.body.position[0] += self.width
                    elif obj.body.position[0] > self.width:
                        obj.body.position[0] -= self.width
                    if obj.body.position[1] < 0:
                        obj.body.position[1] += self.height
                    elif obj.body.position[1] > self.height:
                        obj.body.position[1] -= self.height

                    # Apply Gravity for Planets
                    if obj.explodable:
                        for planet in self.__planets:
                            for point in wrappos(obj.body.position, planet.gravityFieldLength, self.size):
                                if in_circle(planet.body.position, planet.gravityFieldLength, point):                        
                                    obj.body.apply_impulse((point - planet.body.position) * -planet.gravity * lasttime, (0,0))
                                    break
                    
                    # Update and Run Commands
                    obj.update(lasttime)

                    if obj.TTL != None and obj.timealive > obj.TTL:
                        del self[obj]                        
                #next            

                # game time notification
                self.__game.update(lasttime)
                lasttime = time.time() - tstamp
                           
                logging.debug("SEMAPHORE ACQ gameloop [%d]", thread.get_ident())
                self.__addremovesem.acquire()
                #remove objects
                for item in self.__toremove:
                    logging.info("World Removing #%d from Physics Engine %s", item.id, repr(item))
                    item.removeFromSpace(self.__space)
                    
                self.__toremove = []
                    
                # add objects
                for item in self.__toadd:
                    logging.info("World Adding #%d to Physics Engine %s", item.id, repr(item))
                    item.addToSpace(self.__space)

                self.__toadd = []
                self.__addremovesem.release()
                logging.debug("SEMAPHORE REL gameloop [%d]", thread.get_ident())
                    
                # minimum to conserve resources
                if lasttime < MINIMUM_GAMESTEP_TIME:
                    time.sleep(MINIMUM_GAMESTEP_TIME - lasttime)
                    lasttime = MINIMUM_GAMESTEP_TIME
                #else:
                    #logg#ging.debug("Can't keep at 50fps at %dfps", 1.0 / lasttime)
                #eif
            #wend
        except:
            print "EXCEPTION IN GAMELOOP"
            logging.exception("FATAL Error in game loop!!!")
            logging.error(traceback.format_exc())
            print traceback.format_exc()
        logging.debug("Gameloop Ended")

    def getObjectsInArea(self, pos, radius, force=False):
        logging.debug("Get Objects In Area %s %d (%s) [%d]", repr(pos), radius, repr(force), thread.get_ident())
        objList = []
        for obj in self.__objects.values():
            for point in wrappos(obj.body.position, radius, self.size):
                if in_circle(pos, radius, point):
                    objList.append(obj)
                    break
                #eif
            #next
        #next
        return objList

    def getObjectData(self, obj):
        objData = {}
        # Convert Type of Object to String
        objData["TYPE"] = friendly_type(obj)
        objData["ID"] = obj.id
        objData["POSITION"] = intpos(obj.body.position)
        objData["SPEED"] = obj.body.velocity.length
        # TODO: deal with -0.0 case OR match physics library coordinates?
        objData["DIRECTION"] = -obj.body.velocity.angle_degrees # 30 = -120?, -80 = -10
        #objData["VELOCITYDIRECTION"] = obj.velocity.direction
        objData["MAXSPEED"] = obj.body.velocity_limit
        objData["CURHEALTH"] = obj.health.value
        objData["MAXHEALTH"] = obj.health.maximum
        objData["CURENERGY"] = obj.energy.value
        objData["MAXENERGY"] = obj.energy.maximum
        objData["ENERGYRECHARGERATE"] = obj.energyRechargeRate
        objData["MASS"] = obj.mass
        objData["HITRADIUS"] = obj.radius
        objData["TIMEALIVE"] = obj.timealive

        obj.getExtraInfo(objData)

        self.__game.getExtraRadarInfo(obj, objData)

        return objData

    def getEnvironment(self, ship, radarlevel=0, target=-1, getMessages=False):
        #TODO: abstract radar to game level?
        radardata = None
        if radarlevel > 0:
            objs = self.getObjectsInArea(ship.body.position, ship.radarRange)
            #TODO: Need to wait lock the removing of ships with accessing...???
            if ship in objs: objs.remove(ship) # Get rid of self...

            # remove ships with cloak
            for x in xrange(len(objs) - 1, -1, -1):
                if isinstance(objs[x], Ship) and objs[x].commandQueue.containstype(CloakCommand):
                    del objs[x]
                #eif
            #next

            if radarlevel == 1:
                # number of objects
                radardata = []
                for i in xrange(len(objs)):
                    radardata.append({})
            elif radarlevel == 2:
                # (pos, id) list
                radardata = []
                for e in objs:
                    radardata.append({"POSITION":intpos(e.body.position), "ID":e.id})
                #next
            elif radarlevel == 3:
                for obj in objs:
                    if obj.id == target:
                        radardata = [self.getObjectData(obj)]
                        break
            elif radarlevel == 4:
                # (pos, id, type)
                radardata = []
                for e in objs:
                    radardata.append({"POSITION":intpos(e.body.position), "ID":e.id, "TYPE":friendly_type(e)})
                #next
            elif radarlevel == 5:
                radardata = []
                for e in objs:
                    radardata.append(self.getObjectData(e))
                #next
            #eif
        #eif

        msgQueue = []
        if getMessages:
            msqQueue = list(ship.messageQueue)

        return {"SHIPDATA": self.getObjectData(ship),
                "RADARLEVEL": radarlevel,
                "RADARDATA": radardata,
                "GAMEDATA": self.__game.getExtraEnvironment(ship.player),
                "MESSAGES": msgQueue,
                }
