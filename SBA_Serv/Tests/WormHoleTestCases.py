"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2016 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from TestCaseRigging import SBAWorldTestCase, SBAGUITestCase
from unittest import TestCase
from World.WorldEntities import *
from World.AIShips import *
from World.WorldMath import *

import time

class WormHoleVisualShipOneWayTestCase(SBAGUITestCase):

    def test_wormhole_random_location(self):
        """
        Tests if a ship entering a one-way wormhole goes to a random location.
        """
        wormhole = WormHole.spawn(self.game.world, self.cfg, self.game.world.mid_point(0,0))

        start = self.game.world.mid_point(0, -100)
        ship = AIShip_SetList("One", start, self.game, [
                "RotateCommand(self, -90)",
                "ThrustCommand(self, 'B', 5.0, 1.0)"
            ])

        start2 = self.game.world.mid_point(0, 150)
        ship2 = AIShip_SetList("Two", start2, self.game, [
                "RotateCommand(self, 90)",
                "ThrustCommand(self, 'B', 5.0, 1.0)"
            ])

        time.sleep(5.0)

        self.assertAlmostEqual(ship.body.position[0], self.game.world.mid_point(0,0)[0], None, "One ship should be near center. X", 4)
        self.assertAlmostEqual(ship.body.position[1], self.game.world.mid_point(0,0)[1], None, "One ship should be near center. Y", 100)

        time.sleep(1.5)

        self.assertAlmostEqual(ship2.body.position[0], self.game.world.mid_point(0,0)[0], None, "Two ship should be near center. X", 4)
        self.assertAlmostEqual(ship2.body.position[1], self.game.world.mid_point(0,0)[1], None, "Two ship should be near center. Y", 100)

        time.sleep(3.0)

        self.assertGreater(ship.body.position.get_distance(self.game.world.mid_point(0,0)), 128, "One Ship didn't teleport.")

        self.assertGreater(ship2.body.position.get_distance(self.game.world.mid_point(0,0)), 128, "Two Ship didn't teleport.")

    def test_wormhole_torpedo_destroy(self):
        """
        Tests if a ship can destroy another ship through a wormhole...
        """
        wormhole = WormHole(self.game.world.mid_point(0,0), whtype=WormHole.FIXED_POINT, exitpos=self.game.world.mid_point(-200,200))
        self.game.world.append(wormhole)

        start = self.game.world.mid_point(0, -100)
        ship = AIShip_SetList("One", start, self.game, [
                "RotateCommand(self, -90)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 1.0)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 1.0)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 1.0)",
                "FireTorpedoCommand(self, 'F')",
            ])

        start2 = self.game.world.mid_point(-200, 250)
        ship2 = AIShip_SetList("Two", start2, self.game, [])

        self.assertEqual(ship.health.value, ship.health.maximum, "Ship One not at full health.")
        self.assertEqual(ship2.health.value, ship2.health.maximum, "Ship Two not at full health.")

        time.sleep(3.0)

        self.assertEqual(ship.health.value, ship.health.maximum, "Ship One not at full health.")
        self.assertNotEqual(ship2.health.value, ship2.health.maximum, "Ship Two at full health.")

    def test_wormhole_fixed_location(self):
        """
        Tests if a ship entering a own-way wormhole goes to a fixed location.
        """
        wormhole = WormHole(self.game.world.mid_point(0,0), whtype=WormHole.FIXED_POINT, exitpos=self.game.world.mid_point(300,300))
        self.game.world.append(wormhole)

        start = self.game.world.mid_point(100, 0)
        ship = AIShip_SetList("Not Doomed", start, self.game, [
                "RotateCommand(self, 180)",
                "ThrustCommand(self, 'B', 5.0, 1.0)"
            ])

        self.assertAlmostEqual(ship.body.position, start, None, "Not Doomed ship shouldn't have moved", 2)

        time.sleep(5.9)

        self.assertAlmostEqual(ship.body.position[0], self.game.world.mid_point(0,0)[0], None, "Not Doomed ship should be near center. X", 100)
        self.assertAlmostEqual(ship.body.position[1], self.game.world.mid_point(0,0)[1], None, "Not Doomed ship should be near center. Y", 4)

        time.sleep(0.5)

        self.assertAlmostEqual(ship.body.position[0], wormhole.body.position[0]+300, None, "Not Doomed ship didn't teleport to the right location. X", 64)
        self.assertAlmostEqual(ship.body.position[1], wormhole.body.position[1]+300, None, "Not Doomed ship didn't teleport to the right location. Y", 64)

        time.sleep(6.0)

        self.failIfAlmostEqual(ship.body.position[0], wormhole.body.position[0]+300, None, "Not Doomed ship should have continued moving after teleport. X", 96)

    def test_wormhole_travel_back(self):
        """
        Tests if a ship enters a wormhole and returns, that they'll be re-teleported
        """
        wormhole = WormHole(self.game.world.mid_point(0,0), whtype=WormHole.FIXED_POINT, exitpos=self.game.world.mid_point(200,200))
        self.game.world.append(wormhole)

        start = self.game.world.mid_point(100, 0)
        ship = AIShip_SetList("Not Doomed", start, self.game, [
                "RotateCommand(self, 180)",
                "ThrustCommand(self, 'B', 3.0, 1.0)",
                "IdleCommand(self, 3.8)",
                "ThrustCommand(self, 'F', 3.0, 1.0)",
                "IdleCommand(self, 3.0)",
                "RotateCommand(self, -45)",
                "ThrustCommand(self, 'B', 4.0, 1.0)",
            ])

        self.assertAlmostEqual(ship.body.position, start, None, "Not Doomed ship shouldn't have moved", 2)

        time.sleep(5.5)

        self.assertAlmostEqual(ship.body.position[0], self.game.world.mid_point(0,0)[0], None, "Not Doomed ship should be near center. X", 100)
        self.assertAlmostEqual(ship.body.position[1], self.game.world.mid_point(0,0)[1], None, "Not Doomed ship should be near center. Y", 4)

        time.sleep(2.0)

        self.assertAlmostEqual(ship.body.position[0], wormhole.body.position[0]+200, None, "Not Doomed ship didn't teleport to the right location. X", 64)
        self.assertAlmostEqual(ship.body.position[1], wormhole.body.position[1]+200, None, "Not Doomed ship didn't teleport to the right location. Y", 64)

        time.sleep(12.5)

        self.assertAlmostEqual(ship.body.position[0], self.game.world.mid_point(0,0)[0], None, "Not Doomed ship should be near center. X", 100)
        self.assertAlmostEqual(ship.body.position[1], self.game.world.mid_point(0,0)[1], None, "Not Doomed ship should be near center. Y", 100)

        time.sleep(2.5)

        self.assertAlmostEqual(ship.body.position[0], wormhole.body.position[0]+200, None, "Not Doomed ship didn't teleport to the right location. X", 64)
        self.assertAlmostEqual(ship.body.position[1], wormhole.body.position[1]+200, None, "Not Doomed ship didn't teleport to the right location. Y", 64)

        time.sleep(5.5)

        self.failIfAlmostEqual(ship.body.position[0], wormhole.body.position[0]+200, None, "Not Doomed ship should have continued moving after teleport. X", 48)

    def test_wormhole_other_wormhole_one_way(self):
        """
        Tests if a ship entering a one-way wormhole goes to another worm hole, and then that it can't teleport again if it doesn't leave the wormhole area.
        """
        wormhole = WormHole(self.game.world.mid_point(0,0), whtype=WormHole.OTHER_CELESTIALBODY)
        self.game.world.append(wormhole)

        wormhole2 = WormHole(self.game.world.mid_point(-300,-300), whtype=WormHole.FIXED_POINT, exitpos=self.game.world.mid_point(300, -300))
        self.game.world.append(wormhole2)

        # link them!
        wormhole.link_wormhole(wormhole2)

        start = self.game.world.mid_point(100, 0)
        ship = AIShip_SetList("Warped", start, self.game, [
                "RotateCommand(self, 180)",
                "ThrustCommand(self, 'B', 4.0, 1.0)",
                "IdleCommand(self, 4.0)",
                "RotateCommand(self, 180)",
                "ThrustCommand(self, 'B', 10.0, 1.0)"
            ])

        start2 = self.game.world.mid_point(-50, 250)
        ship2 = AIShip_SetList("Free", start2, self.game, [])

        self.assertAlmostEqual(ship.body.position, start, None, "Warped ship shouldn't have moved", 2)

        time.sleep(6.0)

        self.assertAlmostEqual(ship.body.position[0], self.game.world.mid_point(0,0)[0], None, "Warped ship should be near center. X", 100)
        self.assertAlmostEqual(ship.body.position[1], self.game.world.mid_point(0,0)[1], None, "Warped ship should be near center. Y", 4)

        time.sleep(0.5)

        self.assertAlmostEqual(ship.body.position[0], wormhole.body.position[0]-300, None, "Warped ship didn't teleport to the right location. X", 64)
        self.assertAlmostEqual(ship.body.position[1], wormhole.body.position[1]-300, None, "Warped ship didn't teleport to the right location. Y", 64)

        time.sleep(5.0)

        self.failIfAlmostEqual(ship.body.position[0], wormhole.body.position[0]-300, None, "Warped ship didn't move away. X", 64)

        time.sleep(5.0)

        self.assertAlmostEqual(ship.body.position[0], wormhole.body.position[0]-300, None, "Warped ship teleported again. X", 64)
        self.assertAlmostEqual(ship.body.position[1], wormhole.body.position[1]-300, None, "Warped ship teleported again. Y", 64)

        time.sleep(0.5)

        self.assertAlmostEqual(ship2.body.position, start2, None, "Free Ship not in same place", 2)

    def test_wormhole_to_star(self):
        """
        Tests if a ship entering a own-way wormhole goes to another celestial body.
        """
        wormhole = WormHole(self.game.world.mid_point(0,0), whtype=WormHole.OTHER_CELESTIALBODY)
        self.game.world.append(wormhole)

        star = Star(self.game.world.mid_point(350, -150))
        self.game.world.append(star)

        wormhole.link_wormhole(star)

        start = self.game.world.mid_point(100, 0)
        ship = AIShip_SetList("Doomed", start, self.game, [
                "RotateCommand(self, 180)",
                "ThrustCommand(self, 'B', 5.0, 1.0)"
            ])
        health = ship.health.value

        self.assertAlmostEqual(ship.body.position, start, None, "Doomed ship shouldn't have moved", 2)

        time.sleep(5.9)

        self.assertAlmostEqual(ship.body.position[0], self.game.world.mid_point(0,0)[0], None, "Doomed ship should be near center. X", 100)
        self.assertAlmostEqual(ship.body.position[1], self.game.world.mid_point(0,0)[1], None, "Doomed ship should be near center. Y", 4)

        time.sleep(0.5)

        self.assertAlmostEqual(ship.body.position[0], wormhole.body.position[0]+350, None, "Doomed ship didn't teleport to the right location. X", 64)
        self.assertAlmostEqual(ship.body.position[1], wormhole.body.position[1]-150, None, "Doomed ship didn't teleport to the right location. Y", 64)

        time.sleep(6.0)

        self.failIfAlmostEqual(ship.body.position[0], wormhole.body.position[0]+350, None, "Doomed ship should have continued moving after teleport. X", 96)
        self.assertLess(ship.health.value, health - 5, "Doomed ship should have taken damage.")

class WormHoleVisualShipTwoWayTestCase(SBAGUITestCase):

    def test_wormhole_other_wormhole_two_way(self):
        """
        Tests if a ship entering a two-way wormhole goes to the other location, and then can't go back until leaving the area.
        """
        wormhole = WormHole(self.game.world.mid_point(0,0), whtype=WormHole.OTHER_CELESTIALBODY)
        self.game.world.append(wormhole)

        wormhole2 = WormHole(self.game.world.mid_point(300,-300), whtype=WormHole.OTHER_CELESTIALBODY)
        self.game.world.append(wormhole2)

        # link them!
        wormhole.link_wormhole(wormhole2)
        wormhole2.link_wormhole(wormhole)

        start = self.game.world.mid_point(100, 0)
        ship = AIShip_SetList("Warped", start, self.game, [
                "RotateCommand(self, 180)",
                "ThrustCommand(self, 'B', 4.0, 1.0)",
                "IdleCommand(self, 4.5)",
                "RotateCommand(self, 180)",
                "ThrustCommand(self, 'B', 10.0, 1.0)",
                "IdleCommand(self, 10.0)",
                "RotateCommand(self, 180)",
                "ThrustCommand(self, 'B', 10.0, 1.0)"
            ])

        self.assertAlmostEqual(ship.body.position, start, None, "Warped ship shouldn't have moved", 2)

        time.sleep(5.9)

        self.assertAlmostEqual(ship.body.position[0], self.game.world.mid_point(0,0)[0], None, "Warped ship should be near center. X", 100)
        self.assertAlmostEqual(ship.body.position[1], self.game.world.mid_point(0,0)[1], None, "Warped ship should be near center. Y", 4)

        time.sleep(0.5)

        self.assertAlmostEqual(ship.body.position[0], wormhole.body.position[0]+300, None, "Warped ship didn't teleport to the right location. X", 64)
        self.assertAlmostEqual(ship.body.position[1], wormhole.body.position[1]-300, None, "Warped ship didn't teleport to the right location. Y", 64)

        time.sleep(5.0)

        self.failIfAlmostEqual(ship.body.position[0], wormhole.body.position[0]+300, None, "Warped ship didn't move away. X", 64)

        time.sleep(5.0)

        self.assertAlmostEqual(ship.body.position[0], wormhole.body.position[0]+300, None, "Warped ship teleported again. X", 64)
        self.assertAlmostEqual(ship.body.position[1], wormhole.body.position[1]-300, None, "Warped ship teleported again. Y", 64)

        time.sleep(7.0)
        self.assertGreaterEqual(ship.body.position[0], wormhole.body.position[0]+380, "Warped ship not out of range. X")

        time.sleep(12.0)

        self.assertAlmostEqual(ship.body.position[0], wormhole.body.position[0], None, "Warped ship didn't teleport to the right location x2. X", 96)
        self.assertAlmostEqual(ship.body.position[1], wormhole.body.position[1], None, "Warped ship didn't teleport to the right location x2. Y", 96)

        time.sleep(6.0)
        self.failIfAlmostEqual(ship.body.position[0], wormhole.body.position[0], None, "Warped ship didn't move away. X", 96)


# Need to test not warping back until left (or randomly warped into another wormhole?)

if __name__ == '__main__':
    unittest.main()
