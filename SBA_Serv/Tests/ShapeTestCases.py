"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2020 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from .TestCaseRigging import SBAGUITestCase

import World.WorldMap as WorldMap
from World.WorldEntities import *
from World.WorldCommands import *
from World.AIShips import *

import time

class ShapesTestCase(SBAGUITestCase):

    def test_rect(self):
        center = self.game.world.mid_point(0)
        self.ship = AIShip_SetListLoop("Rectangle", center, self.game, [
                "DeployLaserBeaconCommand(self)",
                "ThrustCommand(self, 'B', 3.5)",
                "IdleCommand(self, 4)",
                "BrakeCommand(self, 0)",
                "IdleCommand(self, 4)",
                "RotateCommand(self, 90)",
                "DeployLaserBeaconCommand(self)"
            ], 4)
        self.ship.rotationAngle = 90
        
        while len(self.ship.cmdlist) > 0:
            time.sleep(0.02)

        time.sleep(5)

        logging.debug("Ship Position %s, expected position %s", repr(self.ship.body.position), repr(center))
        self.assertAlmostEqual(float(self.ship.body.position[0]), center[0], None, "Ship X not the same as Start", 3)
        self.assertAlmostEqual(float(self.ship.body.position[1]), center[1], None, "Ship Y not the same as Start", 3)

    def test_spiral(self):
        self.ship = AIShip_SetListLoop("Spiral", self.game.world.mid_point(0), self.game, [
                "DeployLaserBeaconCommand(self)",
                "ThrustCommand(self, 'B', 0.1)",
                "SteerCommand(self, 40, False)",
                "RotateCommand(self, 20)",                
                "IdleCommand(self, 0.05*self.loop)",
                "DeployLaserBeaconCommand(self)",
                "DeployLaserBeaconCommand(self)",
                "RotateCommand(self, 20)",                
                "IdleCommand(self, 0.05*self.loop)",
                "DeployLaserBeaconCommand(self)"
            ])
        self.ship.rotationAngle = 90
        
        time.sleep(60)

        x = self.ship.body.position[0]

if __name__ == '__main__':
    unittest.main()