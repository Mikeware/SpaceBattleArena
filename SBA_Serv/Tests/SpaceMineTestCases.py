"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2016 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from .TestCaseRigging import SBAWorldTestCase, SBAGUITestCase
from unittest import TestCase
from World.WorldEntities import *
from World.AIShips import *
from World.WorldMath import *

import time

class SpaceMineStationaryTestCase(SBAGUITestCase):

    def test_dropping_space_mine(self):
        """
        Tests if a ship can deploy a space mine
        """
        start = self.game.world.mid_point(0, -100)
        ship = AIShip_SetList("Miner", start, self.game, [
                "IdleCommand(self, 2.0)",
                "DeploySpaceMineCommand(self, 4.0, 1)" #Stationary
            ])

        time.sleep(0.5)

        self.assertIn(ship, self.game.world, "Ship not in world.")
        self.assertEqual(len(self.game.world), 1, "More than just ship in world.")

        time.sleep(2.0)

        self.assertIn(ship, self.game.world, "Ship not in world.")
        self.assertEqual(len(self.game.world), 2, "No extra mine in world.")
        self.assertEqual(self.game.world.get_count_of_objects(SpaceMine), 1, "Space Mine didn't spawn.")

        mine = None
        for obj in self.game.world:
            if isinstance(obj, SpaceMine):
                mine = obj
                break

        self.assertAlmostEqual(mine.body.position[0], ship.body.position[0], None, "Mine not near ship", 1)
        self.assertAlmostEqual(mine.body.position[1], ship.body.position[1], None, "Mine not near ship", 1)

    def test_mine_explode(self):
        """
        Tests if a ship can deploy a space mine and then it explodes
        """
        start = self.game.world.mid_point(0, 0)
        ship = AIShip_SetList("Miner", start, self.game, [
                "IdleCommand(self, 2.0)",
                "DeploySpaceMineCommand(self, 2.0, 1)", #Stationary
                "ThrustCommand(self, 'B', 0.5, 1.0)"
            ])

        time.sleep(0.5)

        self.assertIn(ship, self.game.world, "Ship not in world.")
        self.assertEqual(len(self.game.world), 1, "More than just ship in world.")

        time.sleep(2.0)

        self.assertIn(ship, self.game.world, "Ship not in world.")
        self.assertEqual(len(self.game.world), 2, "No extra mine in world.")
        self.assertEqual(self.game.world.get_count_of_objects(SpaceMine), 1, "Space Mine didn't spawn.")

        mine = None
        for obj in self.game.world:
            if isinstance(obj, SpaceMine):
                mine = obj
                break

        self.assertAlmostEqual(mine.body.position[0], ship.body.position[0], None, "Mine not near ship", 6)
        self.assertAlmostEqual(mine.body.position[1], ship.body.position[1], None, "Mine not near ship", 6)

        time.sleep(1.0)

        vel = ship.body.velocity.length

        time.sleep(1.0)

        self.assertIn(ship, self.game.world, "Ship not in world.")
        self.assertEqual(len(self.game.world), 1, "More than just ship in world.")

        self.assertGreater(ship.body.velocity.length, vel + 3, "Mine did not propel ship on explosion.")

        time.sleep(1.0)

    def test_mine_explode_on_impact(self):
        """
        Tests if a ship hits a mine that it explodes
        """
        shipstart = self.game.world.mid_point(100, 0)
        ship = AIShip_SetList("Miner", shipstart, self.game, [
                "RotateCommand(self, 180)",
                "ThrustCommand(self, 'B', 1.5, 1.0)"
            ])

        minestart = self.game.world.mid_point(0, 0)
        mine = SpaceMine(minestart, 0.0, 1)
        self.game.world.append(mine)

        time.sleep(0.5)

        self.assertIn(ship, self.game.world, "Ship not in world.")
        self.assertIn(mine, self.game.world, "Mine not in world.")
        self.assertEqual(len(self.game.world), 2, "More than just ship & mine in world.")

        self.assertGreater(ship.body.position[0], mine.body.position[0], "Ship not to right of mine")
        
        time.sleep(6.0)

        self.assertLess(ship.body.position[0], shipstart[0], "Ship not moving left.")
        pos = ship.body.position[0]

        time.sleep(2.8)

        vel = ship.body.velocity.length
        
        self.assertAlmostEqual(mine.body.position[0], ship.body.position[0], None, "Mine not near ship", 48)
        self.assertAlmostEqual(mine.body.position[1], ship.body.position[1], None, "Mine not near ship", 48)

        time.sleep(2.0)

        self.assertIn(ship, self.game.world, "Ship not in world.")
        self.assertEqual(len(self.game.world), 1, "More than just ship in world.")
        self.assertLess(ship.health.value, ship.health.maximum, "Ship didn't take damage.")

        self.assertGreater(ship.body.velocity.length, vel + 3, "Mine did not propel ship on explosion.")
        self.assertGreater(ship.body.position[0], pos, "Ship not moving towards the right.")

        time.sleep(1.0)


class SpaceMineAutonomousTestCase(SBAGUITestCase):

    def test_autonomous_space_mine(self):
        """
        Tests if an autonomous space mine behaves correctly.
        """
        start = self.game.world.mid_point(0, 0)
        mine = SpaceMine(start, 4.0, 2, 90, 1, 5.0)
        self.game.world.append(mine)

        time.sleep(3.5)

        self.assertIn(mine, self.game.world, "Mine not in world.")
        self.assertEqual(len(self.game.world), 1, "More than just mine in world.")

        self.assertAlmostEqual(mine.body.position[0], start[0], None, "Mine not near center", 1)
        self.assertAlmostEqual(mine.body.position[1], start[1], None, "Mine not near center", 1)

        time.sleep(5.0)

        self.assertLess(mine.body.position[1], start[1], "Mine hasn't moved up")
        self.assertNotAlmostEqual(mine.body.position[1], start[1], None, "Mine near center still", 1)

        self.assertIn(mine, self.game.world, "Mine not in world.")
        self.assertEqual(len(self.game.world), 1, "More than just mine in world.")

        time.sleep(1.5)

        self.assertNotIn(mine, self.game.world, "Mine in world.")
        self.assertEqual(len(self.game.world), 0, "World not empty.")


    def test_autonomous_space_mine_speeds(self):
        """
        Tests if an autonomous space mine behaves correctly.
        """
        start = self.game.world.mid_point(0, 0)

        mines = []

        for i in range(5):
            mines.append(SpaceMine(start, 1.0, 2, 24 + i * 72, i + 1, 10.0))
            self.game.world.append(mines[-1])

        time.sleep(0.5)

        self.assertEqual(len(self.game.world), 5, "Not all mines in world.")

        for i in range(5):
            self.assertAlmostEqual(mines[i].body.position[0], start[0], None, "Mine not near center", 1)
            self.assertAlmostEqual(mines[i].body.position[1], start[1], None, "Mine not near center", 1)

        time.sleep(2.5)

        for i in range(5):
            self.assertNotAlmostEqual(mines[i].body.position[0], start[0], None, "Mine " + repr(i) + " not near center", 1)
            self.assertNotAlmostEqual(mines[i].body.position[1], start[1], None, "Mine " + repr(i) + " not near center", 1)

        time.sleep(1.0)

        s = 0
        for i in range(5):
            self.assertGreater(mines[i].body.velocity.length, s, "Mine " + repr(i) + " speed not greater than previous mine.")
            s = mines[i].body.velocity.length

        time.sleep(0.5)

    def test_mine_explosion_moves_ship(self):
        """
        Tests if a mine can track a ship
        """
        start = self.game.world.mid_point(0, 0)
        ship = AIShip_SetList("Miner", start, self.game, [
                "IdleCommand(self, 2.0)",
                "DeploySpaceMineCommand(self, 8.0, 2, 0, 1, 0.0)", #Auto
                "ThrustCommand(self, 'B', 2.5, 1.0)",
                "IdleCommand(self, 3.0)",
                "ThrustCommand(self, 'F', 2.5, 1.0)"
            ])

        time.sleep(0.5)

        self.assertIn(ship, self.game.world, "Ship not in world.")
        self.assertEqual(len(self.game.world), 1, "More than just ship in world.")

        time.sleep(6.5)

        self.assertIn(ship, self.game.world, "Ship not in world.")
        self.assertEqual(len(self.game.world), 2, "No extra mine in world.")
        self.assertEqual(self.game.world.get_count_of_objects(SpaceMine), 1, "Space Mine didn't spawn.")

        self.assertNotAlmostEqual(ship.body.position[0], start[0], None, "Ship should have moved since start. X", 1)

        time.sleep(2.5)

        self.assertLess(ship.body.velocity.length, 3, "Ship still moving.")

        pos = ship.body.position[0]

        time.sleep(2.5)

        self.assertGreater(ship.body.velocity.length, 3, "Ship not moved by explosion.")
        self.assertGreater(ship.body.position[0], pos, "Ship position hasn't moved. X")

        time.sleep(1.0)


class SpaceMineHomingTestCase(SBAGUITestCase):

    def test_mine_tracks_ship(self):
        """
        Tests if a mine can track a ship
        """
        start = self.game.world.mid_point(0, 0)
        """
        ship = AIShip_SetList("Miner", start, self.game, [
                "IdleCommand(self, 2.0)",
                "DeploySpaceMineCommand(self, 4.0, 3)", #Homing
                "ThrustCommand(self, 'B', 1.5, 1.0)"
            ])
        """

        ship = AIShip_SetList("Miner", start, self.game, [
                "IdleCommand(self, 2.0)",
                "DeploySpaceMineCommand(self, 6.0, 3)", #Homing
                "ThrustCommand(self, 'B', 2.5, 1.0)",
                "IdleCommand(self, 3.0)",
                "ThrustCommand(self, 'F', 2.5, 1.0)"
            ])

        time.sleep(0.5)

        self.assertIn(ship, self.game.world, "Ship not in world.")
        self.assertEqual(len(self.game.world), 1, "More than just ship in world.")

        time.sleep(5.0)

        self.assertIn(ship, self.game.world, "Ship not in world.")
        self.assertEqual(len(self.game.world), 2, "No extra mine in world.")
        self.assertEqual(self.game.world.get_count_of_objects(SpaceMine), 1, "Space Mine didn't spawn.")

        mine = None
        for obj in self.game.world:
            if isinstance(obj, SpaceMine):
                mine = obj
                break

        time.sleep(2.5)

        self.assertAlmostEqual(mine.body.position[0], start[0], None, "Mine moved since start. X", 1)
        self.assertAlmostEqual(mine.body.position[1], start[1], None, "Mine moved since start. Y", 1)

        time.sleep(3.0)

        self.assertGreater(mine.body.position[0], start[0], "Mine has not moved towards ship.")

        time.sleep(1.0)


if __name__ == '__main__':
    unittest.main()
