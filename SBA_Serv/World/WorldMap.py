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
from World.WorldEntities import Influential, Ship
from WorldCommands import CloakCommand
from ThreadStuff.ThreadSafe import ThreadSafeDict

MINIMUM_GAMESTEP_TIME = 0.02 #50fps

class GameWorld(object):
    """
    represents the virtual space world and the objects in it
    Provides hit detection and radar between objects in the world
    """
    def __init__(self, game, worldsize, objlistener=None):
        """
        Parameters:
            game: game object that manages rules for world
            worldsize: tuple of world width,height
            pys: flag to indicate whether this should be the main world running a physics/game loop or not
            objlistener: initial listner callback function
        """
        self.__game = game
        self.size = intpos(worldsize)
        self.width = worldsize[0]
        self.height = worldsize[1]
        self.__space = pymunk.Space()
        #self.__space.add_collision_handler(0, 0, post_solve=self.collideShipStellarObject)
        self.__space.set_default_collision_handler(begin=self.__beginCollideObject, post_solve=self.__collideObject, separate=self.__endCollideObject)
        self.__objects = ThreadSafeDict()
        self.__addremovesem = threading.Semaphore()
        self.__influential = []
        if objlistener == None:
            self.__objectListener = []
        else:
            self.__objectListener = [objlistener]
        self.__toremove = []
        self.__toadd = []        
        self.__active = False
        self.__started = False
        self.gameerror = False
        logging.info("Initialized World of size %s", repr(worldsize))

    def start(self):
        if not self.__started:
            self.__started = True
            self.__active = True
            self.__pys = True
            logging.debug("Started gameloop for World %s", repr(self))
            threading.Thread(None, self.__THREAD__gameloop, "WorldMap_gameloop_" + repr(self)).start()

    def mid_point(self, xoff = 0, yoff = 0):
        return intpos((self.width / 2 + xoff, self.height / 2 + yoff))

    def endGameLoop(self):
        self.__active = False
            
    def destroy_all(self):
        self.__pys = False # disable physics step while we add/remove all objects
        time.sleep(0.2)
        
        # Remove All Objects
        for obj in self:
            self.pysremove(obj)
        
        self.__pys = True
        
    def __beginCollideObject(self, space, arbiter):
        if arbiter.is_first_contact:
            r = self.__game.world_physics_pre_collision( arbiter.shapes[0].world_object, arbiter.shapes[1].world_object )
            if r != None:
                if r == False or r == True:
                    return r
                for i in r[1:]:
                    space.add_post_step_callback(i[0], i[1], i[2])
                return r[0]

        return True       
        
    def __collideObject(self, space, arbiter):        
        if arbiter.is_first_contact:
            r = self.__game.world_physics_collision( arbiter.shapes[0].world_object, arbiter.shapes[1].world_object, arbiter.total_impulse.length / 250.0 )
            if r != None:
                for i in r:
                    space.add_post_step_callback(i[0], i[1], i[2])
        #eif

    def __endCollideObject(self, space, arbiter):
        # when object is destroyed in callback, arbiter may be empty
        if hasattr(arbiter, "shapes"):            
            self.__game.world_physics_end_collision( arbiter.shapes[0].world_object, arbiter.shapes[1].world_object )
        
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
        if callback not in self.__objectListener:
            self.__objectListener.append(callback)

    def __len__(self):
        return len(self.__objects)

    def __iter__(self):
        return self.__objects.__iter__()

    def __getitem__(self, key):
        return self.__objects.__getitem__(key)

    def __setitem__(self, key, value):
        return self.__objects.__setitem__(key, value)

    def has_key(self, key):
        return self.__objects.has_key(key)

    def append(self, item, pys=False):
        """
        Call to add an object to the game world from threads outside the game loop
        """
        logging.debug("Append Object to World %s [%d]", repr(item), thread.get_ident())
        for objListener in self.__objectListener:
            objListener(item, True)

        logging.debug("SEMAPHORE ACQ append [%d]", thread.get_ident())
        self.__addremovesem.acquire()
        if not self.__objects.has_key(item.id):
            self.__objects[item.id] = item
            if pys:
                item.addToSpace(self.__space)
            elif item in self.__toremove:
                self.__toremove.remove(item)
            else:
                self.__toadd.append(item)

            if isinstance(item, Influential) and item.influence_range > 0:
                self.__influential.append(item)
        self.__addremovesem.release()
        logging.debug("SEMAPHORE REL append [%d]", thread.get_ident())                

    def remove(self, item):
        """
        Call to remove an object from the game world
        """
        del self[item]

    def pysremove(self, item):
        self.__delitem__(item, True)
        
    def __delitem__(self, key, pys=False):
        logging.debug("Removing Object from World %s [%d]", repr(key), thread.get_ident())
        # Notify each item this may be in that it's no longer colliding
        # HACK: Get around issue with PyMunk not telling us shapes when object removed already before separate callback
        if len(key.in_celestialbody) > 0:
            for item in key.in_celestialbody[:]:
                item.collide_end(key)

        logging.debug("SEMAPHORE ACQ delitem [%d]", thread.get_ident())
        self.__addremovesem.acquire()            
        if self.__objects.has_key(key.id):
            if pys:
                key.removeFromSpace(self.__space)
            elif key in self.__toadd:
                self.__toadd.remove(key)
            else:
                self.__toremove.append(key)
            
            del self.__objects[key.id]
            if key in self.__influential:
                self.__influential.remove(key)
        self.__addremovesem.release()           
        logging.debug("SEMAPHORE REL delitem [%d]", thread.get_ident())
        
        # Notify after removed, in case re-add same object
        for objListener in self.__objectListener:
            objListener(key, False)

    def __THREAD__gameloop(self):
        lasttime = MINIMUM_GAMESTEP_TIME
        try:
            while self.__active:
                if self.__pys:
                    self.__space.step(MINIMUM_GAMESTEP_TIME) # Advance Physics Engine
                
                tstamp = time.time()

                # update all game objects
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
                        for influencer in self.__influential:
                            for point in wrappos(obj.body.position, influencer.influence_range, self.size):
                                if in_circle(influencer.body.position, influencer.influence_range, point):
                                    influencer.apply_influence(obj, point, lasttime)
                                    break
                    
                    # Update and Run Commands
                    obj.update(lasttime)

                    if obj.has_expired() or obj.destroyed:
                        del self[obj]
                #next            

                # game time notification
                self.__game.game_update(lasttime)

                # update time
                lasttime = time.time() - tstamp
                           
                logging.debug("SEMAPHORE ACQ gameloop [%d]", thread.get_ident())
                self.__addremovesem.acquire()
                # NOTE ISSUE #68 - If server is slow, can be adding and removing object in same step... add first, so we can immediately remove instead of crash
                # TODO: just look for common set between two lists and remove... or have each list check the other first before adding to the lists...
                #       probably best to refactor to PyMunk 4.0.0 and be able to have PyMunk handle adding/removing objects during physics step.
                # add objects
                for item in self.__toadd:
                    logging.info("World Adding #%d to Physics Engine %s", item.id, repr(item))
                    item.addToSpace(self.__space)

                self.__toadd = []

                #remove objects
                for item in self.__toremove:
                    logging.info("World Removing #%d from Physics Engine %s", item.id, repr(item))
                    item.removeFromSpace(self.__space)
                    
                self.__toremove = []
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
            self.gameerror = True
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

    def get_count_of_objects(self, type):
        count = 0
        for obj in self.__objects.values():
            if isinstance(obj, type):
                count += 1
            #eif
        #next
        return count

    def getObjectData(self, obj, player):
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
        objData["HITRADIUS"] = obj.radius #TODO: Move to entites that have this i.e. physicalround?
        objData["TIMEALIVE"] = obj.timealive
        objData["INBODY"] = (len(obj.in_celestialbody) > 0)

        obj.getExtraInfo(objData, player)

        self.__game.game_get_extra_radar_info(obj, objData, player)

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
                        radardata = [self.getObjectData(obj, ship.player)]
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
                    radardata.append(self.getObjectData(e, ship.player))
                #next
            #eif
        #eif

        msgQueue = []
        if getMessages:
            msqQueue = list(ship.messageQueue)

        return {"SHIPDATA": self.getObjectData(ship, ship.player),
                "RADARLEVEL": radarlevel,
                "RADARDATA": radardata,
                "GAMEDATA": self.__game.game_get_extra_environment(ship.player),
                "MESSAGES": msgQueue,
                }
