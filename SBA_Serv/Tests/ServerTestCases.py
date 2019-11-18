"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2016 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from .TestCaseRigging import SBAServerTestCase, SBAGUIWithServerTestCase
import Server.MWNL2 as MWNL2
from World.AIShips import AIShip_Network_Harness
from World.WorldCommands import *
from Game.HungryHungryBaubles import Bauble

import time
import threading

class ServerConnectTestCase(SBAServerTestCase):

    def test_make_connection(self):
        """
        Basic test case to test lifecycle of a client against the server.
        """
        net = MWNL2.MWNL_Init(self.cfg.getint("Server", "port"), self.callback)
        net.connect("localhost")

        x = 0
        while not net.haveID() and not net.iserror() and x < 5:
            x += 1
            time.sleep(1)

        self.assertEqual(net.iserror(), False, "Network Error on Connect")
        self.assertEqual(net.isconnected(), True, "Didn't Connect to Server")
        self.assertEqual(net.haveID(), True, "Don't have Server ID")
        
        net.close()

        x = 0
        while net.haveID() and not net.iserror() and x < 5:
            x += 1
            time.sleep(1)

        self.assertEqual(net.isconnected(), False, "Didn't Disconnect from Server")

        self.server.disconnectAll()

        time.sleep(2)

        self.assertFalse(self.server.isrunning(), "Server hasn't shut down.")

        # TODO: Do more to Test Server clean-up is ok too. Might help with discovery of root cause of #2

    def test_multiple_clients_server_disconnect(self):
        """
        Test to check multiple client connect/disconnect scenario.
        """

        numclients = 40

        self.ships = []

        for x in range(numclients):
            self.ships.append(AIShip_Network_Harness("Add Me " + str(x), self.__bad_thrust_ship))

            self.assertTrue(self.ships[-1].connect(self.cfg.getint("Server", "port")), "Didn't connect to server.")
        #next

        time.sleep(5)

        self.game.end()

        # server closes all connections
        self.server.disconnectAll()

        time.sleep(10)

        print(threading.enumerate())

        self.assertFalse(self.server.isrunning(), "Server still running after disconnect.")

        for x in range(numclients):
            self.assertFalse(self.ships[x].isconnected(), "Client still connected to server after disconnect.")

        print(threading.enumerate())
        self.assertEqual(len(threading.enumerate()), 1, "More than main thread running.")

    def __bad_thrust_ship(self, ship, env):
        logging.info("Test Case got Callback from Network")
        x = random.randint(1, 10)
        if x > 7:
            return ThrustCommand(ship, 'B', 1.0, 0.5)
        elif x > 3:
            time.sleep(3)
            return RotateCommand(ship, 120)
        return IdleCommand(ship, 10)

    def callback(self, sender, cmd):
        pass


class ServerEnableCommandsTestCase(SBAServerTestCase):

    def get_config_filename(self):
        return "test_server_enable.cfg"

    def test_rotate_ship_command_enabled(self):
        """
        Test that a ship using Rotate works with enable_commands Server property
        """
        self.__env = None

        self.ship = AIShip_Network_Harness("Rotator", self.__rotate_ship)

        self.assertTrue(self.ship.connect(self.cfg.getint("Server", "port")), "Didn't connect to server.")

        time.sleep(2)

        self.assertIsNotNone(self.__env, "Never received environment.")
        
        ang = self.__env["SHIPDATA"]["ROTATION"]

        time.sleep(2)

        self.assertEqual(self.ship.errors, 0, "Ship received error message.")

        self.assertNotEqual(ang, self.__env["SHIPDATA"]["ROTATION"], "Angle didn't change over time.")

        self._endServer() # Note, Ship will still be visible as we're not removing it from world in this test.

        time.sleep(3)

        self.assertFalse(self.ship.isconnected(), "Client still connected to server after disconnect.")

    def test_thrust_ship_command_enabled(self):
        """
        Test that a ship using Thrust works with enable_commands Server property
        """
        self.__env = None

        self.ship = AIShip_Network_Harness("Thruster", self.__thrust_ship)

        self.assertTrue(self.ship.connect(self.cfg.getint("Server", "port")), "Didn't connect to server.")

        time.sleep(2)

        self.assertIsNotNone(self.__env, "Never received environment.")
        
        pos = self.__env["SHIPDATA"]["POSITION"]

        time.sleep(2)

        self.assertEqual(self.ship.errors, 0, "Ship received error message.")

        self.assertNotEqual(pos, self.__env["SHIPDATA"]["POSITION"], "Position didn't change over time.")

        self._endServer() # Note, Ship will still be visible as we're not removing it from world in this test.

        time.sleep(3)

        self.assertFalse(self.ship.isconnected(), "Client still connected to server after disconnect.")

    def test_other_ship_command_enabled_fail(self):
        """
        Test that a ship using a different command doesn't work with enable_commands Server property
        """
        self.__env = None

        self.ship = AIShip_Network_Harness("Idle", self.__idle_ship)

        self.assertTrue(self.ship.connect(self.cfg.getint("Server", "port")), "Didn't connect to server.")

        time.sleep(2)

        self.assertIsNotNone(self.__env, "Didn't received initial environment.")
        
        time.sleep(2)

        self.assertGreater(self.ship.errors, 0, "Ship didn't receive error message.")

        self._endServer() # Note, Ship will still be visible as we're not removing it from world in this test.

        time.sleep(3)

        self.assertFalse(self.ship.isconnected(), "Client still connected to server after disconnect.")

    def __rotate_ship(self, ship, env):
        logging.info("Test Case got Callback from Network for Rotate Ship")
        self.__env = env
        return RotateCommand(ship, 6)

    def __thrust_ship(self, ship, env):
        logging.info("Test Case got Callback from Network for Thrust Ship")
        self.__env = env
        return ThrustCommand(ship, 'B', 4.0, 1.0, True)

    def __idle_ship(self, ship, env):
        logging.info("Test Case got Callback from Network for Idle Ship")
        self.__env = env
        return IdleCommand(ship, 1.0)


class ServerDisableCommandsTestCase(SBAServerTestCase):

    def get_config_filename(self):
        return "test_server_disable.cfg"

    def test_rotate_ship_command_disable_fail(self):
        """
        Test that a ship using Rotate doesn't work with disable_commands Server property
        """
        self.__env = None

        self.ship = AIShip_Network_Harness("Rotator", self.__rotate_ship)

        self.assertTrue(self.ship.connect(self.cfg.getint("Server", "port")), "Didn't connect to server.")

        time.sleep(2)

        self.assertIsNotNone(self.__env, "Never received environment.")
        
        ang = self.__env["SHIPDATA"]["ROTATION"]

        time.sleep(2)

        self.assertGreater(self.ship.errors, 0, "Ship didn't receive error message.")

        self.assertEqual(ang, self.__env["SHIPDATA"]["ROTATION"], "Angle changed over time.")

        self._endServer() # Note, Ship will still be visible as we're not removing it from world in this test.

        time.sleep(3)

        self.assertFalse(self.ship.isconnected(), "Client still connected to server after disconnect.")

    def test_thrust_ship_command_disabled(self):
        """
        Test that a ship using Thrust works with disable_commands Server property
        """
        self.__env = None

        self.ship = AIShip_Network_Harness("Thruster", self.__thrust_ship)

        self.assertTrue(self.ship.connect(self.cfg.getint("Server", "port")), "Didn't connect to server.")

        time.sleep(2)

        self.assertIsNotNone(self.__env, "Never received environment.")
        
        pos = self.__env["SHIPDATA"]["POSITION"]

        time.sleep(2)

        self.assertEqual(self.ship.errors, 0, "Ship received error message.")

        self.assertNotEqual(pos, self.__env["SHIPDATA"]["POSITION"], "Position didn't change over time.")

        self._endServer() # Note, Ship will still be visible as we're not removing it from world in this test.

        time.sleep(3)

        self.assertFalse(self.ship.isconnected(), "Client still connected to server after disconnect.")

    def test_other_ship_command_disable(self):
        """
        Test that a ship using a different command works with disable_commands Server property
        """
        self.__env = None

        self.ship = AIShip_Network_Harness("Idle", self.__idle_ship)

        self.assertTrue(self.ship.connect(self.cfg.getint("Server", "port")), "Didn't connect to server.")

        time.sleep(2)

        self.assertIsNotNone(self.__env, "Didn't received initial environment.")
        
        time.sleep(2)

        self.assertEqual(self.ship.errors, 0, "Ship received error message.")

        self._endServer() # Note, Ship will still be visible as we're not removing it from world in this test.

        time.sleep(3)

        self.assertFalse(self.ship.isconnected(), "Client still connected to server after disconnect.")

    def __rotate_ship(self, ship, env):
        logging.info("Test Case got Callback from Network for Rotate Ship")
        self.__env = env
        return RotateCommand(ship, 6)

    def __thrust_ship(self, ship, env):
        logging.info("Test Case got Callback from Network for Thrust Ship")
        self.__env = env
        return ThrustCommand(ship, 'B', 4.0, 1.0, True)

    def __idle_ship(self, ship, env):
        logging.info("Test Case got Callback from Network for Idle Ship")
        self.__env = env
        return IdleCommand(ship, 1.0)


class ServerGUISingleShipRemoteTestCase(SBAGUIWithServerTestCase):

    def get_config_filename(self):
        return "test_server.cfg"

    def test_add_host_close_ship(self):
        """
        Test adding a networked client and having the server close connection
        """
        self.__env = None

        self.ship = AIShip_Network_Harness("Add Me", self.__rotate_ship)

        self.assertTrue(self.ship.connect(self.cfg.getint("Server", "port")), "Didn't connect to server.")

        time.sleep(2)

        self.assertIsNotNone(self.__env, "Never received environment.")
        
        ang = self.__env["SHIPDATA"]["ROTATION"]

        time.sleep(2)

        self.assertNotEqual(ang, self.__env["SHIPDATA"]["ROTATION"], "Angle didn't change over time.")

        self._endServer() # Note, Ship will still be visible as we're not removing it from world in this test.

        time.sleep(3)

        self.assertFalse(self.ship.isconnected(), "Client still connected to server after disconnect.")

    def test_add_client_disconnect_ship(self):
        """
        Pure client connect/disconnect test running single command
        """
        self.__env = None

        self.ship = AIShip_Network_Harness("Add Me", self.__rotate_ship)

        self.assertTrue(self.ship.connect(self.cfg.getint("Server", "port")), "Didn't connect to server.")

        time.sleep(2)

        self.assertIsNotNone(self.__env, "Never received environment.")
        
        ang = self.__env["SHIPDATA"]["ROTATION"]

        time.sleep(2)

        self.assertNotEqual(ang, self.__env["SHIPDATA"]["ROTATION"], "Angle didn't change over time.")

        self.ship.disconnect()

        time.sleep(2)

        self.assertFalse(self.ship.isconnected(), "Client still connected to server after disconnect.")

    def test_add_host_remove_ship(self):
        """
        Test disconnect_on_death setting by remove object from world on server
        """
        self.__env = None

        self.ship = AIShip_Network_Harness("Add Me", self.__rotate_ship)

        self.assertTrue(self.ship.connect(self.cfg.getint("Server", "port")), "Didn't connect to server.")

        time.sleep(2)

        self.assertIsNotNone(self.__env, "Never received environment.")
        
        ang = self.__env["SHIPDATA"]["ROTATION"]

        time.sleep(2)

        self.assertNotEqual(ang, self.__env["SHIPDATA"]["ROTATION"], "Angle didn't change over time.")

        #SERVER
        self.assertEqual(len(self.game.world), 1, "More than one object in the world.")
        for obj in self.game.world:
            self.game.world.remove(obj) # we turned disconnect on death on to make this also disconnect

        time.sleep(3)

        self.assertEqual(len(self.game.world), 0, "Ship still in world.")
        #end SERVER

        self.assertFalse(self.ship.isconnected(), "Client still connected to server after disconnect.")

    def test_client_removed_on_error(self):
        """
        Test disconnect_on_death setting by remove object from world on server
        """
        self.__env = None

        self.ship = AIShip_Network_Harness("Add Me", self.__error_ship)

        self.assertTrue(self.ship.connect(self.cfg.getint("Server", "port")), "Didn't connect to server.")

        time.sleep(2)

        self.assertEqual(len(self.game.world), 1, "Client didn't connect as no object in world.") # Server

        self.assertIsNotNone(self.__env, "Never received environment.")
       
        # Wait for server to remove
        time.sleep(12)
        
        self.assertEqual(len(self.game.world), 0, "Ship still in world.") #SERVER

        time.sleep(3)

        self.assertFalse(self.ship.isconnected(), "Client still connected after failure?")

    def __rotate_ship(self, ship, env):
        logging.info("Test Case got Callback from Network")
        self.__env = env
        return RotateCommand(ship, 6)

    def __error_ship(self, ship, env):
        self.__env = env
        time.sleep(1)
        # want client thread to die to test server, seems to not effect test, which is kind of a bad thing, but we'll exploit it for now
        # means we should be more prudent with testing for those cases with asserts to prevent bad tests.
        raise Exception


class ServerGUITwoShipRemoteTestCase(SBAGUIWithServerTestCase):

    def get_config_filename(self):
        return "test_server.cfg"

    def test_add_two_ships_and_disconnect(self):
        """
        Tests adding two networked clients to a server and that they can disconnect
        """
        self.__env_target = None
        self.__env_radar = None

        self.targetship = AIShip_Network_Harness("Target", self.__target_ship)
        self.assertTrue(self.targetship.connect(self.cfg.getint("Server", "port")), "Target Didn't connect to server.")

        self.radarship = AIShip_Network_Harness("Radar", self.__radar_ship)
        self.assertTrue(self.radarship.connect(self.cfg.getint("Server", "port")), "Radar Didn't connect to server.")

        time.sleep(0.25)

        self.assertTrue(self.targetship.isconnected(), "Target Client not connected to server.")
        self.assertTrue(self.radarship.isconnected(), "Radar Client not connected to server.")

        self.assertIsNotNone(self.__env_target, "Target Never received environment.")
        self.assertIsNotNone(self.__env_radar, "Radar Never received environment.")

        self.assertEqual(len(self.game.world), 2, "Both Ships not in world.")

        tship = None
        rship = None

        for obj in self.game.world:
            if "Target" in obj.player.name:
                tship = obj
            elif "Radar" in obj.player.name:
                rship = obj
        
        self.assertIsNotNone(tship, "Couldn't find Target Ship")
        self.assertIsNotNone(rship, "Couldn't find Radar Ship")

        time.sleep(0.25)

        self._endServer() # Note, Ship will still be visible as we're not removing it from world in this test.

        time.sleep(2)

        self.assertFalse(self.targetship.isconnected(), "Target Client still connected to server after disconnect.")
        self.assertFalse(self.radarship.isconnected(), "Radar Client still connected to server after disconnect.")

        self.assertEqual(len(self.game.world), 0, "Objects still in world.")

        time.sleep(0.5)

    def __target_ship(self, ship, env):
        logging.info("Test Case got Callback from Network for Target Ship")
        self.__env_target = env
        return RotateCommand(ship, 240)

    def __radar_ship(self, ship, env):
        logging.info("Test Case got Callback from Network for Radar Ship")
        self.__env_radar = env
        return RotateCommand(ship, 240)


class ServerGUITournamentRemoteTestCase(SBAGUIWithServerTestCase):

    def get_config_filename(self):
        return "test_hungryhungrybaubles2.cfg", "test_tournament.cfg"

    def test_running_network_tournament(self):
        ships = []
        numships = 8
        groups = self.cfg.getint("Tournament", "groups")

        for x in range(numships):
            ships.append(AIShip_Network_Harness("Move", self.__target_ship))
            self.assertTrue(ships[-1].connect(self.cfg.getint("Server", "port")), "Ship " + repr(x) + " Didn't connect to server.")    
            time.sleep(0.2)
            self.assertTrue(ships[-1].isconnected(), "Target Client not connected to server.")

        for x in range(groups + 1):
            self.assertEqual(len(self.game.world), 0, "Objects in World before round")
            self.assertFalse(self.game.round_get_has_started(), "Game Timer Running")

            self.game.round_start()

            time.sleep(2.0)

            if x == groups:
                self.assertEqual(len(self.game.world), 26, "Found more than 4 ships + baubles in world")

                for player in self.game._tmanager._finalgroup:
                    self.assertTrue(player.object in self.game.world, "Player's Ship not in final tournament")
                    self.assertLess(player.score, 1, "Players shouldn't have score entering final round")

            for i in range(x + 2):
                self.game.world.append(Bauble(intpos(self.game.game_get_current_player_list()[i % 2].object.body.position), 1))
                time.sleep(0.5)

            self.assertTrue(self.game.round_get_has_started(), "Game Timer NOT Running")

            time.sleep(7.5)

            leader = None
            for player in self.game.game_get_current_leader_list():
                print(player.name, player.score)
                if leader == None:
                    leader = player
                #self.assertGreater(player.score, 10, "Each player should have scored")

            time.sleep(23)

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
                self.assertIsNotNone(self.game._tmanager._finalwinners, "Final Winner not marked")
                self.assertIn(leader, self.game._tmanager._finalwinner, "Incorrect leader chosen")
                pass
            #eif
        #next round

        time.sleep(3)

        self._endServer()

    def __target_ship(self, ship, env):
        logging.info("Test Case got Callback from Network for Target Ship")
        self.__env_target = env
        return RotateCommand(ship, 240)

    def __radar_ship(self, ship, env):
        logging.info("Test Case got Callback from Network for Radar Ship")
        self.__env_radar = env
        return RotateCommand(ship, 240)


if __name__ == '__main__':
    unittest.main()
