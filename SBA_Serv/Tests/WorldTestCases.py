"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2015 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from TestCaseRigging import SBAWorldTestCase, SBAGUITestCase
from unittest import TestCase
from World.WorldEntities import *
from World.AIShips import *
from World.WorldMath import PlayerStat

import time

class PlayerStatTestCase(TestCase):
    """
    Basic Test cases for our PlayerStat class.
    """
    def test_max_value(self):
        p = PlayerStat(100, 50)
        p += 100

        self.assertEqual(p, 100, "Adding over max value should equal max value.")

        self.assertEqual(PlayerStat(100, 30) + 30, 60, "value add not equal")

    def test_min_value(self):
        p = PlayerStat(100, 50)
        p -= 100

        self.assertEqual(p, 0, "Subtracting over min value should equal zero.")

    def test_division(self):
        p = PlayerStat(100, 100)
        p /= 2

        self.assertEqual(p, 50, "division not correct.")

        p /= 0.5

        self.assertEqual(p, 100, "division not correct for inverse.")

class WorldTestCase(SBAWorldTestCase):
    """
    Dummy test to create a planet and check it was added to the world of the game.
    """
    def test_planet_exists(self):
        planet = Planet((300, 300))
        self.game.world.append(planet)

        self.assertNotEqual(self.game.world[planet.id], None, 'Planet Missing')

    def test_idle_no_energy(self):
        start = self.game.world.mid_point(50, -50)
        ship = AIShip_SetList("Doomed", start, self.game, [
            "IdleCommand(self, 2.0)"
            ])

        time.sleep(2.2)

        self.assertEqual(ship.energy, 100, "Ship depleated energy doing nothing.")

    def test_regain_energy(self):
        start = self.game.world.mid_point(50, -50)
        ship = AIShip_SetList("Doomed", start, self.game, [
            "IdleCommand(self, 2.0)"
            ])
        
        ship.energy /= 2
        start = ship.energy.value

        time.sleep(2.2)

        self.assertGreater(ship.energy, start, "Ship didn't regain energy over time.")

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

    def test_star_damage(self):
        """
        Tests a ship inside a star takes damage.
        """
        planet = Star(self.game.world.mid_point(0,0), 100, 100) # high pull = faster test for Star
        self.game.world.append(planet)

        start = self.game.world.mid_point(20, -20)
        ship = AIShip_SetList("Doomed", start, self.game, [])        

        start2 = self.game.world.mid_point(-50, 250)
        ship2 = AIShip_SetList("Free", start2, self.game, [])        

        time.sleep(1.0)

        self.failIfAlmostEqual(ship.body.position, start, None, "Doomed ship should have moved", 5)
        self.failIfEqual(ship.health, 100, "Doomed ship did not take damage")

        self.assertEqual(ship2.health, 100, "Free ship took damage")
        self.assertAlmostEqual(ship2.body.position, start2, None, "Free Ship not in same place", 2)

        time.sleep(2.5)

        self.assertFalse(ship in self.game.world, "Doomed Ship not destroyed")

    def test_blackhole_crush(self):
        """
        Tests a ship being destroyed by a blackhole.
        """
        planet = BlackHole(self.game.world.mid_point(0,0), 100, 100)
        self.game.world.append(planet)

        start = self.game.world.mid_point(0, 0)
        ship = AIShip_SetList("Doomed", start, self.game, [])        

        start2 = self.game.world.mid_point(-50, 250)
        ship2 = AIShip_SetList("Free", start2, self.game, [])        

        time.sleep(1)

        #ensure ship is still there for testing ship timeout function doesn't effect AI ships
        self.assertTrue(ship in self.game.world, "Doomed Ship disappeared early")

        time.sleep(8.0)

        #ensure ship is still there for testing ship timeout function doesn't effect AI ships
        self.assertFalse(ship in self.game.world, "Doomed Ship not destroyed")

        #ensure ship is still there for testing ship timeout function doesn't effect AI ships
        self.assertTrue(ship2 in self.game.world, "Free Ship disappeared")
        self.assertAlmostEqual(ship2.body.position, start2, None, "Free Ship not in same place", 2)

    def test_planet_no_gravity(self):
        """
        Tests a ship inside a gravity well vs outside.
        """
        planet = BlackHole(self.game.world.mid_point(0,0), 100, 0)
        self.game.world.append(planet)

        start = self.game.world.mid_point(50, -50)
        ship = AIShip_SetList("Not Doomed", start, self.game, [])        

        time.sleep(5.0)

        self.assertAlmostEqual(ship.body.position, start, None, "Doomed ship shouldn't have moved", 2)

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

    def test_dragon_eats_ship(self):
        """
        Tests a dragon
        """
        start = self.game.world.mid_point(0,80)
        dragon = Dragon(start, 100, 20)
        dragon.body.velocity = Vec2d(0, -5)
        self.game.world.append(dragon)

        speed = dragon.body.velocity.length
        time.sleep(2.5)

        self.failIfAlmostEqual(dragon.body.position, start, None, "Dragon should have moved", 2)

        starts = self.game.world.mid_point(50, 0)
        ship = AIShip_SetList("Doomed", starts, self.game, [])        

        start2 = self.game.world.mid_point(-150, 250)
        ship2 = AIShip_SetList("Free", start2, self.game, [])        

        time.sleep(2.5)

        self.assertGreater(dragon.body.velocity.length, speed, "Dragon not moving faster")

        print dragon.body.velocity.angle_degrees
        self.failIfAlmostEqual(dragon.body.position, start, None, "Dragon should have moved", 5)
        self.assertAlmostEqual(dragon.body.velocity.angle_degrees, -50, None, "Dragon should be facing ship", 15)

        time.sleep(3.5)

        self.failIfEqual(ship.health, 100, "Doomed ship did not take damage")

        self.assertEqual(ship2.health, 100, "Free ship took damage")
        self.assertAlmostEqual(ship2.body.position, start2, None, "Free Ship not in same place", 2)

        time.sleep(5.5)

        self.assertFalse(ship in self.game.world, "Doomed Ship not destroyed")

    def test_ship_shoot_dragon(self):
        """
        Tests that a dragon can take damage from torpedos
        """
        ship = AIShip_SetList("Shooter", self.game.world.mid_point(-100), self.game, [
                "IdleCommand(self, 2)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 0.1)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 0.1)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 0.1)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 0.1)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 0.1)",
                "FireTorpedoCommand(self, 'F')",
            ])

        dragon = Dragon(self.game.world.mid_point(100), 16, 0)
        dragon.body.velocity = Vec2d(0, 0)
        h = dragon.health.value
        self.game.world.append(dragon)

        time.sleep(0.2)

        self.assertEqual(len(self.game.world), 2, "Found more than two objects in world")

        time.sleep(4)

        self.assertLess(dragon.health.value, h, "Dragon didn't take damage")

        #ensure ship is still there for testing ship timeout function doesn't effect AI ships
        self.assertTrue(ship in self.game.world, "Shooter Ship disappeared")

        time.sleep(2)

        self.assertTrue(ship in self.game.world, "Shooter Ship disappeared")
        self.assertFalse(dragon in self.game.world, "Dragon not destroyed")


if __name__ == '__main__':
    unittest.main()
