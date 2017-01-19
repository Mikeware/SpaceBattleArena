
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

    def test_bauble_spawning(self):
        """
        Test that we spawn a new bauble when a ship joins.
        """
        time.sleep(0.5)

        count = 0
        for obj in self.game.world:
            if isinstance(obj, Bauble):
                count += 1

        self.assertEqual(count, self.cfg.getint("Bauble", "number"), "Not enough initial baubles")

        ship = AIShip_SetList("Nothing", self.game.world.mid_point(0), self.game, [])

        time.sleep(2.0)

        count = 0
        for obj in self.game.world:
            if isinstance(obj, Bauble):
                count += 1

        # +1 for Golden bauble for player
        self.assertEqual(count, self.cfg.getint("Bauble", "number") + self.cfg.getint("Bauble", "spawn_on_player_num") + 1, "Baubles didn't spawn for player")

        time.sleep(4.5)

        count = 0
        for obj in self.game.world:
            if isinstance(obj, Bauble):
                count += 1

        # +1 for Golden bauble for player
        self.assertEqual(count, self.cfg.getint("Bauble", "number") + self.cfg.getint("Bauble", "spawn_on_player_num") + self.cfg.getint("Bauble", "spawn_time_num") + 1, "Baubles didn't spawn on timer")


class HungryHungryBaublesTestCases(SBAGUITestCase):
    """
    Test cases for Hungry Hungry Baubles game.

    No baubles set to spawn automatically.
    """
    def get_config_filename(self):
        return "test_hungryhungrybaubles.cfg"
    
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

        self.assertEqual(ship.player.score, 1, "Player didn't earn point")

        time.sleep(6)

        self.assertEqual(ship.player.score, 1 + 3, "Player didn't earn point gold")

        time.sleep(0.5)
        # move to golden bauble position
        bauble = self.game._HungryHungryBaublesGame__baubles[ship.player.netid]
        ship.body.position = bauble.body.position

        time.sleep(0.5)

        self.assertEqual(ship.player.score, 1 + 3 * 2 + self.cfg.getint("HungryHungryBaubles", "bauble_points_extra"), "Player didn't earn golden bauble points")

        time.sleep(0.5)

        self.assertNotIn(bauble, self.game.world, "Golden Bauble wasn't removed")
        self.assertEqual(len(self.game.world), 4, "Baubles not respawned")


class HungryHungryBaublesTournamentTestCases(SBAGUITestCase):
    """
    Test cases for Hungry Hungry Baubles game w/ tournamnet.
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


class HungryHungryBaublesTournamentWildTestCases(SBAGUITestCase):
    """
    Test cases for Hungry Hungry Baubles game w/ wild tournamnet which takes ties directly to final.
    """
    def get_config_filename(self):
        return "test_hungryhungrybaubles.cfg", "test_tournament_wild_ties.cfg"

    def test_full_wild_tournment_with_ties(self):
        """
        Test we take ties to the final round. Out of 8, will have 4 + wildcard + a tie for 6 out of 8...
        """
        ships = []
        numships = 8
        groups = self.cfg.getint("Tournament", "groups")

        for x in xrange(numships):
            ships.append(AIShip_SetList("Move", self.game.world.mid_point(-500 + x * 100, -500 + x * 100), self.game, [
                "IdleCommand(self, random.randint(1, 5))",
            ]))

        for x in xrange(groups + 1):
            self.assertEqual(len(self.game.world), 0, "Objects in World before round")
            self.assertFalse(self.game.round_get_has_started(), "Game Timer Running")

            self.game.round_start()

            time.sleep(2.0)

            if x == groups:
                self.assertEqual(len(self.game.world), 12, "Found more than 6 ships + baubles in world")

                for player in self.game._tmanager._finalgroup:
                    self.assertTrue(player.object in self.game.world, "Player's Ship not in final tournament")
                    self.assertLess(player.score, 1, "Players shouldn't have score entering final round")

            for i in xrange(x + 2):
                self.game.world.append(Bauble(intpos(self.game.game_get_current_player_list()[i % 2].object.body.position), 1))
                time.sleep(0.5)

            self.assertTrue(self.game.round_get_has_started(), "Game Timer NOT Running")

            time.sleep(7.5)

            leader = None
            for player in self.game.game_get_current_leader_list():
                print player.name, player.score
                if leader == None:
                    leader = player
                #self.assertGreater(player.score, 10, "Each player should have scored")

            time.sleep(7)

            self.assertFalse(self.game.round_get_has_started(), "Game Timer Running After")

            # Round should end
            self.assertEqual(len(self.game.world), 0, "Objects in World after round")

            # No player should have died
            self.assertEqual(self.game.game_get_current_player_list()[0].deaths, 0, "Player died")
            self.assertEqual(self.game.game_get_current_player_list()[1].deaths, 0, "Player died")

            # the leader should still have points
            self.assertGreater(leader.score, 0, "Leader should have scored points")

            if x < groups:
                self.assertEqual(len(self.game._tmanager._finalgroup), x+1, "Ship not added to final group")
                self.assertIn(leader, self.game._tmanager._finalgroup, "Correct player not added to final group")
            else:
                # final round
                self.assertIsNotNone(self.game._tmanager._finalwinner, "Final Winner not marked")
                self.assertEqual(self.game._tmanager._finalwinner, leader, "Incorrect leader chosen")
                pass
            #eif
        #next round

        time.sleep(3)

if __name__ == "__main__":
    unittest.main()