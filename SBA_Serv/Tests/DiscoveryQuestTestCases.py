
from .TestCaseRigging import SBAGUIWithServerTestCase

import World.WorldMap as WorldMap
from World.WorldEntities import *
from World.WorldCommands import *
from World.AIShips import *
from Game.DiscoveryQuest import Outpost

import time

class DiscoveryQuestWarpOffTestCases(SBAGUIWithServerTestCase):
    """
    Test cases for Discovery Quest Game (needs to be networked, as AIShips currently circumvent server processing rules by executing commands directly #108)
    """
    def get_config_filename(self):
        return "test_discovery_quest.cfg"

    def test_no_nebula_warp(self):
        """
        Test that we can't warp out of a nebula.
        """
        neb = Nebula(self.game.world.mid_point(-100, -100), (384,256))
        self.game.world.append(neb)

        self.request_warp = False
        self.ship = AIShip_Network_Harness("In Nebula", self.__warp_ship)

        self.assertTrue(self.ship.connect(self.cfg.getint("Server", "port")), "Didn't connect to server.")

        time.sleep(2)

        self.assertEqual(len(self.game.world), 3, "Client didn't connect as no object in world.") # Server

        found = False
        self.remote_ship = None
        for obj in self.game.world:
            if isinstance(obj, Ship):
                found = True
                self.remote_ship = obj
                break

        self.assertIsNotNone(self.remote_ship, "Didn't find Server Ship Object in World.")

        self.remote_ship.body.position = self.game.world.mid_point(-100, -100)

        time.sleep(5.0)

        self.assertTrue(self.request_warp, "Client didn't issue Warp Command.")

        print(self.remote_ship.body.position[0])
        self.assertAlmostEqual(self.remote_ship.body.position[0], self.game.world.mid_point(-100, -100)[0], None, "Ship Warped Out of Nebula", 20)
        self.assertAlmostEqual(self.remote_ship.body.position[1], self.game.world.mid_point(-100, -100)[1], None, "Ship Warped Out of Nebula", 20)

        time.sleep(2.0)

    def __warp_ship(self, ship, env):
        self.__env = env
        if env["SHIPDATA"]["TIMEALIVE"] < 1:
            logging.info("Test Case got Callback from Network - Idle")
            return IdleCommand(self.ship, 4.0);

        logging.info("Test Case got Callback from Network - Warp")
        self.request_warp = True
        self.ship.rotationAngle = env["SHIPDATA"]["ROTATION"]
        return WarpCommand(ship)

class DiscoveryQuestWarpOnTestCases(SBAGUIWithServerTestCase):
    """
    Test cases for Discovery Quest Game (needs to be networked, as AIShips currently circumvent server processing rules by executing commands directly #108)
    """
    def get_config_filename(self):
        return "test_discovery_quest2.cfg"

    def test_nebula_warp(self):
        """
        Test that we can warp out of a nebula.
        """
        neb = Nebula(self.game.world.mid_point(-100, -100), (384,256))
        self.game.world.append(neb)

        self.request_warp = False
        self.ship = AIShip_Network_Harness("In Nebula", self.__warp_ship)

        self.assertTrue(self.ship.connect(self.cfg.getint("Server", "port")), "Didn't connect to server.")

        time.sleep(2)

        self.assertEqual(len(self.game.world), 3, "Client didn't connect as no object in world.") # Server

        found = False
        self.remote_ship = None
        for obj in self.game.world:
            if isinstance(obj, Ship):
                found = True
                self.remote_ship = obj
                break

        self.assertIsNotNone(self.remote_ship, "Didn't find Server Ship Object in World.")

        self.remote_ship.body.position = self.game.world.mid_point(-100, -100)

        time.sleep(5.0)

        self.assertTrue(self.request_warp, "Client didn't issue Warp Command.")

        print(self.remote_ship.body.position[0])
        self.assertNotAlmostEqual(self.remote_ship.body.position, self.game.world.mid_point(-100, -100), None, "Ship Didn't Warp Out of Nebula", 20)

        time.sleep(2.0)

    def __warp_ship(self, ship, env):
        self.__env = env
        if env["SHIPDATA"]["TIMEALIVE"] < 1:
            logging.info("Test Case got Callback from Network - Idle")
            return IdleCommand(self.ship, 4.0);

        logging.info("Test Case got Callback from Network - Warp")
        self.request_warp = True
        self.ship.rotationAngle = env["SHIPDATA"]["ROTATION"]
        return WarpCommand(ship, 200.0)

if __name__ == "__main__":
    unittest.main()