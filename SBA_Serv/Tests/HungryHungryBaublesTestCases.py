
from TestCaseRigging import SBAGUITestCase

import World.WorldMap as WorldMap
from World.WorldEntities import *
from World.WorldCommands import *
from World.AIShips import *
from Game.HungryHungryBaubles import Bauble

import time

class HungryHungryBaublesBaubleTestCases(SBAGUITestCase):
    """
    Test cases for Hungry Hungry Baubles game bauble spawning.
    """
    def get_config_filename(self):
        return "test_hungryhungrybaubles2.cfg"

    def world_create(self, game, pys):
        return None # use default Hungry Baubles construction

    def test_bauble_spawning(self):
        """
        Test that we spawn a new bauble when a ship joins.
        """
        time.sleep(0.5)

        count = 0
        for obj in self.game.world:
            if isinstance(obj, Bauble):
                count += 1

        self.assertEqual(count, self.cfg.getint("HungryHungryBaubles", "bauble_initial"), "Not enough initial baubles")

        ship = AIShip_SetList("Nothing", self.game.world.mid_point(0), self.game, [])

        time.sleep(2.0)

        count = 0
        for obj in self.game.world:
            if isinstance(obj, Bauble):
                count += 1

        # +1 for Golden bauble for player
        self.assertEqual(count, self.cfg.getint("HungryHungryBaubles", "bauble_initial") + self.cfg.getint("HungryHungryBaubles", "bauble_per_player") + 1, "Baubles didn't spawn for player")

        time.sleep(4.0)

        count = 0
        for obj in self.game.world:
            if isinstance(obj, Bauble):
                count += 1

        # +1 for Golden bauble for player
        self.assertEqual(count, self.cfg.getint("HungryHungryBaubles", "bauble_initial") + self.cfg.getint("HungryHungryBaubles", "bauble_per_player") + self.cfg.getint("HungryHungryBaubles", "bauble_timer_spawns") + 1, "Baubles didn't spawn on timer")


class HungryHungryBaublesTestCases(SBAGUITestCase):
    """
    Test cases for Hungry Hungry Baubles game.

    No baubles set to spawn automatically.
    """
    def get_config_filename(self):
        return "test_hungryhungrybaubles.cfg"

    def world_create(self, game, pys):
        return None
    
    def test_baubles_dont_spawn(self):
        """
        Test to make sure there's no baubles spawning with this configuration file.
        """
        time.sleep(8)

        self.assertEqual(len(self.game.world), 0, "Objects found in world")

    def test_points_on_pickup(self):
        """
        Test that a ship can collect points
        """
        ship = AIShip_SetList("Winner", self.game.world.mid_point(-100), self.game, [
                "IdleCommand(self, 2.0)",
                "ThrustCommand(self, 'B', 3.0)",
            ])

        self.game.world.append(Bauble(self.game.world.mid_point(-50), 1))

        self.game.world.append(Bauble(self.game.world.mid_point(50), 3))

        time.sleep(5)

        self.assertEqual(ship.player.score, self.cfg.getint("HungryHungryBaubles", "bauble_points_blue"), "Player didn't earn point")

        time.sleep(6)

        self.assertEqual(ship.player.score, self.cfg.getint("HungryHungryBaubles", "bauble_points_blue") + self.cfg.getint("HungryHungryBaubles", "bauble_points_gold"), "Player didn't earn point gold")

        time.sleep(0.5)
        # move to golden bauble position
        bauble = self.game._HungryHungryBaublesGame__baubles[ship.player.netid]
        ship.body.position = bauble.body.position

        time.sleep(0.5)

        self.assertEqual(ship.player.score, self.cfg.getint("HungryHungryBaubles", "bauble_points_blue") + self.cfg.getint("HungryHungryBaubles", "bauble_points_gold") * 2 + self.cfg.getint("HungryHungryBaubles", "bauble_points_extra"), "Player didn't earn golden bauble points")

        time.sleep(0.5)

        self.assertNotIn(bauble, self.game.world, "Golden Bauble wasn't removed")
        self.assertEqual(len(self.game.world), 4, "Baubles not respawned")


class HungryHungryBaublesTournamentTestCases(SBAGUITestCase):
    """
    Test cases for Asteroid Miner basic game w/ tournamnet.
    """
    def get_config_filename(self):
        return "test_hungryhungrybaubles.cfg", "test_tournament.cfg"

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
        self.assertEqual(len(self.game.world), 2, "Not Ship+Bauble in world")



if __name__ == "__main__":
    unittest.main()