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
        self.TTL = None # None means will live 'forever', otherwise if timealive > TTL (time to live), then the object will be automatically cleaned up in gameloop and destroyed.

        self.in_celestialbody = [] # keeps track of celestial bodies this object is in

    def collide_start(self, otherobj):
        """
        Called on both objects when a collision first occurs, the other object is the one being hit

        If either object returns False, then no collision will occur
        """
        return True

    def collide_end(self, otherobj):
        """
        Called when two objects finish colliding/overlapping (even if they didn't actually 'collide')
        """
        pass

    def take_damage(self, damage, by=None):
        """
        Called when damage is taken.
        """
        logging.debug("Object #%d took %d damage", self.id, damage)
        self.health -= damage
        if self.health.maximum > 0 and self.health.value <= 0:
            if by != None:
                logging.info("Object #%d killed by #%d", self.id, by.id)
            self.killedby = by

    def has_expired(self):
        """
        Has this entity expired?

        Returns False if there is no expiry time either.
        """
        return self.TTL != None and self.timealive > self.TTL

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

        destroyed: this object has lost all its health and was removed from the world
        TTL: time to live, amount of time before this object should get removed from the world, if None will be ignored
        explodable: boolean should this object be effected by explosion forces
    """
    def __init__(self, mass, pos):
        super(PhysicsCore, self).__init__()
        self._constructPhysics(mass, pos)
        self.body.position = pos
        
        self.destroyed = False        
        self.explodable = True

    def _constructPhysics(self, mass, pos):
        """To be called by the parent class to define the Physical model of this shape.

        Should define the mass, inertia, body, position, and shape for the object.
        """
        pass

    def addToSpace(self, space):
        self.shape.id = self.id
        self.shape.world_object = self
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

    This is a Physical Entity which has a shape that is round.

    Attributes:
        radius: integer radois of the object.
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
        self.shape = pymunk.Circle(self.body, self.radius, (0, 0))

class PhysicalPoly(PhysicsCore):
    """Polygon Entity.

    This is a Physical Entity which has a shape that is a closed polygon.

    Attributes:
        points: list of tuples representing points on the polygon.
    """
    def __init__(self, pointlist, mass, pos):
        self.points = pointlist
        super(PhysicalPoly, self).__init__(mass, pos)

    def _constructPhysics(self, mass, pos):
        self.mass = mass
        self.inertia = pymunk.moment_for_poly(mass, self.points)
        self.body = pymunk.Body(mass, self.inertia)
        self.shape = pymunk.Poly(self.body, self.points)

class PhysicalEllipse(PhysicalPoly):
    """Elliptical Entity.

    This is a Physical Entity which has a shape that is an elliptical.

    Attributes:
        major: length of ellipse along its angle from center point to edge
        minor: length of ellipse perpendicular to its angle from the center point to edge
    """
    def __init__(self, size, mass, pos, segments=16):
        a = size[0] / 2
        b = size[1] / 2
        self.major = a
        self.minor = b
        self.radius = b + int((a - b) / 2) # HACK: expect all objects to have radius
        points = []
        ang = math.pi * 2 / segments
        for seg in xrange(0, segments):
            points.append((a * math.cos(seg * ang), b * math.sin(seg * ang)))

        super(PhysicalEllipse, self).__init__(points, mass, pos)
