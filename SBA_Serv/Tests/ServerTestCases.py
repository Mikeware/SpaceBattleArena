"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2015 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from TestCaseRigging import SBAServerTestCase, SBAGUIWithServerTestCase
import Server.MWNL2 as MWNL2
from World.AIShips import AIShip_Network_Harness
from World.WorldCommands import *

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

        for x in xrange(numclients):
            self.ships.append(AIShip_Network_Harness("Add Me " + str(x), self.__bad_thrust_ship))

            self.assertTrue(self.ships[-1].connect(self.cfg.getint("Server", "port")), "Didn't connect to server.")
        #next

        time.sleep(5)

        self.game.end()

        # server closes all connections
        self.server.disconnectAll()

        time.sleep(10)

        print threading.enumerate()

        self.assertFalse(self.server.isrunning(), "Server still running after disconnect.")

        for x in xrange(numclients):
            self.assertFalse(self.ships[x].isconnected(), "Client still connected to server after disconnect.")

        print threading.enumerate()
        self.assertEqual(len(threading.enumerate()), 1, "More than main thread running.")

    def __bad_thrust_ship(self, env):
        logging.info("Test Case got Callback from Network")
        x = random.randint(1, 10)
        if x > 7:
            return ThrustCommand(self.ships[0], 'B', 1.0, 0.5)
        elif x > 3:
            time.sleep(3)
            return RotateCommand(self.ships[0], 120)
        return IdleCommand(self.ships[0], 10)

    def callback(self, sender, cmd):
        pass

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

    def __rotate_ship(self, env):
        logging.info("Test Case got Callback from Network")
        self.__env = env
        return RotateCommand(self.ship, 6)

    def __error_ship(self, env):
        self.__env = env
        time.sleep(1)
        # want client thread to die to test server, seems to not effect test, which is kind of a bad thing, but we'll exploit it for now
        # means we should be more prudent with testing for those cases with asserts to prevent bad tests.
        raise Exception

if __name__ == '__main__':
    unittest.main()
