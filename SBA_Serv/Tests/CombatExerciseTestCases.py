
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
                "IdleCommand(self, 10.0)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 0.1)",
                "FireTorpedoCommand(self, 'F')",
                "IdleCommand(self, 0.1)",
                "FireTorpedoCommand(self, 'F')",
            ])

        self.ship2 = AIShip_SetList("Target", self.game.world.mid_point(50), self.game, [])

        time.sleep(0.2)

        self.assertEqual(len(self.game.world), 2, "Found more than two ships in world")

        time.sleep(14)

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

if __name__ == "__main__":
    unittest.main()