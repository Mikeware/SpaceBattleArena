
from .TestCaseRigging import SBAGUITestCase

import World.WorldMap as WorldMap
from World.WorldEntities import *
from World.WorldCommands import *
from World.AIShips import *

import time

class AsteroidMinerTestCases(SBAGUITestCase):
    """
    Test cases for Asteroid Miner basic game.
    """
    def get_config_filename(self):
        return "test_asteroidminer.cfg"

    def test_asteroid_spawned_on_ship(self):
        """
        Test that we spawn a new asteroid when a ship joins.
        """
        self.ship = AIShip_SetList("Nothing", self.game.world.mid_point(0), self.game, [])

        time.sleep(2.0)

        found = False
        for obj in self.game.world:
            if isinstance(obj, Asteroid):
                found = True
                break

        self.assertTrue(found, "No Asteroid Spawned")

        self.assertEqual(len(self.game.world), 2, "Found more than 2 things in world (asteroid, ship expected)")

    def test_asteroid_spawned_on_timer(self):
        """
        Test that we spawn a new asteroid over a period of time.
        """
        time.sleep(12.0)

        found = False
        for obj in self.game.world:
            if isinstance(obj, Asteroid):
                found = True
                break

        self.assertTrue(found, "No Asteroid Spawned")

        self.assertEqual(len(self.game.world), 1, "Found more than 1 asteroid in world")

    def test_points_on_torpedo(self):
        """
        Tests that we get 2 points for destroying an asteroid with a torpedo.
        """
        self.ship = AIShip_SetList("Nothing", self.game.world.mid_point(-100), self.game, [
                "IdleCommand(self, 2.0)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 0.1)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 0.1)",
                "FireTorpedoCommand(self, 'F')",
            ])

        time.sleep(0.2)

        found = None
        for obj in self.game.world:
            if isinstance(obj, Asteroid):
                found = obj
                break
        if found != None:
            self.game.world.remove(obj) # Get rid of initial asteroid

        time.sleep(0.2)

        self.assertEqual(len(self.game.world), 1, "Found more than ship in world")

        time.sleep(0.2)

        a = Asteroid(self.game.world.mid_point())
        a.body.velocity = Vec2d(0,0)
        self.game.world.append(a)

        time.sleep(3)

        found = False
        for obj in self.game.world:
            if isinstance(obj, Asteroid):
                found = True
                break

        self.assertFalse(found, "Asteroid Not Destroyed")
        self.assertEqual(self.ship.player.score, 2, "Ship didn't gain 2 points")

    def test_points_on_ship(self):
        """
        Tests that we get a point for ramming an asteroid with our ship...
        """
        self.ship = AIShip_SetList("Collide", self.game.world.mid_point(-200), self.game, [
                "ThrustCommand(self, 'B', 1.0)",
                "IdleCommand(self, 1.0)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 0.1)",
                #"FireTorpedoCommand(self, 'F')",
                "ThrustCommand(self, 'B', 7.0)",
            ])

        time.sleep(0.4)

        found = None
        for obj in self.game.world:
            if isinstance(obj, Asteroid):
                found = obj
                break
        if found != None:
            self.game.world.remove(obj) # Get rid of initial asteroid

        a = Asteroid(self.game.world.mid_point(), 2000)
        a.body.velocity = Vec2d(-5,0)
        self.game.world.append(a)

        time.sleep(13)

        found = False
        for obj in self.game.world:
            if isinstance(obj, Asteroid) and obj.id == a.id:
                found = True
                break

        self.assertFalse(found, "Asteroid Not Destroyed")
        self.assertEqual(self.ship.player.score, 1, "Ship didn't gain 1 point")

class AsteroidMinerTournamentTestCases(SBAGUITestCase):
    """
    Test cases for Asteroid Miner basic game w/ tournamnet.
    """
    def get_config_filename(self):
        return "test_asteroidminer.cfg", "test_tournament.cfg"

    def test_ship_not_added_until_after_start(self):
        """
        Test that we spawn a new asteroid when a ship joins.
        """
        ship = AIShip_SetList("Nothing", self.game.world.mid_point(0), self.game, [])

        self.assertEqual(len(self.game.world), 0, "Objects in World")

        time.sleep(2.0)

        self.assertFalse(ship in self.game.world, "Ship added to world")

        self.game.round_start()

        time.sleep(3)

        self.assertTrue(ship in self.game.world, "Ship didn't get added to world")



if __name__ == "__main__":
    unittest.main()