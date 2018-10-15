"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2016 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

import logging
import random
import math
from pymunk import Vec2d
from WorldMath import intpos
import WorldEntities
#from Entities import Torpedo

#TODO: Have Command Definition? List parameters?
SHIP_CMD_THRUST = "THRST"
SHIP_CMD_BRAKE = "BRAKE"
SHIP_CMD_ROTATE = "ROT"
SHIP_CMD_STEER = "STEER"
SHIP_CMD_IDLE = "IDLE"
SHIP_CMD_RADAR = "RADAR"

SHIP_CMD_DEPLOY_LASER_BEACON = "DLBN"
SHIP_CMD_DESTROY_ALL_BEACONS = "DAYLB"

SHIP_CMD_ALL_STOP = "STOP"
SHIP_CMD_WARP = "WARP"

SHIP_CMD_TORPEDO = "FIRE"
SHIP_CMD_SPACEMINE = "MINE"

SHIP_CMD_SHIELD = "SHLD"
SHIP_CMD_CLOAK = "CLOAK"

SHIP_CMD_REPAIR = "REP"
SHIP_CMD_SCOOP = "SCOOP"

from Messaging import Command, OneTimeCommand

def ConvertNetworkMessageToCommand(ship, cmdname, cmddict):
    # Sanitize Network Input and Convert to Game Command
    if isinstance(cmdname, unicode) and isinstance(cmddict, dict):
        if cmdname == SHIP_CMD_THRUST:
            if cmddict.has_key("DIR") and cmddict["DIR"] in [u'L',u'F',u'R',u'B']:
                if cmddict.has_key("DUR") and isinstance(cmddict["DUR"], float) and cmddict["DUR"] >= 0.1:
                    if cmddict.has_key("PER"):
                        if isinstance(cmddict["PER"], float) and 0.1 <= cmddict["PER"] <= 1.0:
                            if cmddict.has_key("BLOCK") and isinstance(cmddict["BLOCK"], bool):
                                return ThrustCommand(ship, cmddict["DIR"], cmddict["DUR"], cmddict["PER"], cmddict["BLOCK"])
                            else:
                                return ThrustCommand(ship, cmddict["DIR"], cmddict["DUR"], cmddict["PER"])
                        else:
                            return "Percent Missing or Should Be Float 0.1 <= Arg <= 1.0"
                    else:
                        return ThrustCommand(ship, cmddict["DIR"], cmddict["DUR"])
                    #eif
                else:
                    return "Duration Missing or Should be Float >= 0.1"
                #eif
            else:
                return "Direction Missing or Should Be L, F, R, or B"
            #eif
        elif cmdname == SHIP_CMD_RADAR:
            if cmddict.has_key("LVL") and isinstance(cmddict["LVL"], int) and 0 < cmddict["LVL"] <= 5:
                if cmddict["LVL"] == 3:
                    if cmddict.has_key("TARGET") and isinstance(cmddict["TARGET"], int) and cmddict["TARGET"] > 0:
                        return RadarCommand(ship, cmddict["LVL"], cmddict["TARGET"])
                    else:
                        return "Target Missing or Should be Positive Int"
                else:
                    return RadarCommand(ship, cmddict["LVL"])
                #eif
            else:
                return "Level Missing or Should be Int 0 < Arg <= 5"
        elif cmdname == SHIP_CMD_BRAKE:
            if cmddict.has_key("PER"):
                if isinstance(cmddict["PER"], float) and 0.0 <= cmddict["PER"] < 1.0:
                    return BrakeCommand(ship, cmddict["PER"])
                else:
                    return "Percent Missing or Should Be Float 0.0 <= Arg < 1.0"
            else:
                return BrakeCommand(ship, 0)
            #eif
        elif cmdname == SHIP_CMD_ALL_STOP:
            return AllStopCommand(ship)
        elif cmdname == SHIP_CMD_WARP:
            if cmddict.has_key("DIST") and isinstance(cmddict["DIST"], float) and cmddict["DIST"] > 0 and cmddict["DIST"] <= WarpCommand.MAXWARPDISTANCE:
                return WarpCommand(ship, cmddict["DIST"])
            elif cmddict.has_key("DIST"):
                return "Distance must be a positive Float less than or equal to " + repr(WarpCommand.MAXWARPDISTANCE)
            else:
                return WarpCommand(ship)
            #eif
        elif cmdname == SHIP_CMD_ROTATE:
            if cmddict.has_key("DEG") and isinstance(cmddict["DEG"], int):
                return RotateCommand(ship, cmddict["DEG"])
            else:
                return "Degrees Missing or Should Be Integer"
            #eif
        elif cmdname == SHIP_CMD_STEER:
            if cmddict.has_key("DEG") and isinstance(cmddict["DEG"], int):
                if cmddict.has_key("BLOCK") and isinstance(cmddict["BLOCK"], bool):
                    return SteerCommand(ship, cmddict["DEG"], cmddict["BLOCK"])
                else:
                    return SteerCommand(ship, cmddict["DEG"])
            else:
                return "Degrees Missing or Should Be Integer"
            #eif
        elif cmdname == SHIP_CMD_IDLE:
            if cmddict.has_key("DUR"):
                if isinstance(cmddict["DUR"], float) and cmddict["DUR"] >= 0.1:
                    return IdleCommand(ship, cmddict["DUR"])
                else:
                    return "Idle Duration Should Be a Positive Float greater than or equal to 0.1"
            else:
                return IdleCommand(ship)
            #eif
        elif cmdname == SHIP_CMD_DEPLOY_LASER_BEACON:
            return DeployLaserBeaconCommand(ship)
        elif cmdname == SHIP_CMD_DESTROY_ALL_BEACONS:
            return DestroyAllLaserBeaconsCommand(ship)
        elif cmdname == SHIP_CMD_TORPEDO:
            if cmddict.has_key("DIR") and cmddict["DIR"] in [u'F',u'B']:
                return FireTorpedoCommand(ship, cmddict["DIR"])
            else:
                return "Firing a torpedo requires a direction 'F'orward or 'B'ackwards"
            #eif
        elif cmdname == SHIP_CMD_SPACEMINE:
            if cmddict.has_key("MODE") and cmddict.has_key("DELAY") and isinstance(cmddict["DELAY"], float) and cmddict["DELAY"] > 0 and cmddict["DELAY"] <= 10:
                if cmddict["MODE"] not in [WorldEntities.SpaceMine.STATIONARY, WorldEntities.SpaceMine.AUTONOMOUS, WorldEntities.SpaceMine.HOMING]:
                    return "Invalid Mine Mode, use 1, 2, or 3"
                elif cmddict["MODE"] == WorldEntities.SpaceMine.AUTONOMOUS:
                    if cmddict.has_key("SPEED") and cmddict.has_key("DUR") and cmddict.has_key("DIR"):
                        if isinstance(cmddict["SPEED"], int) and isinstance(cmddict["DUR"], float) and isinstance(cmddict["DIR"], int):
                            if cmddict["SPEED"] > 0 and cmddict["SPEED"] <= 5:
                                if cmddict["DUR"] > 0 and cmddict["DUR"] <= 10:
                                    return DeploySpaceMineCommand(ship, cmddict["DELAY"], cmddict["MODE"], cmddict["DIR"], cmddict["SPEED"], cmddict["DUR"])
                                else:
                                    return "Must have positive mine duration less than or equal to 10 seconds."
                            else:
                                return "Invalid Mine Speed use 1-5"
                        else:
                            return "Mine paramter type incorrect"
                    else:
                        return "Missing Parameter for Auto Mine"
                else:
                    return DeploySpaceMineCommand(ship, cmddict["DELAY"], cmddict["MODE"])
            else:
                return "Mines need a mode and positive float delay less than or equal to 10 seconds."
        elif cmdname == SHIP_CMD_REPAIR:
            if cmddict.has_key("AMT") and isinstance(cmddict["AMT"], int) and cmddict["AMT"] > 0 and cmddict["AMT"] < 100:
                return RepairCommand(ship, cmddict["AMT"])
            else:
                return "Repair amount must be a positive integer less than 100"
        elif cmdname == SHIP_CMD_SCOOP:
            if cmddict.has_key("SHORT") and isinstance(cmddict["SHORT"], bool):
                if cmddict["SHORT"]:
                    return LowerEnergyScoopCommand(ship)
                else:
                    return LowerEnergyScoopCommand(ship, 2)
            else:
                return "LowerEnergyScoop expects a boolean to indicate if short or long duration is requested"
        elif cmdname == SHIP_CMD_CLOAK:
            if cmddict.has_key("DUR") and isinstance(cmddict["DUR"], float) and cmddict["DUR"] > 0:
                return CloakCommand(ship, cmddict["DUR"])
            else:
                return "Cloak Command Needs a Positive Float for Duration"
            #eif
        elif cmdname == SHIP_CMD_SHIELD:
            if cmddict.has_key("DUR") and isinstance(cmddict["DUR"], float) and cmddict["DUR"] > 0:
                return RaiseShieldsCommand(ship, cmddict["DUR"])
            else:
                return "Shield Command Needs a Positive Float for Duration"
            #eif
        #eif
    else:
        return "Command Format Not Recognized"
    #eif

class ThrustCommand(Command):
    NAME = SHIP_CMD_THRUST

    def __init__(self, obj, direction, duration, power=1.0, block=False):
        super(ThrustCommand, self).__init__(obj, ThrustCommand.NAME, duration, block=block)
        #self.__pow = power
        self.direction = direction
        if direction == 'L':
            self.__off = Vec2d(0, 1)
        elif direction == 'R':
            self.__off = Vec2d(0, -1)
        elif direction == 'F':
            self.__off = Vec2d(-1, 0)
        elif direction == 'B':
            self.__off = Vec2d(1, 0)
        #eif
        self.__off *= power
        self.power = power
        self.energycost = 3 * power

    def getForceVector(self, force, rotation, t):
        return (self.__off * force * t).rotated_degrees(-rotation)
        """
        x = (self.__off * force * t)
        print "org:", x
        x = x.rotated_degrees(-rotation)
        print "rot:", x
        return x
        """

    def execute(self, t):
        self._obj.body.apply_impulse(self.getForceVector(self._obj.thrusterForce, self._obj.rotationAngle, t), (0,0))
        #logging.debug("Executing Thrust on %s for %f", repr(obj), t)
        
    def __repr__(self):
        return super(ThrustCommand, self).__repr__() + " DIR: " + self.direction + " POW: %.2f" % self.power

    def net_repr(self):
        return (ThrustCommand.NAME, {"DIR": self.direction, "DUR":self.timeToLive, "PER":self.power})

class BrakeCommand(Command):
    NAME = SHIP_CMD_BRAKE

    def __init__(self, obj, percent):
        super(BrakeCommand, self).__init__(obj, BrakeCommand.NAME, 15, block=True)
        self.__target = self._obj.body.velocity.length * percent
        if self.__target <= 0.000001:
            self.__target = 0.000001
        self.energycost = 4

    def isComplete(self):
        return self._obj.body.velocity.length <= self.__target

    def execute(self, t):
        amt = (self._obj.thrusterForce / self._obj.mass) * t
        if amt < self._obj.body.velocity.length:
            self._obj.body.velocity.length -= amt
        else:
            self._obj.body.velocity.length = 0.000001
            
class AllStopCommand(OneTimeCommand):
    NAME = SHIP_CMD_ALL_STOP

    def __init__(self, obj):
        if obj.body.velocity.length < 1:
            super(AllStopCommand, self).__init__(obj, AllStopCommand.NAME, True, 1)
        else:
            super(AllStopCommand, self).__init__(obj, AllStopCommand.NAME, True, 5, required=40)
        #eif

    def onetime(self):        
        self._obj.body.velocity = Vec2d(0, 0)
        self._obj.take_damage(max(1, self._obj.health.value / 2), self._obj, True)
            
class WarpCommand(Command):
    """

    __mode (0 = Random, 1 = Directed)
    If directed, wait 1 second.
    If random, rotate to destination.
    Then __stage 0 = play sound and move, go to stage 1
    stage 1 = cooldown timer
    stage 2 = terminate command
    """
    NAME = SHIP_CMD_WARP
    MAXWARPDISTANCE = 400.0

    def __init__(self, obj, distance=0.0):        
        super(WarpCommand, self).__init__(obj, WarpCommand.NAME, 11, block=True, required=10) #maximum duration of warp is 10.5
        self.__stage = 0
        self.__time = 0.0
        self.__initial_distance = distance
        self.energycost = 9
        if distance <= 0.1:
            self.__mode = 0
            self.__dest = (random.randint(-1000,1000), random.randint(-1000,1000))        
            self.__deg = math.degrees(math.atan2(self.__dest[1], self.__dest[0])) - self._obj.rotationAngle
            if self.__deg > 180:
                self.__deg -= 360
            elif self.__deg < -180:
                self.__deg += 360
            #eif
            self.__cooldown = 5
        else:
            self.__mode = 1
            self.__dest = (math.cos(math.radians(-self._obj.rotationAngle)) * distance,
                           math.sin(math.radians(-self._obj.rotationAngle)) * distance)
            self.__cooldown = (int)(distance / 50)

    def isComplete(self):
        return self.__stage == 2

    def execute(self, t):
        self.__time += t
        if self.__mode == 1 and self.__time < 1:
            return
        elif self.__mode == 0 and not (-0.01 < self.__deg < 0.01):
            if self.__deg < 0:
                amt = -self._obj.rotationSpeed * t
                if amt < self.__deg: amt = self.__deg            
            else:
                amt = self._obj.rotationSpeed * t
                if amt > self.__deg: amt = self.__deg
            self.__deg -= amt
            self._obj.rotationAngle += amt
            if self._obj.rotationAngle < 0: self._obj.rotationAngle += 360
            elif self._obj.rotationAngle > 360: self._obj.rotationAngle -= 360
        elif self.__stage == 0:
            self._obj.player.sound = "WARP"
            self._obj.body.position[0] += self.__dest[0]
            self._obj.body.position[1] += self.__dest[1]
            self.__stage = 1
            self.__time = 1
        elif self.__time - 1 >= self.__cooldown:
            self.__stage = 2
            
    def __repr__(self):
        return super(WarpCommand, self).__repr__() + " DEST: " + repr(intpos(self.__dest))
            
    def net_repr(self):
        return (WarpCommand.NAME, {"DIST": self.__initial_distance})

class RotateCommand(Command):
    NAME = SHIP_CMD_ROTATE

    def __init__(self, obj, degrees):
        super(RotateCommand, self).__init__(obj, RotateCommand.NAME, block=True)        
        # Limit to one go around?
        #while degrees > 360:
        #    degrees -= 360
        #while degrees < -360:
        #    degrees += 360
        # Make sure we take optimal rotation
        #if degrees > 180:
        #    degrees -= 360
        #elif degrees < -180:
        #   degrees += 360
        self.__deg = degrees
        self.energycost = 2

    def isComplete(self):
        return -0.01 < self.__deg < 0.01

    def execute(self, t):
        if self.__deg < 0:
            amt = -self._obj.rotationSpeed * t
            if amt < self.__deg: amt = self.__deg            
        else:
            amt = self._obj.rotationSpeed * t
            if amt > self.__deg: amt = self.__deg
        self.__deg -= amt
        self._obj.rotationAngle += amt
        if self._obj.rotationAngle < 0: self._obj.rotationAngle += 360
        elif self._obj.rotationAngle > 360: self._obj.rotationAngle -= 360
        #logging.debug("Executing Rotate on #%d for %f", self._obj.id, t)
        
    def __repr__(self):
        return super(RotateCommand, self).__repr__() + " DEG: %d" % self.__deg

    def net_repr(self):
        return (RotateCommand.NAME, {"DEG":self.__deg})

class SteerCommand(Command):
    NAME = SHIP_CMD_STEER

    def __init__(self, obj, degrees, block=True):
        super(SteerCommand, self).__init__(obj, SteerCommand.NAME, 15, block=block) # 12 should be enough to do a circle

        self.__deg = -degrees # Physics rotations is opposite
        self.orgdeg = -degrees
        self.energycost = 4

    def percent(self):
        return float(self.__deg) / self.orgdeg

    def isComplete(self):
        return -0.01 < self.__deg < 0.01

    def execute(self, t):
        if self.__deg < 0:
            amt = -self._obj.rotationSpeed * t / 4
            if amt < self.__deg: amt = self.__deg
        else:
            amt = self._obj.rotationSpeed * t / 4
            if amt > self.__deg: amt = self.__deg
        self.__deg -= amt
        self._obj.body.velocity.angle_degrees += amt
        #logging.debug("Executing Steering on #%d for %f", self._obj.id, t)
        
    def __repr__(self):
        return super(SteerCommand, self).__repr__() + " DEG: %d" % self.__deg

class IdleCommand(Command):
    NAME = SHIP_CMD_IDLE

    def __init__(self, obj, duration=0.0):
        super(IdleCommand, self).__init__(obj, IdleCommand.NAME, duration, block=True)

    def net_repr(self):
        return (IdleCommand.NAME, {"DUR":self.timeToLive})

class RadarCommand(Command):
    NAME = SHIP_CMD_RADAR

    def __init__(self, obj, level, target=-1):
        self.level = level
        self.target = target
        if level == 1:
            dur = 0.03
        elif level == 2:
            dur = 0.10
        elif level == 3:
            dur = 0.10
        elif level == 4:
            dur = 0.15
        elif level == 5:
            dur = 0.4
        #eif
        self.energycost = 6
        super(RadarCommand, self).__init__(obj, RadarCommand.NAME, dur, block=True)
        
    def __repr__(self):
        return super(RadarCommand, self).__repr__() + " LVL: " + repr(self.level) + " TAR: " + repr(self.target)

    def net_repr(self):
        return (RadarCommand.NAME, {"LVL": self.level, "TAR":self.target})

class DeployLaserBeaconCommand(OneTimeCommand):
    NAME = SHIP_CMD_DEPLOY_LASER_BEACON

    def __init__(self, obj):
        obj.lasernodes.append(intpos(obj.body.position))

        super(DeployLaserBeaconCommand, self).__init__(obj, DeployLaserBeaconCommand.NAME, True, ttl=0.05)

class DestroyAllLaserBeaconsCommand(OneTimeCommand):
    NAME = SHIP_CMD_DESTROY_ALL_BEACONS

    def __init__(self, obj):
        obj.lasernodes = []
        
        super(DestroyAllLaserBeaconsCommand, self).__init__(obj, DestroyAllLaserBeaconsCommand.NAME, True, ttl=0.1)

class FireTorpedoCommand(OneTimeCommand):
    NAME = SHIP_CMD_TORPEDO

    def __init__(self, ship, direction):        
        self.__direction = direction
        super(FireTorpedoCommand, self).__init__(ship, FireTorpedoCommand.NAME, True, 0.2, required=12)
        
    def onetime(self):        
        self._obj.player.sound = "LASER"        
        if self.__direction == 'F':
            self._obj._world.append(WorldEntities.Torpedo(self._obj.body.position, self._obj.rotationAngle, self._obj))
        elif self.__direction == 'B':
            self._obj._world.append(WorldEntities.Torpedo(self._obj.body.position, self._obj.rotationAngle - 180, self._obj))
        #eif

class DeploySpaceMineCommand(OneTimeCommand):
    NAME = SHIP_CMD_SPACEMINE

    def __init__(self, ship, delay, wmode, direction=None, speed=None, duration=None):
        self.__delay = delay
        self.__wmode = wmode
        self.__direction = direction
        self.__speed = speed
        self.__duration = duration
        super(DeploySpaceMineCommand, self).__init__(ship, DeploySpaceMineCommand.NAME, True, 2, required=(22 + self.__wmode * 11))

    def onetime(self):
        self._obj.player.sound = "MINE"
        if self.__wmode == WorldEntities.SpaceMine.STATIONARY:
            self._obj._world.append(WorldEntities.SpaceMine(self._obj.body.position, self.__delay, WorldEntities.SpaceMine.STATIONARY, owner=self._obj))
        elif self.__wmode == WorldEntities.SpaceMine.HOMING:
            self._obj._world.append(WorldEntities.SpaceMine(self._obj.body.position, self.__delay, WorldEntities.SpaceMine.HOMING, owner=self._obj))
        elif self.__wmode == WorldEntities.SpaceMine.AUTONOMOUS:
            self._obj._world.append(WorldEntities.SpaceMine(self._obj.body.position, self.__delay, WorldEntities.SpaceMine.AUTONOMOUS, self.__direction, self.__speed, self.__duration, owner=self._obj))

class RepairCommand(Command):
    NAME = SHIP_CMD_REPAIR

    def __init__(self, obj, amount):                
        super(RepairCommand, self).__init__(obj, RepairCommand.NAME, float(amount) / 4)
        self.left = amount
        self.energycost = 8

    def isComplete(self):
        return -0.01 < self.left < 0.01

    def execute(self, t):
        if self.left > 0:
            amt = 4 * t
            if amt > self.left: amt = self.left
        self.left -= amt
        self._obj.health += amt
        self._obj.shield += amt / self._obj.shieldConversionRate

    def __repr__(self):
        return super(RepairCommand, self).__repr__() + " LEFT: %.1f" % self.left

class LowerEnergyScoopCommand(Command):
    """
    The LowerEnergyScoopCommand deploys an energy collector under your ship.

    If flying through a celestial body (like a Sun, Constellation, or Nebula), this scoop will collect a massive amount of energy.
    It will additionally cause some drag.

    If not in an energy source, this command will drain energy quickly.

    It can be run for a 'short period' of 3 seconds or a 'long period' of 6 seconds.  A long period will restore almost all energy from the initial requirements to start this command.
    """
    NAME = SHIP_CMD_SCOOP

    def __init__(self, obj, short=1):
        super(LowerEnergyScoopCommand, self).__init__(obj, LowerEnergyScoopCommand.NAME, 3 * short, required=4)
        self.energycost = 8

    def execute(self, t):
        bpull = 500
        for body in self._obj.in_celestialbody:
            if isinstance(body, WorldEntities.CelestialBody): # Nebula, BlackHoles, Stars, Constellation
                self._obj.energy += t * 24
                bpull = body.pull
                break
        if self._obj.body.velocity.length > 0.1:
            self._obj.body.velocity.length -= (bpull / self._obj.mass) * t

class CloakCommand(Command):
    NAME = SHIP_CMD_CLOAK

    def __init__(self, obj, duration):
        super(CloakCommand, self).__init__(obj, CloakCommand.NAME, duration, block=False, required=15)
        self.energycost = 2
        if hasattr(self._obj, "player") and self._obj.player != None:
            self._obj.player.sound = "CLOAK"
        self._done = False
        
    def isComplete(self):
        if self._done:
            self._obj.player.sound = "CLOAK"
        return self._done
        
    def execute(self, t):
        if self._obj.commandQueue.containstype(FireTorpedoCommand, True) or self._obj.commandQueue.containstype(RaiseShieldsCommand, True):
            self._done = True

    def net_repr(self):
        return (CloakCommand.NAME, {"DUR": self.timeToLive})

class RaiseShieldsCommand(Command):
    NAME = SHIP_CMD_SHIELD

    def __init__(self, obj, duration):
        super(RaiseShieldsCommand, self).__init__(obj, RaiseShieldsCommand.NAME, duration, required=20)
        self.energycost = 4
        self._done = False
        self._sound = True

    def isComplete(self):
        return self._done

    def execute(self, t):
        if self._sound:
            self._sound = False
            self._obj.player.sound = "SHIELD"
            
        if self._obj.shield.value == 0:
            self._done = True
        elif self._obj.shield.value < self._obj.shield.maximum:
            self._obj.shield += t * self._obj.energyRechargeRate * self._obj.shieldConversionRate
            self._obj.energy -= t * self._obj.shieldConversionRate