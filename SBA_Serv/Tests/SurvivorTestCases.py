
from TestCaseRigging import SBAGUITestCase

import World.WorldMap as WorldMap
from World.WorldEntities import *
from World.WorldCommands import *
from World.AIShips import *

import time

class SurvivorTestCases(SBAGUITestCase):
    """
    Test cases for Survivor basic game.
    """
    def get_config_filename(self):
        return "test_survivor.cfg"

    def test_score_points_or_not(self):
        """
        Test points if a ship doesn't move vs moving
        """
        ship = AIShip_SetList("Move", self.game.world.mid_point(10), self.game, [
                "ThrustCommand(self, 'B', 2.0)",
            ])

        ship2 = AIShip_SetList("Still", self.game.world.mid_point(-50, -100), self.game, [])

        time.sleep(0.2)

        self.assertEqual(len(self.game.world), 2, "Didn't find two ships in world")

        time.sleep(8)

        self.assertEqual(ship2.player.score, 0, "Still Ship Gained Points")

        self.assertGreater(ship.player.score, 5, "Moving ship didn't gain points")

class SurvivorTournamentTestCases(SBAGUITestCase):
    """
    Test cases for Survivor basic game w/ tournamnet.
    """
    def get_config_filename(self):
        return "test_survivor.cfg", "test_tournament.cfg"

    def test_full_tournament(self):
        """
        Test an actual full tournament
        """
        ships = []
        numships = 16
        groups = self.cfg.getint("Tournament", "groups")

        for x in xrange(numships):
            ships.append(AIShip_SetList("Move", self.game.world.mid_point(random.randint(-400, 400), random.randint(-400, 400)), self.game, [
                "RotateCommand(self, random.randint(30, 330))",
                "IdleCommand(self, random.randint(1, 5))",
                "ThrustCommand(self, 'B', 2.0)",
            ]))

        for x in xrange(groups + 1):
            self.assertEqual(len(self.game.world), 0, "Objects in World before round")
            self.assertFalse(self.game.round_get_has_started(), "Game Timer Running")

            self.game.round_start()

            time.sleep(2.0)

            if x == groups:
                for player in self.game._tmanager._finalgroup:
                    self.assertLess(player.score, 1, "Players shouldn't have score entering final round")
                    self.assertTrue(player.object in self.game.world, "Player's Ship not in final tournament")
                    # need to readd a command to ships
                    player.object.add_command("IdleCommand(self, random.randint(1, 5))")
                    player.object.add_command("ThrustCommand(self, 'B', 2.0)")

            self.assertEqual(len(self.game.world), numships / groups, "Found more than tournament group in world")        
            self.assertTrue(self.game.round_get_has_started(), "Game Timer NOT Running")

            time.sleep(25)

            leader = None
            for player in self.game.game_get_current_leader_list():
                print player.name, player.score
                if leader == None:
                    leader = player
                self.assertGreater(player.score, 10, "Each player should have scored")

            time.sleep(7)

            self.assertFalse(self.game.round_get_has_started(), "Game Timer Running After")            

            # Round should end
            self.assertEqual(len(self.game.world), 0, "Objects in World after round")

            if x < groups:
                self.assertEqual(len(self.game._tmanager._finalgroup), x+1, "Ship not added to final group")
                self.assertIn(leader, self.game._tmanager._finalgroup, "Correct player not added to final group")
            else:
                # final round
                self.assertIsNotNone(self.game._tmanager._finalwinners, "Final Winner not marked")
                self.assertIn(leader, self.game._tmanager._finalwinners, "Incorrect leader chosen")
            #eif
        #next round

        time.sleep(3)
        
class SurvivorTournamentWildTestCases(SBAGUITestCase):
    """
    Test cases for Survivor basic game w/ tournamnet.
    """
    def get_config_filename(self):
        return "test_survivor.cfg", "test_tournament_wild.cfg"

    def test_full_wild_tournament(self):
        """
        Test an actual full tournament
        """
        ships = []
        numships = 16
        groups = self.cfg.getint("Tournament", "groups")

        for x in xrange(numships):
            ships.append(AIShip_SetList("Move", self.game.world.mid_point(random.randint(-400, 400), random.randint(-400, 400)), self.game, [
                "RotateCommand(self, random.randint(30, 330))",
                "IdleCommand(self, random.randint(1, 5))",
                "ThrustCommand(self, 'B', 2.0)",
            ]))

        for x in xrange(groups + 2):
            self.assertEqual(len(self.game.world), 0, "Objects in World before round")
            self.assertFalse(self.game.round_get_has_started(), "Game Timer Running")

            self.game.round_start()

            time.sleep(2.0)

            #if x == groups:
                #for player in self.game._tmanager._finalgroup:
                    #self.assertLess(player.score, 1, "Players shouldn't have score entering final round")
                    #self.assertTrue(player.object in self.game.world, "Player's Ship not in final tournament")
                    # need to readd a command to ships
                    #player.object.add_command("IdleCommand(self, random.randint(1, 5))")
                    #player.object.add_command("ThrustCommand(self, 'B', 2.0)")

            #self.assertEqual(len(self.game.world), numships / groups, "Found more than tournament group in world")
            self.assertTrue(self.game.round_get_has_started(), "Game Timer NOT Running")

            time.sleep(10)

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

            if x < groups:
                self.assertEqual(len(self.game._tmanager._finalgroup), x+1, "Ship not added to final group")
                self.assertIn(leader, self.game._tmanager._finalgroup, "Correct player not added to final group")
            else:
                # final round
                #self.assertIsNotNone(self.game._tmanager._finalwinners, "Final Winner not marked")
                #self.assertIn(leader, self.game._tmanager._finalwinners, "Incorrect leader chosen")
                pass
            #eif
        #next round

        time.sleep(3)

if __name__ == "__main__":
    unittest.main()