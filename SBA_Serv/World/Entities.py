import random
import pymunk
import math
import logging

from Messaging import MessageQueue
from Commanding import CommandSystem
from WorldMath import PlayerStat

class Entity(object):
    """Describes the basic properties for any entities in the game world.
    
    Attributes:
        id: integer unique id for the object.
        messageQueue: MessageQueue object to store messages for this Entity (unused).
        health: PlayerStat object representing the health of this object (default 100).
        enery: PlayerStat object representing the energy of this object (default 0).
        energyRechargeRate: integer representing how quickly (per second) the energy rechages (default 0).
        timealive: number to keep track of the total time (in seconds) this object has lived.
    """
    IDs = random.randint(100, 200)

    def __init__(self):
        self.id = Entity.IDs
        Entity.IDs += random.randint(1, 8) # Prevent guessing of id assignments
        
        self.messageQueue = MessageQueue()
        self.health = PlayerStat(100)
        self.energy = PlayerStat(0)
        self.energyRechargeRate = 0 # Amount of Energy Recovered Per Second
        self.timealive = 0

    def update(self, t):
        """Called each game frame to update the object

        Args:
            t: amount of time elapsed since last frame (excluding draw time).
        """
        self.timealive += t
        #self.energy += self.energyRechargeRate * t
        #self.position = self.velocity.updatePosition(self.position, t)
    
    def getExtraInfo(self, objData):
        """Method called by world to get extra Radar info about a particular Entity.

        Args:
            objData: dictionary[string] = obj Should add keys to objData for extra properties object has over base properties.

        See WorldMap.getObjectData.
        """
        pass

class PhysicsCore(Entity):
    """Abstract class to be used as a basis for physical models of entities.

    Attributes:
        mass: mass of object.
        destroyed: boolean should this object be removed on the next cycle.
        TTL: if set as number, will automatically remove the object after this time has elapsed.
        explodable: will this object be influenced by explosions in the game world.

        inertia: physical moment for this object.
        body: pymunk Body for this object.
        shape: pymunk Shape for this object.
    """
    def __init__(self, mass, pos):
        super(PhysicsCore, self).__init__()
        self._constructPhysics(mass, pos)        
        
        self.destroyed = False
        self.TTL = None
        self.explodable = True

    def _constructPhysics(self, mass, pos):
        """To be called by the parent class to define the Physical model of this shape.

        Should define the mass, inertia, body, position, and shape for the object.
        """
        pass

    def addToSpace(self, space):
        self.shape.id = self.id
        space.add(self.body, self.shape)

    def removeFromSpace(self, space):
        if hasattr(self.shape, "id"):
            logging.info("Removing Shape #%d", self.shape.id)
        else:
            logging.error("Shape doesn't have ID for Object #%d", self.id)
        #eif
        space.remove(self.shape, self.body)

class PhysicalRound(PhysicsCore):
    """Round Entity.

    This is a Physical Entity which is a shape that is round.
    """
    def __init__(self, radius, mass, pos):
        self.radius = radius
        super(PhysicalRound, self).__init__(mass, pos)
            

    def _constructPhysics(self, mass, pos):
        """Called by parent constructor.
        """
        self.mass = mass
        self.inertia = pymunk.moment_for_circle(mass, 0, self.radius, (0, 0))
        self.body = pymunk.Body(mass, self.inertia)
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, self.radius, (0, 0))
