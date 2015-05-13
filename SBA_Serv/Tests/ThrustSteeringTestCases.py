"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2015 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from TestCaseRigging import SBAGUITestCase

import World.WorldMap as WorldMap
from World.WorldEntities import *
from World.WorldCommands import *
from World.AIShips import *

import time


class SteeringTestCase(SBAGUITestCase):

    def test_thrust(self):
        self.ship = AIShip_SetList("Thrust", self.game.world.mid_point(-50), self.game, [
                "ThrustCommand(self, 'B', 7.0)",
            ])        

        time.sleep(5.0)

        self.assertEqual(len(self.ship.commandQueue), 1, "Ship not processing Thurst Command still")
        self.assertNotAlmostEqual(self.game.world.mid_point(-50)[0], self.ship.body.position[0], None, "Ship didn't move in X direction", 1)

    def test_steer_no_velocity(self):
        center = self.game.world.mid_point()
        ship = AIShip_SetList("Steer", center, self.game, [
                "SteerCommand(self, 180)"
            ])
        sang = ship.rotationAngle

        time.sleep(3.0)

        self.assertAlmostEqual(float(ship.body.position[0]), center[0], None, "Ship X not the same as Start", 1)
        self.assertAlmostEqual(float(ship.body.position[1]), center[1], None, "Ship Y not the same as Start", 1)
        self.assertAlmostEqual(ship.rotationAngle, sang, None, "Ship orientation changed.", 1)

    def test_steer_vs_thrust_90(self):
        self.ship = AIShip_SetList("Steer", self.game.world.mid_point(-50), self.game, [
                "ThrustCommand(self, 'B', 3.0)",
                "IdleCommand(self, 3.0)",
                "RotateCommand(self, 90)",
                "SteerCommand(self, 90)",                
                "IdleCommand(self, 5.0)"
            ])        
        self.ship.rotationAngle = 180
        self.ship2 = AIShip_SetList("Thrust", self.game.world.mid_point(50), self.game, [
                "ThrustCommand(self, 'B', 3.0)",
                "IdleCommand(self, 3.0)",
                #"RotateCommand(self, 90)",
                "ThrustCommand(self, 'L', 5.0, 0.5)",
                "ThrustCommand(self, 'F', 5.0, 0.5)",
                "IdleCommand(self, 5.0)"
            ])
        self.ship2.rotationAngle = 0

        time.sleep(0.5)

        ang = abs(self.ship.body.velocity.angle_degrees) # +/-180
        print ang
        
        while len(self.ship.cmdlist) > 0:
            time.sleep(0.02)

        time.sleep(5)

        # angle is minus as our rotation is opposite the physics engine notation
        nang = -self.ship.body.velocity.angle_degrees
        if nang < 0: 
            nang += 360
        print nang # should be 270
        logging.debug("Ship Angle %d, expected %d", nang, ang + 90)
        self.assertAlmostEqual(ang + 90, nang, None, "Ship Didn't Steer 90 Degrees", 3)

    def test_steer_vs_thrust_180(self):
        self.ship = AIShip_SetList("Steer", self.game.world.mid_point(-50), self.game, [
                "ThrustCommand(self, 'B', 3.0)",
                "IdleCommand(self, 3.0)",
                "RotateCommand(self, 180)",
                "SteerCommand(self, 180)",                
                "IdleCommand(self, 5.0)"
            ])
        self.ship.rotationAngle = 180
        
        self.ship2 = AIShip_SetList("Thrust Direct", self.game.world.mid_point(50), self.game, [
                "ThrustCommand(self, 'B', 3.0)",
                "IdleCommand(self, 3.0)",
                "ThrustCommand(self, 'F', 6.0)",
                "IdleCommand(self, 5.0)"
            ])
        self.ship2.rotationAngle = 0

        self.ship3 = AIShip_SetList("Thrust Around", self.game.world.mid_point(0, -150), self.game, [
                "ThrustCommand(self, 'B', 3.0)",
                "IdleCommand(self, 3.0)",
                "ThrustCommand(self, 'L', 5.0, 0.5)",
                "ThrustCommand(self, 'F', 12.0, 0.5)",
                "IdleCommand(self, 12.0)",                
            ])
        self.ship3.rotationAngle = 0

        time.sleep(0.5)

        ang = abs(self.ship.body.velocity.angle_degrees) # +/-180
        print ang
        
        while len(self.ship.cmdlist) > 0 or len(self.ship2.cmdlist) > 0 or len(self.ship3.cmdlist) > 0:
            time.sleep(0.02)

        time.sleep(5)

        # angle is minus as our rotation is opposite the physics engine notation
        nang = -self.ship.body.velocity.angle_degrees
        if nang <= 3: 
            nang += 360
        print nang # should be 360
        logging.debug("Ship Angle %d, expected %d", nang, ang + 180)
        self.assertAlmostEqual(ang + 180, nang, None, "Ship Didn't Steer 180 Degrees", 3)

    def test_steer_vs_thrust_360(self):
        center = self.game.world.mid_point(0)
        self.ship = AIShip_SetList("Steer", center, self.game, [
                "ThrustCommand(self, 'B', 3.0)",
                "IdleCommand(self, 3.0)",
                "SteerCommand(self, 360)",                
                "ThrustCommand(self, 'F', 5.7)",
                "IdleCommand(self, 5.7)",
                "BrakeCommand(self, 0)"
            ])
        self.ship.rotationAngle = 180
        
        while len(self.ship.cmdlist) > 0:
            time.sleep(0.02)

        time.sleep(3)

        print center, self.ship.body.position
        logging.debug("Ship Position %s, expected position %s", repr(self.ship.body.position), repr(center))
        self.assertAlmostEqual(float(self.ship.body.position[0]), center[0], None, "Ship X not the same as Start", 20)
        self.assertAlmostEqual(float(self.ship.body.position[1]), center[1], None, "Ship Y not the same as Start", 3)
