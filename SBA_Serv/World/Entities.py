"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2015 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

import random, pymunk, math, logging

from Messaging import MessageQueue
from Commanding import CommandSystem
from WorldMath import PlayerStat

class PhysicalRound(object):
    IDs = random.randint(100, 200)

    def __init__(self, mass, radius, pos):
        self.id = PhysicalRound.IDs
        PhysicalRound.IDs += random.randint(1, 8)
        self.mass = mass
        self.radius = radius
        self.inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        self.body = pymunk.Body(mass, self.inertia)
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, radius, (0, 0))
        self.destroyed = False
        self.TTL = None
        self.explodable = True

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

class Entity(PhysicalRound):
    """Describes the basic properties for any entities in the game world"""

    def __init__(self, mass, radius, pos):
        super(Entity, self).__init__(mass, radius, pos)
        self.messageQueue = MessageQueue()
        self.health = PlayerStat(100)
        self.energy = PlayerStat(0)
        self.energyRechargeRate = 0 # Amount of Energy Recovered Per Second
        self.timealive = 0

    def update(self, t):
        self.timealive += t
        #self.energy += self.energyRechargeRate * t
        #self.position = self.velocity.updatePosition(self.position, t)

    """
    Should add keys to objData for extra properties object has over base
    """
    def getExtraInfo(self, objData):
        pass

class Ship(Entity):
    """Describes a ship"""

    def __init__(self, pos, world):
        super(Ship, self).__init__(500, 28, pos)
        self._world = world
        self.energyRechargeRate = 4

        self.body.velocity_limit = 100

        # Ship Specific
        self.commandQueue = CommandSystem(self, 4)

        self.shield = PlayerStat(100)
        self.shieldConversionRate = 1.0 # Amount of Shield Recovered Per Energy (Higher Better)
        self.shieldDamageReduction = 0.8 # Amount Damage is Multiplied by and taken from Shields before health is touched (Higher Better)
        self.radarRange = 300

        self.energy = PlayerStat(100)
        self.energyRechargeRate = 4

        self.thrusterForce = 3500
        self.rotationAngle = random.randint(0, 359)
        self.rotationSpeed = 120

        #self.resources = PlayerStat(1000)
        #self.resources.empty()
        #self.miningSpeed = 8
        self.tractorbeamForce = 10000
        
        self.lasernodes = []

        # extra state
        self.killed = False
        self.disconnected = False #TODO: Move to player?

    def setCommandBufferSize(self, size):
        old = self.commandQueue[:]
        self.commandQueue = MessageQueue(size)
        self.commandQueue.extend(old)

    def update(self, t):
        super(Ship, self).update(t) 
        self.commandQueue.update(t)
        self.energy += self.energyRechargeRate * t

    def getExtraInfo(self, objData):
        objData["RADARRANGE"] = self.radarRange
        objData["ROTATION"] = self.rotationAngle
        objData["ROTATIONSPEED"] = self.rotationSpeed
        objData["CURSHIELD"] = self.shield.value
        objData["MAXSHIELD"] = self.shield.maximum

class Planet(Entity):
    """
    Planets have stockpiles of energy which slowly recharge overtime
    Player's can leach energy off of a planet at twice their Energy Recharge Rate (Recover Energy Twice as Fast)
    Planet's also have resources which can be mined, as the planet's resources are mined, the planet recovers energy less
    """
    EnergyRechargeRateFactor = 2

    def __init__(self, pos, mass=-1, radius=60):
        if mass == -1: mass = 150000 + random.randint(0, 50000)
        super(Planet, self).__init__(mass, radius, pos)
        #self.energyRechargeRate = 1
        #self.energy = PlayerStat(random.randint(50, 200))

        # Everything in Group 1 won't hit anything else in Group 1
        self.shape.group = 1
        
        # Planets can't be moved by explosions
        self.explodable = False
        
        # Planet specific
        self.health = PlayerStat(0)
        self.gravity = random.randint(5, 25)
        self.gravityFieldLength = 96 + random.randint(16, 96)
        #self.resources = PlayerStat(random.randint(500, 2000))

    def getExtraInfo(self, objData):
        objData["GRAVITY"] = self.gravity
        objData["GRAVITYFIELDLENGTH"] = self.gravityFieldLength

class BlackHole(Planet):
    """
    BlackHoles are similar to planets however have no resources and have stronger gravity fields
    """
    def __init__(self, pos):
        super(BlackHole, self).__init__(pos, 400000, 16)
        self.gravity = 20 + random.randint(32, 48)
        self.gravityFieldLength = 48 + random.randint(16, 160)

        self.resources = PlayerStat(0)

class Asteroid(Entity):
    """
    Asteroids are given an initial random direction and speed and will travel in that direction forever until disrupted...
    """

    def __init__(self, pos):
        #TODO: Make Asteroids of different sizes
        super(Asteroid, self).__init__(random.randint(1500, 3500), 16, pos)
        self.shape.elasticity = 0.8
        self.health = PlayerStat(self.mass / 15.0)

        self.shape.group = 1

        # initial movement
        v = random.randint(20000, 40000)
        self.body.apply_impulse((random.randint(-1, 1) * v, random.randint(-1, 1) * v), (0,0))

class Torpedo(Entity):
    """
    Torpedos are weapons which are launched from ships at a given position and direction
    """
    def __init__(self, pos, direction, owner=None):
        pos = (pos[0] + math.cos(math.radians(-direction)) * 32,
               pos[1] + math.sin(math.radians(-direction)) * 32)
        super(Torpedo, self).__init__(60, 6, pos)
        self.TTL = 4 # Torpedos last 4 seconds
        self.shape.elasticity = 0.8
        self.health = PlayerStat(1)
        self.owner = owner

        #self.shape.group = 1
        v = 15000
        self.body.apply_impulse((math.cos(math.radians(-direction)) * v,
                                 math.sin(math.radians(-direction)) * v), (0,0))
                                 
    def getExtraInfo(self, objData):
        objData["OWNERID"] = self.owner.id
