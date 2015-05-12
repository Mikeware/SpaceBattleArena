"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2015 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from TestCaseRigging import SBAWorldTestCase, SBAGUITestCase
from World.WorldEntities import *
from World.AIShips import *

import time

class WorldTestCase(SBAWorldTestCase):
    """
    Dummy test to create a planet and check it was added to the world of the game.
    """
    def test_planet_exists(self):
        planet = Planet((300, 300))
        self.game.world.append(planet)

        self.assertNotEqual(self.game.world[planet.id], None, 'Planet Missing')


class WorldVisualTestCase(SBAGUITestCase):

    def test_planet_gravity(self):
        """
        Tests a ship inside a gravity well vs outside.
        """
        planet = BlackHole(self.game.world.mid_point(0,0), 100, 100)
        self.game.world.append(planet)

        start = self.game.world.mid_point(50, -50)
        ship = AIShip_SetList("Doomed", start, self.game, [])        

        start2 = self.game.world.mid_point(-50, 250)
        ship2 = AIShip_SetList("Free", start2, self.game, [])        

        time.sleep(5.0)

        self.failIfAlmostEqual(ship.body.position, start, None, "Doomed ship should have moved", 5)
        self.assertAlmostEqual(ship2.body.position, start2, None, "Free Ship not in same place", 2)

    def test_nebula_drag(self):
        """
        Test which has two ships thrust in the same direction, but one slowed by Nebula.
        """
        neb = Nebula(self.game.world.mid_point(100, -160), (384,256))
        self.game.world.append(neb)

        ship = AIShip_SetList("Nebula", self.game.world.mid_point(-100, -100), self.game, [
            "ThrustCommand(self, 'B', 7.0)",
        ])        

        ship2 = AIShip_SetList("Free", self.game.world.mid_point(-100, 100), self.game, [
            "ThrustCommand(self, 'B', 7.0)",
        ])        

        time.sleep(8.0)

        print ship2.body.position[0], " vs ", ship.body.position[0]
        self.failIfAlmostEqual(ship2.body.position[0], ship.body.position[0], None, "Ship Didn't get Slowed Down By Nebula", 15)


if __name__ == '__main__':
    unittest.main()
