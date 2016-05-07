
from TestCaseRigging import SBAGUITestCase

import World.WorldMap as WorldMap
from World.WorldEntities import *
from World.WorldCommands import *
from World.AIShips import *
from Game.KingOfTheBubble import Bubble

import time

class KingOfTheBubbleSpawnTestCases(SBAGUITestCase):
    """
    Test cases for King of the Bubble game bubble spawning.
    """
    def get_config_filename(self):
        return "test_kingofthebubble_spawn.cfg"

    def test_bubble_spawn(self):
        """
        Test that we spawn a new bauble when a ship joins.
        """
        time.sleep(0.5)

        exists = False
        count = 0
        for obj in self.game.world:
            if isinstance(obj, Bubble):
                count += 1

        self.assertEqual(count, self.cfg.getint("Bubble", "number"), "Not enough initial baubles")

        #ship = AIShip_SetList("Nothing", self.game.world.mid_point(0), self.game, [])

        bubble = self.game.spawnmanager.spawn_entity("Bubble", self.game.world.mid_point(), False)

        time.sleep(2.0)

        count = 0
        for obj in self.game.world:
            if isinstance(obj, Bubble):
                count += 1 

        self.assertEqual(bubble.size - bubble.basesize, self.cfg.getint("Bubble", "points_min"), "Bubble not right size") 
        self.assertEqual(count, self.cfg.getint("Bubble", "number") + 1, "Baubles didn't spawn")
        
        time.sleep(4.5)

        self.assertEqual(bubble.size - bubble.basesize, self.cfg.getint("Bubble", "points_min"), "Bubble not right size") 

        time.sleep(3)

        self.assertLess(bubble.size - bubble.basesize, self.cfg.getint("Bubble", "points_min"), "Bubble should be shrinking") 

        time.sleep(7.0)

        self.assertFalse(bubble in self.game.world, "Bubble shouldn't be in world")

    def test_bubble_points(self):
        """
        Test that we spawn a new bauble when a ship joins.
        """
        time.sleep(0.5)

        exists = False
        count = 0
        for obj in self.game.world:
            if isinstance(obj, Bubble):
                count += 1

        self.assertEqual(count, self.cfg.getint("Bubble", "number"), "Not enough initial baubles")        

        bubble = self.game.spawnmanager.spawn_entity("Bubble", self.game.world.mid_point(), False)

        time.sleep(0.5)

        ship = AIShip_SetList("Nothing", self.game.world.mid_point(0), self.game, [])

        time.sleep(2.0)

        self.assertGreater(ship.player.score, 0, "Player should have points")
        self.assertLess(bubble.size - bubble.basesize, self.cfg.getint("Bubble", "points_min"), "Bubble should be shrinking") 


class KingOfTheBubbleTournamentTestCases(SBAGUITestCase):
    """
    Test cases for Bauble Hunt game w/ tournamnet.
    """
    def get_config_filename(self):
        return "test_kingofthebubble_spawn.cfg", "test_tournament.cfg"

    def test_ship_not_added_until_after_start_bubble(self):
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
        self.assertEqual(len(self.game.world), 1, "Not Ship in world")

    def test_bubble_points_tournament(self):
        """
        Test that we spawn a new bauble when a ship joins.
        """

        ship = AIShip_SetList("Nothing", self.game.world.mid_point(0), self.game, [])
        ship2 = AIShip_SetList("Nothing2", self.game.world.mid_point(0), self.game, [])

        time.sleep(0.5)

        for i in xrange(2):
            self.game.round_start()

            time.sleep(0.5)

            exists = False
            count = 0
            for obj in self.game.world:
                if isinstance(obj, Bubble):
                    count += 1

            self.assertEqual(count, self.cfg.getint("Bubble", "number"), "Not enough initial baubles")

            bubble = self.game.spawnmanager.spawn_entity("Bubble", self.game.world.mid_point(), False)

            time.sleep(2.0)

            #self.assertGreater(ship.player.score, 0, "Player should have points")
            self.assertLess(bubble.size - bubble.basesize, self.cfg.getint("Bubble", "points_min"), "Bubble should be shrinking") 

            time.sleep(0.5)

            self.game.round_over()

            time.sleep(0.5)

if __name__ == "__main__":
    unittest.main()