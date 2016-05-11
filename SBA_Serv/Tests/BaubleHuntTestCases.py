
from TestCaseRigging import SBAGUITestCase

import World.WorldMap as WorldMap
from World.WorldEntities import *
from World.WorldCommands import *
from World.AIShips import *
from Game.BaubleHunt import Bauble, Outpost

import time

class BaubleHuntSpawnTestCases(SBAGUITestCase):
    """
    Test cases for Bauble Hunt game bauble spawning.
    """
    def get_config_filename(self):
        return "test_baublehunt.cfg"

    def test_bauble_base_spawning(self):
        """
        Test that we spawn a new bauble when a ship joins.
        """
        time.sleep(0.5)

        exists = False
        count = 0
        for obj in self.game.world:
            if isinstance(obj, Bauble):
                count += 1
            elif isinstance(obj, Outpost):
                exists = True

        self.assertEqual(count, self.cfg.getint("Bauble", "number"), "Not enough initial baubles")
        self.assertFalse(exists, "Home Base created before player.")

        ship = AIShip_SetList("Nothing", self.game.world.mid_point(0), self.game, [])

        time.sleep(2.0)

        exists = False
        count = 0
        for obj in self.game.world:
            if isinstance(obj, Bauble):
                count += 1 
            elif isinstance(obj, Outpost):
                exists = True

        self.assertEqual(count, self.cfg.getint("Bauble", "number") + self.cfg.getint("Bauble", "spawn_on_player_num"), "Baubles didn't spawn for player")
        self.assertTrue(exists, "Home Base not created for player")

        time.sleep(4.5)

        count = 0
        for obj in self.game.world:
            if isinstance(obj, Bauble):
                count += 1

        self.assertEqual(count, self.cfg.getint("Bauble", "number") + self.cfg.getint("Bauble", "spawn_on_player_num") + self.cfg.getint("Bauble", "spawn_time_num"), "Baubles didn't spawn on timer")


class BaubleHuntTestCases(SBAGUITestCase):
    """
    Test cases for Bauble Hunt game.

    No baubles set to spawn automatically.
    """
    def get_config_filename(self):
        return "test_baublehunt.cfg"
    
    def test_baubles_dont_spawn(self):
        """
        Test to make sure there's no baubles spawning with this configuration file.
        """
        time.sleep(4)

        self.assertEqual(len(self.game.world), 0, "Objects found in world")

    def test_points_on_pickup(self):
        """
        Test that a ship can collect points
        """
        ship = AIShip_SetList("Winner", self.game.world.mid_point(-100), self.game, [
                "IdleCommand(self, 2.0)",
                "ThrustCommand(self, 'B', 4.0)",
            ])

        self.game.world.append(Bauble(self.game.world.mid_point(-50), 1))

        self.game.world.append(Bauble(self.game.world.mid_point(50), 3))

        self.game.world.append(Bauble(self.game.world.mid_point(150), 5))

        time.sleep(5)

        outpost = None
        for obj in self.game.world:
            if isinstance(obj, Outpost):
                outpost = obj

        self.assertIsNotNone(outpost, "Didn't find outpost.")
        self.assertEqual(outpost.owner, ship, "Outpost not correct owner.")
        self.assertEqual(len(ship.player.carrying), 1, "Player didn't pick up bauble.")
        self.assertEqual(ship.player.score, 0, "Player doesn't earn points on pick up 1.")
        #self.assertEqual(ship.player.score, self.cfg.getint("BaubleHunt", "bauble_points_blue"), "Player didn't earn point")

        time.sleep(6)

        self.assertEqual(len(ship.player.carrying), 2, "Player didn't pick up bauble 2.")
        self.assertEqual(ship.player.score, 0, "Player doesn't earn points on pick up 2.")
        #self.assertEqual(ship.player.score, self.cfg.getint("BaubleHunt", "bauble_points_blue") + self.cfg.getint("BaubleHunt", "bauble_points_yellow"), "Player didn't earn point yellow")

        time.sleep(4)

        self.assertEqual(len(ship.player.carrying), 3, "Player didn't pick up bauble 3.")
        self.assertEqual(ship.player.score, 0, "Player doesn't earn points on pick up 3.")

        ship.body.position = outpost.body.position # move to outpost

        time.sleep(0.5)

        self.assertEqual(len(ship.player.carrying), 0, "Player didn't drop off baubles")
        self.assertEqual(ship.player.score, self.cfg.getint("BaubleGame", "bauble_points_blue") + self.cfg.getint("BaubleGame", "bauble_points_yellow") + self.cfg.getint("BaubleGame", "bauble_points_red"), "Player didn't earn bauble points")
        self.assertGreater(len(self.game.world), 7, "Baubles not respawned")


class BaubleHuntTournamentTestCases(SBAGUITestCase):
    """
    Test cases for Bauble Hunt game w/ tournamnet.
    """
    def get_config_filename(self):
        return "test_baublehunt.cfg", "test_tournament.cfg"

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
        self.assertEqual(len(self.game.world), 3, "Not Ship+Bauble+Outpost in world")



if __name__ == "__main__":
    unittest.main()