
from TestCaseRigging import SBAGUITestCase

import World.WorldMap as WorldMap
from World.WorldEntities import *
from World.WorldCommands import *
from World.AIShips import *

import time

class CombatExerciseTestCases(SBAGUITestCase):
    """
    Test cases for CombatExercise basic game.
    """
    def get_config_filename(self):
        return "test_combatexercise.cfg"

    def test_points_on_torpedo_ship(self):
        """
        Tests that we get points for destroying a ship with a torpedo
        """
        self.ship = AIShip_SetList("Shooter", self.game.world.mid_point(-100), self.game, [
                "IdleCommand(self, 12.0)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 0.1)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 0.1)",
                "FireTorpedoCommand(self, 'F')",
            ])

        self.ship2 = AIShip_SetList("Target", self.game.world.mid_point(50), self.game, [])

        time.sleep(0.2)

        self.assertEqual(len(self.game.world), 2, "Found more than two ships in world")

        time.sleep(11)

        #ensure ship is still there for testing ship timeout function doesn't effect AI ships
        self.assertTrue(self.ship2 in self.game.world, "Target Ship disappeared early")

        time.sleep(5)

        #self.assertFalse(found, "Asteroid Not Destroyed") # TODO: figure out how to determine if ship was destroyed...
        self.assertGreaterEqual(self.ship.player.score, 3, "Ship didn't gain at least 3 points")

    def test_points_on_ram_ship(self):
        """
        Tests that we get points for ramming a whip
        """
        self.ship = AIShip_SetList("Collide", self.game.world.mid_point(-200), self.game, [
                "ThrustCommand(self, 'B', 1.0)",
                "IdleCommand(self, 1.0)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 0.1)",
                #"FireTorpedoCommand(self, 'F')",
                "ThrustCommand(self, 'B', 7.0)",
            ])

        self.ship2 = AIShip_SetList("Target", self.game.world.mid_point(50), self.game, [
                "ThrustCommand(self, 'F', 5.0)",
            ])

        time.sleep(0.4)

        time.sleep(13)

        self.assertGreaterEqual(self.ship.player.score, 2, "Ship didn't gain 2 points")

class CombatExerciseTournamentTestCases(SBAGUITestCase):
    """
    Test cases for Combat Exercise basic game w/ tournamnet.
    """
    def get_config_filename(self):
        return "test_combatexercise.cfg", "test_tournament.cfg", "test_singlegroup.cfg"

    def test_ship_not_readded(self):
        """
        Test that we spawn a new asteroid when a ship joins.
        """
        target = AIShip_SetList("Target", self.game.world.mid_point(50), self.game, [])

        ship = AIShip_SetList("Shooter", self.game.world.mid_point(-100), self.game, [
                "IdleCommand(self, 12.0)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 0.1)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 0.1)",
                "FireTorpedoCommand(self, 'F')",
            ])

        self.assertEqual(len(self.game.world), 0, "Objects in World")

        time.sleep(2.0)

        self.assertFalse(target in self.game.world, "Target ship added to world")
        self.assertFalse(ship in self.game.world, "Ship added to world")

        self.game.round_start()

        time.sleep(3)

        self.assertTrue(target in self.game.world, "Target ship didn't get added to world")
        self.assertTrue(ship in self.game.world, "Ship didn't get added to world")

        time.sleep(0.2)

        self.assertEqual(len(self.game.world), 2, "Found more than two ships in world")

        time.sleep(7)

        #ensure ship is still there for testing ship timeout function doesn't effect AI ships
        self.assertTrue(target in self.game.world, "Target Ship disappeared early")

        time.sleep(6)

        #self.assertFalse(found, "Asteroid Not Destroyed") # TODO: figure out how to determine if ship was destroyed...
        self.assertGreaterEqual(ship.player.score, 3, "Ship didn't gain at least 3 points")
        self.assertEqual(target.player.deaths, 1, "Target didn't get marked as dead")

        #self.assertTrue(target in self.game.world, "Target Ship didn't reappear")
        #self.assertNotAlmostEqual(target.body.position[1], self.game.world.mid_point(50)[1], None, "Target Ship didn't respawn in another location", 2)

        time.sleep(1)

        self.game.round_over()

        time.sleep(1)

        self.assertEqual(len(self.game.world), 0, "Ships still in world after round ended")

        self.assertNotEqual(len(self.game._tmanager._finalgroup), 0, "Ship not added to final group")
        self.assertIn(ship.player, self.game._tmanager._finalgroup, "Correct player not added to final group")


if __name__ == "__main__":
    unittest.main()