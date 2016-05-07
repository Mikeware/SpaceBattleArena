
from TestCaseRigging import SBAGUITestCase

import World.WorldMap as WorldMap
from World.WorldEntities import *
from World.WorldCommands import *
from World.AIShips import *

import time

class FindTheMiddleTestCases(SBAGUITestCase):
    """
    Test Cases for Find The Middle Basic Game
    """
    def get_config_filename(self):
        return "test_findthemiddle.cfg"

    def test_no_points_outside(self):
        """
        Check we don't score points outside the circle.
        """
        self.ship = AIShip_SetList("Nothing", self.game.world.mid_point(400), self.game, [])

        time.sleep(4.0)

        self.assertEqual(self.ship.player.score, 0, "Ship gained score")

    def test_max_points_middle(self):
        """
        Check we get the maximum points inside the circle.
        """
        self.ship = AIShip_SetList("Something", self.game.world.mid_point(0), self.game, [])

        time.sleep(4.0)

        print self.ship.player.score
        logging.debug("Ship Score %d, expected 5", self.ship.player.score)
        self.assertEqual(self.ship.player.score, 5, "Ship Didn't Get Score")

    def test_multiple_points_middle(self):
        """
        Check we can score multiple times in the middle of the circle.
        """
        self.ship = AIShip_SetList("Something", self.game.world.mid_point(0), self.game, [])

        time.sleep(4.0)

        print self.ship.player.score
        logging.debug("Ship Score %d, expected 5", self.ship.player.score)
        self.assertEqual(self.ship.player.score, 5, "Ship Didn't Get Score")

        # move player back to center

        self.ship.body.position = self.game.world.mid_point()

        time.sleep(4.0)

        print self.ship.player.score
        logging.debug("Ship Score %d, expected 10", self.ship.player.score)
        self.assertEqual(self.ship.player.score, 10, "Ship doesn't have score of 10")

    def test_ship_reset_score(self):
        """
        Test the reset_score_on_death flag and that our bestscore remains in place.
        """
        self.ship = AIShip_SetList("Something", self.game.world.mid_point(0), self.game, [])

        time.sleep(4.0)

        print self.ship.player.score
        logging.debug("Ship Score %d, expected 5", self.ship.player.score)
        self.assertEqual(self.ship.player.score, 5, "Ship Didn't Get Score")

        # simulate destroy player
        self.game.world.remove(self.ship)

        time.sleep(0.5)

        print self.ship.player.score
        logging.debug("Ship Score %d, expected 0", self.ship.player.score)
        self.assertEqual(self.ship.player.score, 0, "Ship Score Not Reset")

        print self.ship.player.bestscore
        logging.debug("Ship Best score %d, expected 5", self.ship.player.bestscore)
        self.assertEqual(self.ship.player.bestscore, 5, "Ship Best Score Not 5")

class FindTheMiddleTournamentTestCases(SBAGUITestCase):
    """
    Test cases for Find the Middle game w/ tournamnet.
    """
    def get_config_filename(self):
        return "test_findthemiddle.cfg", "test_tournament.cfg"

    def test_find_the_middle_tournament_start(self):
        """
        Test that we can start a find the middle tournament
        """
        ship = AIShip_SetList("Nothing", self.game.world.mid_point(0), self.game, [])

        self.assertEqual(len(self.game.world), 0, "Objects in World")

        time.sleep(2.0)

        self.assertFalse(ship in self.game.world, "Ship added to world")
        
        self.game.round_start()

        time.sleep(3)

        self.assertTrue(ship in self.game.world, "Ship didn't get added to world")

