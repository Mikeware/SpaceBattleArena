"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2020 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

import random
import pymunk
import math
import logging
import sys

from .WorldCommands import RaiseShieldsCommand, CloakCommand
from .Messaging import MessageQueue
from .Commanding import CommandSystem
from .WorldMath import PlayerStat, getPositionAwayFromOtherObjects, cfg_rand_min_max, istypeinlist
from .Entities import PhysicalRound, PhysicalEllipse
from pymunk import Vec2d, ShapeFilter

class Ship(PhysicalRound):
    """
    A Ship is the main entity a player controls in the world.
    
    Attributes:
        killed: boolean different than destroyed, represents an object forcibly removed from the world (by GUI or end of round), should NOT respawn
    """

    def __init__(self, pos, world):
        super(Ship, self).__init__(28, 500, pos)
        self._world = world # NOTE: The ONLY reason this is here/needed is because the ship is creating a Torpedo from it's command system...
        self.energyRechargeRate = 4        

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
        self.killed = False # forcibly removed object 'for good'

    def _constructPhysics(self, mass, pos):
        self.velocity_limit = 100

        super(Ship, self)._constructPhysics(mass, pos)

    def setCommandBufferSize(self, size):
        old = self.commandQueue[:]
        self.commandQueue = MessageQueue(size)
        self.commandQueue.extend(old)

    def take_damage(self, damage, by=None, force=False):
        logging.debug("Ship #%d taking damage %d", self.id, damage)
        if self.commandQueue.containstype(RaiseShieldsCommand, force) and self.shield.value > 0:
            logging.debug("Shields of #%d absorbed %d damage", self.id, damage * self.shieldDamageReduction)
            self.shield -= damage * self.shieldDamageReduction
            super(Ship, self).take_damage(damage * (1.0 - self.shieldDamageReduction), by)
        else:
            super(Ship, self).take_damage(damage, by)
        #eif

        if self.health == 0:
            if self.killedby != None:
                if isinstance(self.killedby, Star):
                    self.player.sound = "BURN"
                elif isinstance(self.killedby, BlackHole):
                    self.player.sound = "CRUSH"
                else:
                    self.player.sound = "EXPLODE"
            else:
                self.player.sound = "EXPLODE"
        elif by != None:
            if isinstance(by, Dragon):
                self.player.sound = "CHOMP"
            elif isinstance(by, Weapon):
                self.player.sound = "IMPACT"
            elif not isinstance(by, Star):
                self.player.sound = "HIT"

    def update(self, t):
        super(Ship, self).update(t)
        if len(self.commandQueue) > 0: 
            self.commandQueue.update(t)
            self.TTL = None
        elif self.TTL == None and hasattr(self, "player") and self.player.netid >= 0: # if we're a human player, make sure we issue another command within 10 seconds, or kill scuttle the ship.
            logging.info("Ship #%d on clock for not issuing a command in given time.", self.id)
            self.TTL = self.timealive + 10
        self.energy += self.energyRechargeRate * t

    def getExtraInfo(self, objData, player):
        objData["RADARRANGE"] = self.radarRange
        objData["ROTATION"] = int(self.rotationAngle) % 360
        objData["ROTATIONSPEED"] = self.rotationSpeed
        objData["CURSHIELD"] = self.shield.value
        objData["MAXSHIELD"] = self.shield.maximum

        # Only show some properties to the owner of the ship
        if player != None and hasattr(self, "player") and self.player != None and self.player.netid == player.netid:
            objData["CMDQ"] = self.commandQueue.getRadarRepr()
        else:
            # Remove this property for other ships
            del objData["CURENERGY"]

class CelestialBody:
    """
    Celestial Bodies are a sub-baseclass to denote Entities which have an effect when the player is within their hit 'radius'.

    They can also be 'mined' for energy with the LowerEnergyScoopCommand, though this is most effective in Nebulas and Stars
    """
    
    def collide_start(self, otherobj):
        """
        Notification that this object is now starting to collide with the otherobj.

        return False in order to force the Physics Engine to ignore the normal processing of the collision (e.g. bounce/damage)
        """
        self.in_celestialbody.append(otherobj)
        otherobj.in_celestialbody.append(self)

    def collide_end(self, otherobj):
        """
        Notification that this object is no longer colliding with the otherobj.
        """
        if otherobj in self.in_celestialbody:
            self.in_celestialbody.remove(otherobj)
        if self in otherobj.in_celestialbody:
            otherobj.in_celestialbody.remove(self)

class Influential:
    """
    Influential bodies are those which have a circular area of effect behind their hit radius (like gravity for planets).

    They should have an 'influence_range' property
    """
    def apply_influence(self, otherobj, mapped_pos, t):
        """
        This function will get called once for every object within the range of influence.

        The mapped_position may not be the actual position of the object, but the modified coordinates outside the edge of the world border to help with math.
        """
        pass

class Nebula(CelestialBody, PhysicalEllipse):
    """
    Nebulas are an odd shape.

    They impose a 'friction' on objects and TODO: reduce radar range?
    """
    def __init__(self, pos, size=(384, 256), pull=2000, mass=-1):
        if mass == -1: mass = sys.maxsize
        super(Nebula, self).__init__(size, mass, pos)

        self.body.angle = math.radians(random.randint(-30, 30))

        # Everything in Group 1 won't hit anything else in Group 1
        self.shape.filter = ShapeFilter(group=1)
        
        # Nebulas can't be moved by explosions
        self.explodable = False
        self.gravitable = False
        
        self.health = PlayerStat(0)
        self.pull = pull
        #self.resources = PlayerStat(random.randint(500, 2000))

    def collide_start(self, otherobj):
        # TODO: Add 'in' function here and drag
        super(Nebula, self).collide_start(otherobj)
        return False

    def update(self, t):
        # Objects in nebulas get slowed down
        if self.pull > 0:
            for obj in self.in_celestialbody:
                if obj.body.velocity.length > 0.1:
                    v = obj.body.velocity
                    v.length -= (self.pull / obj.mass) * t
                    obj.body.velocity = v

        super(Nebula, self).update(t)

    def getExtraInfo(self, objData, player):
        objData["PULL"] = self.pull

        # Overrides
        objData["DIRECTION"] = -math.degrees(self.body.angle) % 360
        objData["ROTATION"] = int(round(-math.degrees(self.body.angle)) % 360)

        objData["MAJOR"] = self.major
        objData["MINOR"] = self.minor

    @staticmethod
    def spawn(world, cfg, pos=None):
        if pos == None:
            pos = getPositionAwayFromOtherObjects(world, cfg.getint("Nebula", "buffer_object"), cfg.getint("Nebula", "buffer_edge"))
        n = Nebula(pos, random.choice(eval(cfg.get("Nebula", "sizes"))), cfg_rand_min_max(cfg, "Nebula", "pull"))
        world.append(n)
        return n

class Quasar(Nebula):
    """
    Quasars are an odd shape and act like a Nebula.

    They also reduce energy regen, drain shields, and prevent shields from working.
    """
    def __init__(self, pos, size=(384, 256), pull=1000, mass=-1):
        super(Quasar, self).__init__(pos, size, pull, mass)

    def update(self, t):
        # Objects in Quasars lose energy and shields
        for obj in self.in_celestialbody:
            if isinstance(obj, Ship):
                obj.energy -= (obj.energyRechargeRate * 0.75) * t
                obj.shield -= (obj.shieldConversionRate * 0.75) * t

        super(Quasar, self).update(t)

    @staticmethod
    def spawn(world, cfg, pos=None):
        if pos == None:
            pos = getPositionAwayFromOtherObjects(world, cfg.getint("Quasar", "buffer_object"), cfg.getint("Quasar", "buffer_edge"))
        n = Quasar(pos, random.choice(eval(cfg.get("Quasar", "sizes"))), cfg_rand_min_max(cfg, "Quasar", "pull"))
        world.append(n)
        return n

class Planet(Influential, PhysicalRound):
    """
    Planets (and similar celestial bodies) have gravity which will pull a player towards their center

    TODO:
    Planet's also have resources which can be mined
    """

    def __init__(self, pos, size=128, pull=15, radius=60, torpedo=False, mass=-1):
        if mass == -1: mass = sys.maxsize
        super(Planet, self).__init__(radius, mass, pos)

        #self.energyRechargeRate = 1
        #self.energy = PlayerStat(random.randint(50, 200))

        # Everything in Group 1 won't hit anything else in Group 1
        self.shape.filter = ShapeFilter(group=1)
        
        # Planets can't be moved by explosions
        self.explodable = False
        self.gravitable = False
        
        # Planet specific
        self.health = PlayerStat(0)
        self.pull = pull
        self.influence_range = size
        #self.resources = PlayerStat(random.randint(500, 2000))

        self.effect_weapon = torpedo

    def getExtraInfo(self, objData, player):
        objData["PULL"] = self.pull

        objData["MAJOR"] = self.influence_range
        objData["MINOR"] = self.influence_range

    def apply_influence(self, otherobj, mapped_pos, t):
        # apply 'gravity' pull amount force towards planet's center if not a Torpedo (hard math) or another Planet thing (fixed)
        if self.effect_weapon or not isinstance(otherobj, Weapon):
            #TODO: Should we use apply_force_at_local_point? or apply_force_at_world_point from planet's center? Would that mean we wouldn't need distance calculation?
            otherobj.body.apply_impulse_at_local_point((mapped_pos - self.body.position) * -self.pull * t, (0,0))

    @staticmethod
    def spawn(world, cfg, pos=None):
        if pos == None:
            pos = getPositionAwayFromOtherObjects(world, cfg.getint("Planet", "buffer_object"), cfg.getint("Planet", "buffer_edge"))
        p = Planet(pos, cfg_rand_min_max(cfg, "Planet", "range"), cfg_rand_min_max(cfg, "Planet", "pull"), torpedo=cfg.getboolean("Planet", "pull_weapon"))
        world.append(p)
        return p

class BlackHole(CelestialBody, Planet):
    """
    BlackHoles are similar to planets however have no resources and have stronger gravity fields
    """
    def __init__(self, pos, size=96, pull=64, crushtime=5.0, torpedo=False):
        super(BlackHole, self).__init__(pos, size, pull, 16, torpedo)
        self._crushtime = crushtime

    def collide_start(self, otherobj):
        otherobj.bh_timer = 0
        super(BlackHole, self).collide_start(otherobj)
        return False

    def update(self, t):
        if self.pull > 0 and self._crushtime > 0.001:
            # Ships in center of BH for too long get crushed
            for obj in self.in_celestialbody:
                if isinstance(obj, Ship):
                    obj.bh_timer += t
                    if obj.bh_timer >= self._crushtime and not obj.commandQueue.containstype(RaiseShieldsCommand):
                        obj.take_damage(9000, self)

    @staticmethod
    def spawn(world, cfg, pos=None):
        if pos == None:
            pos = getPositionAwayFromOtherObjects(world, cfg.getint("BlackHole", "buffer_object"), cfg.getint("BlackHole", "buffer_edge"))
        bh = BlackHole(pos, cfg_rand_min_max(cfg, "BlackHole", "range"), cfg_rand_min_max(cfg, "BlackHole", "pull"), cfg.getfloat("BlackHole", "crush_time"), cfg.getboolean("Planet", "pull_weapon"))
        world.append(bh)
        return bh


class Star(CelestialBody, Planet):
    """
    Stars are similar to planets/blackholes however cause damage in relation to how close you are to their center
    """
    def __init__(self, pos, size=192, pull=32, extra=0.0, torpedo=False):
        super(Star, self).__init__(pos, size, pull, 90, torpedo)

        # make the star pull have a small impact on the rate of damage
        self.dmg_divide = 18 - (self.pull / 6.0) - extra

    def collide_start(self, otherobj):
        super(Star, self).collide_start(otherobj)
        return False

    def update(self, t):
        # Objects in stars take damage
        if self.pull > 0:
            for obj in self.in_celestialbody:
                if isinstance(obj, Ship):
                    #print self.id, self.pull, self.dmg_divide, (self.radius + obj.radius - self.body.position.get_distance(obj.body.position)) / self.dmg_divide
                    obj.take_damage(max(0, (self.radius + obj.radius - self.body.position.get_distance(obj.body.position)) * t / self.dmg_divide), self)

        super(Star, self).update(t)

    @staticmethod
    def spawn(world, cfg, pos=None):
        if pos == None:
            pos = getPositionAwayFromOtherObjects(world, cfg.getint("Star", "buffer_object"), cfg.getint("Star", "buffer_edge"))
        s = Star(pos, cfg_rand_min_max(cfg, "Star", "range"), cfg_rand_min_max(cfg, "Star", "pull"), cfg.getfloat("Star", "dmg_mod"), cfg.getboolean("Planet", "pull_weapon"))
        world.append(s)
        return s

class WormHole(CelestialBody, Influential, PhysicalRound):
    """
    WormHoles can teleport players to other areas of space or to other WormHoles paired with one another.

    Note: Worm Hole's size should be less than its radius for special processing requirements.
    """

    RANDOM = 1
    OTHER_CELESTIALBODY = 2
    FIXED_POINT = 3

    def __init__(self, pos, size=44, radius=96, whtype=1, exitpos=None): # need pairing option
        """
        whtype should be the type of WormHole (RANDOM, OTHER_CELESTIALBODY, FIXED_POINT)

        if you choose type FIXED_POINT, pass in an exitpos as a position
        if you choose type RANDOM, pass in an exitpos as a function which returns a random point.
        """
        super(WormHole, self).__init__(radius, sys.maxsize, pos)

        # Everything in Group 1 won't hit anything else in Group 1
        self.shape.filter = ShapeFilter(group=1)

        self.health = PlayerStat(0)
        self.influence_range = size # just used for consistency
        
        # WormHoles can't be moved by explosions
        self.explodable = False
        self.gravitable = False

        self.type = whtype
        self.exit = exitpos

    def link_wormhole(self, other_wormhole):
        """
        Links the given object to this one so that it will be the 'exit' to this wormhole. (Could be a blackhole, star, or nebula for instance)
        """
        self.exit = other_wormhole

    def collide_start(self, otherobj):
        super(WormHole, self).collide_start(otherobj)
        return False

    def apply_influence(self, otherobj, mapped_pos, t):
        # teleport ships, todo: cooldown check
        if (not hasattr(otherobj, "teleported") or otherobj.teleported == False or otherobj.teleported == self.id):
            if isinstance(otherobj, Ship):
                otherobj.player.sound = "WORMHOLE"

            if self.type == WormHole.RANDOM:
                otherobj.body.position = self.exit()
            elif self.type == WormHole.OTHER_CELESTIALBODY:
                otherobj.body.position = self.exit.body.position + (random.randint(-self.influence_range, self.influence_range), random.randint(-self.influence_range, self.influence_range))
            elif self.type == WormHole.FIXED_POINT:
                otherobj.body.position = pymunk.Vec2d(self.exit) + (random.randint(-self.influence_range, self.influence_range), random.randint(-self.influence_range, self.influence_range))

            otherobj.teleported = self.id
            logging.info("Ship #%d entered wormhole of type %d and was moved to position %s.", otherobj.id, self.type, repr(otherobj.body.position))

        return False
    
    def collide_end(self, otherobj):
        super(WormHole, self).collide_end(otherobj)

        if not hasattr(otherobj, "teleported") or (otherobj.teleported and otherobj.teleported != self.id):
            otherobj.teleported = False

    def getExtraInfo(self, objData, player):
        objData["MAJOR"] = self.influence_range
        objData["MINOR"] = self.influence_range

    @staticmethod
    def spawn(world, cfg, pos=None):
        get_random_point = lambda : getPositionAwayFromOtherObjects(world, cfg.getint("WormHole", "buffer_exit_object"), cfg.getint("WormHole", "buffer_exit_edge"))

        if pos == None:
            pos = getPositionAwayFromOtherObjects(world, cfg.getint("WormHole", "buffer_object"), cfg.getint("WormHole", "buffer_edge"))
        wht = random.choice(eval(cfg.get("WormHole", "types")))
        if wht == WormHole.RANDOM:
            p = WormHole(pos, whtype=WormHole.RANDOM, exitpos=get_random_point)
        elif wht == WormHole.FIXED_POINT:
            p = WormHole(pos, whtype=WormHole.FIXED_POINT, exitpos=get_random_point())
        elif wht == WormHole.OTHER_CELESTIALBODY:
            pos2 = getPositionAwayFromOtherObjects(world, cfg.getint("WormHole", "buffer_object"), cfg.getint("WormHole", "buffer_edge"))
            p2 = WormHole(pos2, whtype=WormHole.OTHER_CELESTIALBODY)
            world.append(p2)

            p = WormHole(pos, whtype=WormHole.OTHER_CELESTIALBODY)
            
            p.link_wormhole(p2)
            p2.link_wormhole(p)
        world.append(p)
        return p

class Asteroid(PhysicalRound):
    """
    Asteroids are given an initial random direction and speed and will travel in that direction forever until disrupted...
    """

    def __init__(self, pos, move_speed=30, mass = None):
        #TODO: Make Asteroids of different sizes
        if mass == None:
            mass = random.randint(1500, 3500)
        super(Asteroid, self).__init__(16, mass, pos)
        self.shape.elasticity = 0.8
        self.health = PlayerStat(self.mass / 15.0)

        self.shape.filter = ShapeFilter(group=1)

        # initial movement
        ang = random.randint(0, 359)
        self.body.velocity = Vec2d(math.cos(math.radians(ang)) * move_speed,
                                   math.sin(math.radians(ang)) * move_speed)

    @staticmethod
    def spawn(world, cfg, pos=None):
        if pos == None:
            pos = getPositionAwayFromOtherObjects(world, cfg.getint("Asteroid", "buffer_object"), cfg.getint("Asteroid", "buffer_edge"))
        a = Asteroid(pos, cfg_rand_min_max(cfg, "Asteroid", "move_speed"))
        world.append(a)
        return a

class Dragon(CelestialBody, Influential, PhysicalRound):
    """
    Dragons move around the world and may try and track a nearby player.

    Ships are munched on a bit when close to its mouth.
    """
    def __init__(self, pos, attack_range=64, attack_speed=5, health=400, attack_time=(1.0, 2.0), attack_amount=(15, 25), move_speed=14, mass = None):
        if mass == None:
            mass = random.randint(3000, 5000)
        super(Dragon, self).__init__(16, mass, pos)
        self.shape.elasticity = 0.8
        self.health = PlayerStat(health)

        self.shape.filter = ShapeFilter(group=1)

        self.influence_range = attack_range
        self.attack_speed = attack_speed
        self.attack_time = attack_time
        self.attack_amt = attack_amount
        self._get_next_attack()
        self.target = None
        self.see = []
        #initial movement
        ang = random.randint(0, 359)
        self.body.velocity = Vec2d(math.cos(math.radians(ang)) * move_speed,
                                   math.sin(math.radians(ang)) * move_speed)
        self.lv = self.body.velocity.normalized()

    def _get_next_attack(self):
        self.natk = (random.uniform(self.attack_time[0], self.attack_time[1]),
                     random.randint(self.attack_amt[0], self.attack_amt[1]))

    def collide_start(self, otherobj):
        otherobj.dr_timer = 0
        super(Dragon, self).collide_start(otherobj)
        if isinstance(otherobj, Weapon): # Torpedos & SpaceMines can hit Dragons
            return True

        return False

    def apply_influence(self, otherobj, mapped_pos, t):
        # get closest ship though cloak protects ship from dragon 'seeing' it
        if isinstance(otherobj, Ship) and not otherobj.commandQueue.containstype(CloakCommand):
            if self.target == None or self.body.position.get_dist_sqrd(mapped_pos) < self.body.position.get_dist_sqrd(self.target[1].body.position): # TODO: Get this to be able to wrap
                if self.target == None:
                    if len(self.in_celestialbody) == 0:
                        otherobj.player.sound = "RAWR"
                    if self.body.velocity.length == 0:
                        self.body.velocity = self.lv * self.attack_speed
                    else:
                        v = self.body.velocity
                        v.length += self.attack_speed
                        self.body.velocity = v
                    self.lv = self.body.velocity.normalized()
                self.target = (pymunk.Vec2d(mapped_pos), otherobj)
            elif self.target[1] == otherobj:
                # Update our position of our tracked object
                self.target = (pymunk.Vec2d(mapped_pos), otherobj)
            self.see.append(otherobj)

    def update(self, t):
        # Objects 'in' dragons take damage
        #if self.pull > 0: # TODO: Range for moving towards thing
        for obj in self.in_celestialbody:
            if isinstance(obj, Ship) and not obj.commandQueue.containstype(CloakCommand):
                obj.dr_timer += t
                if obj.dr_timer >= self.natk[0]:
                    obj.dr_timer = 0
                    obj.take_damage(self.natk[1], self)
                    self._get_next_attack()

        if self.target != None and self.target[1] not in self.see:
            self.target = None
            if self.body.velocity.length > self.attack_speed:
                v = self.body.velocity
                v.length -= self.attack_speed * 0.9 # TODO: make this 'rage retainer' a config value???
                self.body.velocity = v
        self.see = []

        if self.target != None:
            # turn towards target
            nang = self.body.velocity.get_angle_degrees_between(self.target[0] - self.body.position)
            v = self.body.velocity            
            v.angle_degrees += nang * t
            self.body.velocity = v

            # clear target as we'll reaquire to 'readjust course' for moving object...
            dist = self.body.position.get_dist_sqrd(self.target[0])
            if dist < self.radius * 1.5 and self.target[1].body.velocity.length < self.body.velocity.length or self.target[1].health <= 0:
                if self.body.velocity.length > self.attack_speed:
                    v = self.body.velocity
                    v.length -= self.attack_speed
                    self.body.velocity = v
            if dist > self.influence_range * self.influence_range * 1.1 or self.target[1].health <= 0:
                self.target = None

        super(Dragon, self).update(t)

    def getExtraInfo(self, objData, player):
        objData["PULL"] = self.attack_speed

        objData["MAJOR"] = self.influence_range
        objData["MINOR"] = self.influence_range

    @staticmethod
    def spawn(world, cfg, pos=None):
        if pos == None:
            pos = getPositionAwayFromOtherObjects(world, cfg.getint("Dragon", "buffer_object"), cfg.getint("Dragon", "buffer_edge"))
        d = Dragon(pos, cfg_rand_min_max(cfg, "Dragon", "range"), 
                        cfg_rand_min_max(cfg, "Dragon", "attack_speed"), 
                        cfg_rand_min_max(cfg, "Dragon", "health"),
                        (cfg.getfloat("Dragon", "attack_time_min"), cfg.getfloat("Dragon", "attack_time_max")),
                        (cfg.getfloat("Dragon", "attack_amount_min"), cfg.getfloat("Dragon", "attack_amount_max")),
                        cfg_rand_min_max(cfg, "Dragon", "move_speed")
                        )
        world.append(d)
        return d

class Weapon(PhysicalRound):
    def __init__(self, radius, mass, position):
        super(Weapon, self).__init__(radius, mass, position)

class Torpedo(Weapon):
    """
    Torpedos are weapons which are launched from ships at a given position and direction
    """
    def __init__(self, pos, direction, owner=None):
        pos = (pos[0] + math.cos(math.radians(-direction)) * 32,
               pos[1] + math.sin(math.radians(-direction)) * 32)
        super(Torpedo, self).__init__(6, 60, pos)
        self.TTL = 4 # Torpedos last 4 seconds
        self.shape.elasticity = 0.8
        self.health = PlayerStat(1)
        self.owner = owner
        self.explodable = False

        #self.shape.filter = ShapeFilter(group=1)
        v = 15000
        self.body.apply_impulse_at_local_point((math.cos(math.radians(-direction)) * v,
                                                math.sin(math.radians(-direction)) * v), (0,0))
                                 
    def getExtraInfo(self, objData, player):
        objData["OWNERID"] = self.owner.id

class SpaceMine(CelestialBody, Influential, Weapon):
    """
    SpaceMines are weapons which are dropped from a ship
    """

    STATIONARY = 1
    AUTONOMOUS = 2
    HOMING = 3
    
    RADIUS = 128
    FORCE = 600

    def __init__(self, pos, delay, wmode, direction=None, speed=None, duration=None, owner=None):
        super(SpaceMine, self).__init__(7, 120, pos)
        self.shape.elasticity = 0.7
        self.health = PlayerStat(1)
        self.owner = owner
        self.explodable = False
        self.delay = delay
        self.active = False
        self.mode = wmode
        self.direction = direction
        self.speed = speed
        self.duration = duration
        self.influence_range = 96
        self.attack_speed = 5
        self.target = None
        self.lv = self.body.velocity.normalized()

    def collide_start(self, otherobj):
        #TODO: Test if we say False, if we ever get collide_end notification...?
        parent = super(SpaceMine, self).collide_start(otherobj)
        if not self.active:
            return False

        return parent

    def update(self, t):
        super(SpaceMine, self).update(t)
        self.delay -= t

        if self.delay <= 0:
            if istypeinlist(Ship, self.in_celestialbody):
                logging.info("Ship still touching mine when activated!")
                self.TTL = self.timealive - 1
            elif self.mode == SpaceMine.AUTONOMOUS and not self.active:
                v = 500 * self.speed
                self.body.apply_impulse_at_local_point((math.cos(math.radians(-self.direction)) * v,
                                                        math.sin(math.radians(-self.direction)) * v), (0,0))
                self.TTL = self.timealive + self.duration
            elif self.mode == SpaceMine.HOMING:
                if self.target != None:
                    # turn towards target
                    nang = self.body.velocity.get_angle_degrees_between(self.target - self.body.position)
                    v = self.body.velocity
                    v.angle_degrees += nang * t
                    self.body.velocity = v

                    # clear target as we'll reaquire to 'readjust course' for moving object...
                    if self.body.position.get_dist_sqrd(self.target) < 300:
                        if self.body.velocity.length > self.attack_speed:
                            v = self.body.velocity
                            v.length -= self.attack_speed
                            self.body.velocity = v
                        self.target = None
            self.active = True

    def apply_influence(self, otherobj, mapped_pos, t):
        if not self.active or self.mode != SpaceMine.HOMING:
            return

        # get closest ship though cloak protects ship from dragon 'seeing' it
        if isinstance(otherobj, Ship) and not otherobj.commandQueue.containstype(CloakCommand) and \
                (self.target == None or self.body.position.get_dist_sqrd(mapped_pos) < self.body.position.get_dist_sqrd(self.target)):
            if self.target == None:
                if self.body.velocity.length < 1:
                    if self.body.velocity.length == 0:
                        nang = 0
                    else:
                        nang = self.body.velocity.get_angle_degrees_between(mapped_pos - self.body.position)
                    self.body.apply_impulse_at_local_point((math.cos(math.radians(nang)) * self.attack_speed * 100,
                                                            math.sin(math.radians(nang)) * self.attack_speed * 100), (0,0))
                else:
                    v = self.body.velocity
                    v.length += self.attack_speed
                    self.body.velocity = v
                self.lv = self.body.velocity.normalized()
            self.target = pymunk.Vec2d(mapped_pos)
                                   
    def getExtraInfo(self, objData, player):
        if self.owner != None:
            objData["OWNERID"] = self.owner.id

    @staticmethod
    def spawn(world, cfg, pos=None):
        if pos == None:
            pos = getPositionAwayFromOtherObjects(world, cfg.getint("SpaceMine", "buffer_object"), cfg.getint("SpaceMine", "buffer_edge"))
        t = random.choice(eval(cfg.get("SpaceMine", "types")))
        if t == SpaceMine.AUTONOMOUS:
            sm = SpaceMine(pos, cfg_rand_min_max(cfg, "SpaceMine", "delay"), t, cfg_rand_min_max(cfg, "SpaceMine", "direction"), cfg_rand_min_max(cfg, "SpaceMine", "speed"), cfg_rand_min_max(cfg, "SpaceMine", "duration"))
        else:
            sm = SpaceMine(pos, cfg_rand_min_max(cfg, "SpaceMine", "delay"), t)
        world.append(sm)
        return sm

class Constellation(CelestialBody, PhysicalRound):
    """
    Constellations are mainly decorative, but are useful to be scanned in Discovery Quest
    """

    def __init__(self, pos):
        super(Constellation, self).__init__(48, sys.maxsize, pos)

        # Everything in Group 1 won't hit anything else in Group 1
        self.shape.filter = ShapeFilter(group=1)
        
        # Constellations can't be moved by explosions
        self.explodable = False
        self.gravitable = False

        self.health = PlayerStat(0)

    def collide_start(self, otherobj):
        super(Constellation, self).collide_start(otherobj)
        return False

    @staticmethod
    def spawn(world, cfg, pos=None):
        if pos == None:
            pos = getPositionAwayFromOtherObjects(world, cfg.getint("Constellation", "buffer_object"), cfg.getint("Constellation", "buffer_edge"))
        a = Constellation(pos)
        world.append(a)
        return a
