"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2020 Michael A. Hawker and Brett Wortzman

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

class WorldMathTestCases(TestCase):
    """
    Basic Test cases for the WorldMath functions.
    """
    def test_aligninstances(self):
        self.assertEqual(aligninstances(4, 6.0, float, int), (6.0, 4), "Object values not swapped")
        self.assertEqual(aligninstances(5, 5, int, str), (None, None), "Invalid Type match not returning None, None")
        self.assertEqual(aligninstances("43", 8, str, int), ("43", 8), "Same order values not the same")

    def test_intpos(self):
        x = intpos((4.4, 5.6))
        print(x)
        self.assertEqual(x, (4, 5), "Not rounded correctly")

        x = intpos((6.6, 8.1))
        self.assertIsInstance(x[0], int, "First value not integer")
        self.assertIsInstance(x[1], int, "Second value not integer")

    def test_istypeinlist(self):
        self.assertTrue(istypeinlist(int, [5.0, "asd", 6]), "Failed to find integer.")
        self.assertTrue(istypeinlist(Ship, ["asdfasdf", Ship((0, 0), None)]), "Failed to find ship.")

class WorldTestCase(SBAGUITestCase):
    """
    Dummy test to create a planet and check it was added to the world of the game.
    """
    def test_planet_exists(self):
        planet = Planet((300, 300))
        self.game.world.append(planet)

        self.assertNotEqual(self.game.world[planet.id], None, 'Planet Missing')

    def test_idle_no_energy(self):
        start = self.game.world.mid_point(50, -50)
        ship = AIShip_SetList("Energy", start, self.game, [
            "IdleCommand(self, 2.0)"
            ])

        time.sleep(2.2)

        self.assertEqual(ship.energy, 100, "Ship depleated energy doing nothing.")

    def test_regain_energy(self):
        start = self.game.world.mid_point(50, -50)
        ship = AIShip_SetList("Energy", start, self.game, [
            "IdleCommand(self, 2.0)"
            ])
        
        ship.energy /= 2
        start = ship.energy.value

        time.sleep(2.2)

        self.assertGreater(ship.energy, start, "Ship didn't regain energy over time.")

    def test_ship_respawn(self):
        start = self.game.world.mid_point()
        ship = AIShip_SetList("Doomed", start, self.game, [])

        time.sleep(0.5)

        self.assertIn(ship, self.game.world, "Ship not in world.")

        ship.take_damage(9000)

        time.sleep(0.5)

        self.assertIn(ship, self.game.world, "Ship not in world.")
        self.assertNotEqual(ship.body.position, start, "Ship didn't move") # should move when respawn
        #self.assertTrue(ship.destroyed, "Ship not marked destroyed")

        # TODO, need to respawn ship! Issue with _game_add_ship_for_player?


class WorldNoRespawnTestCase(SBAWorldTestCase):

    def get_config_filename(self):
        return "test_destroyed.cfg"

    def test_ship_no_respawn(self):
        start = self.game.world.mid_point()
        ship = AIShip_SetList("Doomed", start, self.game, [])

        time.sleep(0.5)

        self.assertIn(ship, self.game.world, "Ship not in world.")

        ship.take_damage(9000)

        time.sleep(0.5)

        self.assertNotIn(ship, self.game.world, "Ship still in world.")

class WorldVisualShipExplosionTestCase(SBAGUITestCase):

    def test_explosion_force_no_outside_effect(self):
        """
        Tests that radius of explosion force is enforced.
        """
        start = self.game.world.mid_point(0, -100)
        ship = AIShip_SetList("Free", start, self.game, [])

        time.sleep(2.0)

        self.game.world.causeExplosion(self.game.world.mid_point(0, 0), 50, 2000)

        time.sleep(3.0)

        self.assertAlmostEqual(ship.body.position, start, None, "Free Ship not in same place", 2)

    def test_explosion_force_effect(self):
        """
        Tests that radius has impact on ship movement.
        """
        start = self.game.world.mid_point(0, -100)
        ship = AIShip_SetList("Free", start, self.game, [])

        time.sleep(2.0)

        self.game.world.causeExplosion(self.game.world.mid_point(0, 0), 200, 1000)

        time.sleep(3.0)

        self.assertNotAlmostEqual(ship.body.position, start, None, "Free Ship in same place", 2)

    """
    def test_explosion_force_amount(self):
        
        #Tests that different radii have impact on ship movement.
        
        start = self.game.world.mid_point(-40, -100)
        ship = AIShip_SetList("Far", start, self.game, [])

        start2 = self.game.world.mid_point(40, -50)
        ship2 = AIShip_SetList("Close", start2, self.game, [])

        time.sleep(2.0)

        self.game.world.causeExplosion(self.game.world.mid_point(0, 0), 150, 50)

        time.sleep(3.0)

        self.failIfAlmostEqual(ship.body.position, start, None, "Far Ship in same place", 2)
        self.failIfAlmostEqual(ship2.body.position, start2, None, "Close Ship in same place", 2)

        self.assertGreater(ship2.body.velocity.length, ship.body.velocity.length, "Ship Close should be traveling faster than Ship Far by being closer to blast radius.")
        self.assertGreater(abs(ship.body.position[0] - ship2.body.position[0]), abs(start[0] - start2[0]), "Ships Horizontal Positions have not diverged.")
        self.assertGreater(abs(ship2.body.position - start2), abs(ship.body.position - start), "Ship Close Should be Farther From its Start than Ship Far.")
    """

class WorldVisualShipRespawnTestCase(SBAGUITestCase):

    def test_ship_ram_planet(self):
        """
        Tests a ship raming into a planet should take damange.
        """
        planet = Planet(self.game.world.mid_point(0,0))
        self.game.world.append(planet)

        start = self.game.world.mid_point(300, 0)
        ship = AIShip_SetList("Doomed", start, self.game, [
                "RotateCommand(self, 180)",
                "ThrustCommand(self, 'B', 6.0, 1.0)"
            ])
        health = ship.health.value

        start2 = self.game.world.mid_point(-50, 250)
        ship2 = AIShip_SetList("Free", start2, self.game, [])

        time.sleep(15.0)

        self.assertNotAlmostEqual(ship.body.position, start, None, "Doomed ship should have moved", 5)
        self.assertAlmostEqual(ship2.body.position, start2, None, "Free Ship not in same place", 2)

        self.assertNotAlmostEqual(ship.health.value, health, None, "Doomed ship should have taken damage", 5)
        #self.assertAlmostEqual(planet.body.position, self.game.world.mid_point(0, 0), None, "Planet shouldn't move when hit", 1)

    def test_ship_ram_planet_destroyed(self):
        """
        Tests a ship raming into a planet should take damange.
        """
        planet = Planet(self.game.world.mid_point(0,0))
        self.game.world.append(planet)

        start = self.game.world.mid_point(300, 0)
        ship = AIShip_SetList("Doomed", start, self.game, [
                "RotateCommand(self, 180)",
                "ThrustCommand(self, 'B', 6.0, 1.0)"
            ])
        ship.health /= 2
        health = ship.health.value

        start2 = self.game.world.mid_point(-50, 250)
        ship2 = AIShip_SetList("Free", start2, self.game, [])

        time.sleep(15.0)

        self.assertNotAlmostEqual(ship.body.position, start, None, "Doomed ship should have moved", 5)
        self.assertAlmostEqual(ship2.body.position, start2, None, "Free Ship not in same place", 2)

        self.assertNotAlmostEqual(ship.health.value, health, None, "Doomed ship should have taken damage", 5)
        self.assertEqual(ship.killedby, planet, "Planet not set as killer")
        #self.assertTrue(ship.destroyed, "Doomed not marked destroyed") # Issue with _game_add_ship_for_player dealing with AI_Ships, moving it and resetting... boo

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

        self.assertNotAlmostEqual(ship.body.position, start, None, "Doomed ship should have moved", 5)
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

    def test_planet_torpedo_no_gravity(self):
        """
        Tests torpedos aren't effected by planet's gravity.
        """
        planet = Planet(self.game.world.mid_point(0,0), 256, 100)
        self.game.world.append(planet)

        start = self.game.world.mid_point(0, -100)
        ship = AIShip_SetList("Bully", start, self.game, [
                "RotateCommand(self, 170)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 1.0)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 1.0)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 1.0)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 1.0)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 1.0)",
            ])

        start2 = self.game.world.mid_point(-100, 50)
        ship2 = AIShip_SetList("Doomed", start2, self.game, [])

        self.assertEqual(ship.health.value, ship.health.maximum, "Ship Bully not at full health.")
        self.assertEqual(ship2.health.value, ship2.health.maximum, "Ship Doomed not at full health.")

        time.sleep(12.0)

        self.assertTrue(ship in self.game.world, "Bully Ship missing")
        self.assertTrue(ship2 in self.game.world, "Doomed Ship missing")
        self.assertGreater(ship.health.value, ship.health.maximum / 2, "Ship Bully not at 'full' health.")
        self.assertGreater(ship2.health.value, ship2.health.maximum / 3, "Ship Doomed not at 'full' health.")

        self.assertEqual(len(self.game.world), 3, "Not all objects still in world")
    
    def test_planet_torpedo_gravity(self):
        """
        Tests torpedos are effected by planet's gravity.
        """
        planet = Planet(self.game.world.mid_point(0,0), 256, 100, torpedo = True)
        self.game.world.append(planet)

        start = self.game.world.mid_point(0, -100)
        ship = AIShip_SetList("Bully", start, self.game, [
                "RotateCommand(self, 170)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 1.0)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 1.0)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 1.0)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 1.0)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 1.0)",
            ])

        start2 = self.game.world.mid_point(-100, 50)
        ship2 = AIShip_SetList("Doomed", start2, self.game, [])

        self.assertEqual(ship.health.value, ship.health.maximum, "Ship Bully not at full health.")
        self.assertEqual(ship2.health.value, ship2.health.maximum, "Ship Doomed not at full health.")

        time.sleep(6.0)

        self.assertGreater(ship.health.value, ship.health.maximum / 2, "Ship Bully not at 'full' health.")
        #self.assertLess(ship2.health.value, ship2.health.maximum / 3, "Ship Doomed at 'full' health.")

        self.assertTrue(ship in self.game.world, "Bully Ship missing")
        #self.assertFalse(ship2 in self.game.world, "Doomed Ship not destroyed") # BUGBUG: AI setup overwriting this, should redo how AI-Ships 'respawn'?
        print(ship2.killedby)
        self.assertIsNotNone(ship2.killedby, "Ship Killed By Not Set.")
        self.assertTrue(isinstance(ship2.killedby, Torpedo), "Ship not marked as destroyed by Torpedo.")
        self.assertEqual(ship2.killedby.owner, ship, "Torpedo was not marked as belonging to Ship Bully.")

        time.sleep(6.0)

        # should be 2, but other AI-ship sticks around...?
        self.assertEqual(len(self.game.world), 3, "Not all objects still in world")

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

        print(ship2.body.position[0], " vs ", ship.body.position[0])
        self.assertNotAlmostEqual(ship2.body.position[0], ship.body.position[0], None, "Ship Didn't get Slowed Down By Nebula", 15)

    def test_energy_scoop(self):
        """
        Test two ships, one in Nebula and using Energy Scoop.
        """
        neb = Nebula(self.game.world.mid_point(100, -160), (384,256))
        self.game.world.append(neb)

        ship = AIShip_SetList("Nebula", self.game.world.mid_point(-100, -100), self.game, [
            "ThrustCommand(self, 'B', 7.0)",
            "IdleCommand(self, 2.0)",
            "LowerEnergyScoopCommand(self, 1)",
        ])        

        ship2 = AIShip_SetList("Free", self.game.world.mid_point(-100, 100), self.game, [
            "ThrustCommand(self, 'B', 7.0)",
        ])
        
        ship.energy -= 50
        ship2.energy -= 50

        time.sleep(9.0)

        print(ship2.body.position[0], " vs ", ship.body.position[0])
        self.assertNotAlmostEqual(ship2.body.position[0], ship.body.position[0], None, "Ship Didn't get Slowed Down By Nebula", 15)
        self.assertGreater(ship.energy.value, ship2.energy.value, "Ship didn't get extra energy")
        self.assertAlmostEqual(ship.energy.value, 100, None, "Ship didn't regain all energy", 5)

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

class WorldVisualShipDestroyedTestCase(SBAGUITestCase):

    def get_config_filename(self):
        return "test_destroyed.cfg"

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

        self.assertNotAlmostEqual(ship.body.position, start, None, "Doomed ship should have moved", 5)
        self.assertNotEqual(ship.health, 100, "Doomed ship did not take damage")

        self.assertEqual(ship2.health, 100, "Free ship took damage")
        self.assertAlmostEqual(ship2.body.position, start2, None, "Free Ship not in same place", 2)

        time.sleep(2.5)

        self.assertFalse(ship in self.game.world, "Doomed Ship not destroyed")
        print(ship.killedby)
        self.assertIsNotNone(ship.killedby, "Ship Killed By Not Set.")
        self.assertTrue(isinstance(ship.killedby, Star), "Ship not marked as destroyed by Star.")

    def test_star_damage_ship_destory_ship(self):
        """
        Tests a ship inside a star takes damage.
        """
        planet = Star(self.game.world.mid_point(0,0), 100, 100) # high pull = faster test for Star
        self.game.world.append(planet)

        start = self.game.world.mid_point(30, -20)
        ship = AIShip_SetList("Doomed", start, self.game, [])

        start2 = self.game.world.mid_point(-50, 250)
        ship2 = AIShip_SetList("Free", start2, self.game, [
                "RotateCommand(self, 70)",
                "FireTorpedoCommand(self, 'F')",
                "FireTorpedoCommand(self, 'F')",
                "FireTorpedoCommand(self, 'F')",
                "FireTorpedoCommand(self, 'F')",
        ])

        time.sleep(1.0)

        self.assertNotAlmostEqual(ship.body.position, start, None, "Doomed ship should have moved", 5)
        self.assertNotEqual(ship.health, 100, "Doomed ship did not take damage")

        self.assertEqual(ship2.health, 100, "Free ship took damage")
        self.assertAlmostEqual(ship2.body.position, start2, None, "Free Ship not in same place", 2)

        time.sleep(2.5)

        self.assertFalse(ship in self.game.world, "Doomed Ship not destroyed")
        print(ship.killedby)
        self.assertIsNotNone(ship.killedby, "Ship Killed By Not Set.")
        self.assertTrue(isinstance(ship.killedby, Torpedo), "Ship not marked as destroyed by Torpedo.")
        self.assertEqual(ship.killedby.owner, ship2, "Torpedo was not marked as belonging to Ship.")

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

    def test_blackhole_crush_vs_shield(self):
        """
        Tests a ship not being destroyed by a blackhole if shields raised.
        """
        planet = BlackHole(self.game.world.mid_point(0,0), 100, 100)
        self.game.world.append(planet)

        start = self.game.world.mid_point(0, 0)
        ship = AIShip_SetList("Doomed", start, self.game, [
                "IdleCommand(self, 4.0)",
                "RaiseShieldsCommand(self, 3.0)",
            ])

        start2 = self.game.world.mid_point(-50, 250)
        ship2 = AIShip_SetList("Free", start2, self.game, [])        

        time.sleep(1)

        #ensure ship is still there for testing ship timeout function doesn't effect AI ships
        self.assertTrue(ship in self.game.world, "Doomed Ship disappeared early")

        time.sleep(6.0)

        # should be safe as shield up
        self.assertTrue(ship in self.game.world, "Doomed Ship disappeared to early destroyed")

        time.sleep(2.5) # wait for shield to expire, should be crushed immediately

        self.assertFalse(ship in self.game.world, "Doomed Ship not destroyed")

        self.assertAlmostEqual(ship2.body.position, start2, None, "Free Ship not in same place", 2)

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

        self.assertNotAlmostEqual(dragon.body.position, start, None, "Dragon should have moved", 2)

        starts = self.game.world.mid_point(50, 0)
        ship = AIShip_SetList("Doomed", starts, self.game, [])        

        start2 = self.game.world.mid_point(-150, 250)
        ship2 = AIShip_SetList("Free", start2, self.game, [])        

        time.sleep(2.5)

        self.assertGreater(dragon.body.velocity.length, speed, "Dragon not moving faster")

        print(dragon.body.velocity.angle_degrees)
        self.assertNotAlmostEqual(dragon.body.position, start, None, "Dragon should have moved", 5)
        self.assertAlmostEqual(dragon.body.velocity.angle_degrees, -50, None, "Dragon should be facing ship", 15)

        time.sleep(3.5)

        self.assertNotEqual(ship.health, 100, "Doomed ship did not take damage")

        self.assertEqual(ship2.health, 100, "Free ship took damage")
        self.assertAlmostEqual(ship2.body.position, start2, None, "Free Ship not in same place", 2)

        time.sleep(6.5)

        self.assertFalse(ship in self.game.world, "Doomed Ship not destroyed")

    def test_dragon_stopped(self):
        """
        Tests a dragon
        """
        start = self.game.world.mid_point(0,80)
        dragon = Dragon(start, 100, 20)
        dragon.body.velocity = Vec2d(0, 0)
        self.game.world.append(dragon)

        speed = dragon.body.velocity.length
        time.sleep(1.5)

        starts = self.game.world.mid_point(50, 0)
        ship = AIShip_SetList("Doomed", starts, self.game, [])        

        start2 = self.game.world.mid_point(-150, 250)
        ship2 = AIShip_SetList("Free", start2, self.game, [])        

        time.sleep(2.5)

        self.assertGreater(dragon.body.velocity.length, speed, "Dragon not moving faster")

        print(dragon.body.velocity.angle_degrees)
        self.assertNotAlmostEqual(dragon.body.position, start, None, "Dragon should have moved", 5)
        self.assertAlmostEqual(dragon.body.velocity.angle_degrees, -50, None, "Dragon should be facing ship", 15)

        time.sleep(0.5)

    def test_dragon_vs_cloak(self):
        """
        Tests a dragon and his ability (or lack of) to see cloaked ships
        """
        start = self.game.world.mid_point(0,100)
        dragon = Dragon(start, 100, 20)
        dragon.body.velocity = Vec2d(0, -5)
        self.game.world.append(dragon)

        speed = dragon.body.velocity.length
        direction = dragon.body.velocity.angle_degrees
        time.sleep(2.5)

        self.assertNotAlmostEqual(dragon.body.position, start, None, "Dragon should have moved", 2)

        starts = self.game.world.mid_point(120, 0)
        ship = AIShip_SetList("Cloaked", starts, self.game, [
                "RotateCommand(self, 180)",
                "ThrustCommand(self, 'B', 3.0, 1.0)",
                "CloakCommand(self, 5.0)",
            ])

        start2 = self.game.world.mid_point(-150, 250)
        ship2 = AIShip_SetList("Free", start2, self.game, [])

        time.sleep(2.5)

        self.assertAlmostEqual(dragon.body.velocity.length, speed, None, "Dragon increased speed", 5)
        self.assertAlmostEqual(dragon.body.velocity.angle_degrees, direction, None, "Dragon changed direction", 5)

        print(dragon.body.velocity.angle_degrees)
        self.assertNotAlmostEqual(dragon.body.position, start, None, "Dragon should have moved", 5)

        time.sleep(5)

        print(dragon.body.velocity.angle_degrees)
        self.assertGreater(dragon.body.velocity.length, speed, "Dragon should have increased speed")
        self.assertAlmostEqual(dragon.body.velocity.angle_degrees, -60, None, "Dragon should be facing ship", 15)

        time.sleep(2.5)

        self.assertNotEqual(ship.health, 100, "Doomed ship did not take damage")

        self.assertEqual(ship2.health, 100, "Free ship took damage")
        self.assertAlmostEqual(ship2.body.position, start2, None, "Free Ship not in same place", 2)

        time.sleep(7)

        self.assertFalse(ship in self.game.world, "Doomed Ship not destroyed")

    def test_dragon_vs_cloak_eating(self):
        """
        Tests a dragon and that he can't eat a cloaked ship
        """
        start = self.game.world.mid_point()
        dragon = Dragon(start, 100, 0)
        dragon.body.velocity = Vec2d(0, -0.05)
        self.game.world.append(dragon)

        time.sleep(0.5)

        #self.assertAlmostEqual(dragon.body.position[, start, None, "Dragon shouldn't have moved", 3)

        ship = AIShip_SetList("Cloaked", start, self.game, [
            "IdleCommand(self, 0.5)", # TODO: Looks like get callback before registration so player doesn't exist to play cloak sound?
            "CloakCommand(self, 5.0)",
            ])

        health = ship.health.value
        time.sleep(0.5)

        self.assertEqual(ship.health, health, "Ship lost health")

        time.sleep(3.5)

        self.assertEqual(ship.health, health, "Ship lost health")

        time.sleep(4.5) # wait for decloak

        self.assertNotEqual(ship.health, health, "Ship didn't lose health")

    def test_dragon_ship_escape(self):
        """
        Tests a dragon not catching a ship at full speed.
        """
        start = self.game.world.mid_point(0,80)
        dragon = Dragon(start, 100, 20)
        dragon.body.velocity = Vec2d(0, -5)
        self.game.world.append(dragon)

        speed = dragon.body.velocity.length
        time.sleep(2.5)

        self.assertNotAlmostEqual(dragon.body.position, start, None, "Dragon should have moved", 2)

        starts = self.game.world.mid_point(50, 0)
        ship = AIShip_SetList("Doomed", starts, self.game, [
                "RotateCommand(self, 150)",
                "ThrustCommand(self, 'B', 7.0, 1.0)",
            ])        

        start2 = self.game.world.mid_point(-150, 250)
        ship2 = AIShip_SetList("Free", start2, self.game, [])        

        time.sleep(2.5)

        self.assertGreater(dragon.body.velocity.length, speed, "Dragon not moving faster")

        print(dragon.body.velocity.angle_degrees)
        self.assertNotAlmostEqual(dragon.body.position, start, None, "Dragon should have moved", 5)
        self.assertAlmostEqual(dragon.body.velocity.angle_degrees, -50, None, "Dragon should be facing ship", 15)

        time.sleep(3.5)

        self.assertNotEqual(ship.health, 100, "Doomed ship did not take damage")

        self.assertEqual(ship2.health, 100, "Free ship took damage")
        self.assertAlmostEqual(ship2.body.position, start2, None, "Free Ship not in same place", 2)

        time.sleep(5.5)

        self.assertTrue(ship in self.game.world, "Doomed Ship destroyed")
        self.assertAlmostEqual(dragon.body.velocity.angle_degrees, ship.body.velocity.angle_degrees, None, "Dragon should be headed in about same direction as ship.", 10)

        time.sleep(3.5)

        self.assertAlmostEqual(dragon.body.velocity.length, speed, None, "Dragon should have lost interest", 4)

    def test_all_stop(self):
        start = self.game.world.mid_point(0, 0)
        ship = AIShip_SetListLoop("Doomed", start, self.game, [
                "RotateCommand(self, 15)",
                "ThrustCommand(self, 'B', 4.0, 1.0)",
                "IdleCommand(self, 5.0)",
                "AllStopCommand(self)"
            ])  

        time.sleep(2.0)

        self.assertEqual(ship.health, 100, "Player Not Full Health")
        self.assertEqual(ship.energy, 100, "Player Not Full Energy")

        time.sleep(3.5)

        print(ship.health)
        self.assertAlmostEqual(ship.health.value, 50, None, "Player Health not Halved", 1)
        self.assertLess(ship.energy.value, 100, "Player Energy didn't decrease")

        time.sleep(10.5)

        print(ship.health)
        ship.energy.full() # replenish
        self.assertAlmostEqual(ship.health.value, 25, None, "Player Health not Halved 2", 1)

        time.sleep(10.5)

        print(ship.health)        
        self.assertAlmostEqual(ship.health.value, 13, None, "Player Health not Halved 3", 1)

        time.sleep(10.5)

        print(ship.health)
        ship.energy.full() # replenish
        self.assertAlmostEqual(ship.health.value, 7, None, "Player Health not Halved 4", 1)

        time.sleep(10.5)

        print(ship.health)        
        self.assertAlmostEqual(ship.health.value, 4, None, "Player Health not Halved 5", 1)

        time.sleep(10.5)

        print(ship.health)
        ship.energy.full() # replenish
        self.assertAlmostEqual(ship.health.value, 2, None, "Player Health not Halved 6", 1)

        time.sleep(10.5)

        print(ship.health)        
        self.assertAlmostEqual(ship.health.value, 1, None, "Player Health not Halved 7", 1)

        time.sleep(11)

        print(ship.health)
        self.assertFalse(ship in self.game.world, "Doomed Ship not destroyed")

if __name__ == '__main__':
    unittest.main()
