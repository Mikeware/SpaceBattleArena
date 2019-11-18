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
from World.WorldEntities import Nebula, Ship
from World.WorldCommands import *

import time
import threading

class RadarClientServerTestCase(SBAGUIWithServerTestCase):

    def get_config_filename(self):
        return "test_server.cfg"

    def test_add_two_ships_get_radar_results(self):
        """
        Test adding two networked clients to a server and that one can radar the other
        """
        self._env_target = None
        self._env_radar = None

        self.targetship = AIShip_Network_Harness("Target", self.__target_ship)
        self.assertTrue(self.targetship.connect(self.cfg.getint("Server", "port")), "Target Didn't connect to server.")

        self.radarship = AIShip_Network_Harness("Radar", self.__radar_ship)
        self.assertTrue(self.radarship.connect(self.cfg.getint("Server", "port")), "Radar Didn't connect to server.")

        time.sleep(0.5)

        self.assertTrue(self.targetship.isconnected(), "Target Client not connected to server.")
        self.assertTrue(self.radarship.isconnected(), "Radar Client not connected to server.")

        self.assertIsNotNone(self._env_target, "Target Never received environment.")
        self.assertIsNotNone(self._env_radar, "Radar Never received environment.")

        tship = None
        rship = None

        for obj in self.game.world:
            if "Target" in obj.player.name:
                tship = obj
            elif "Radar" in obj.player.name:
                rship = obj
        
        self.assertIsNotNone(tship, "Couldn't find Target Ship")
        self.assertIsNotNone(rship, "Couldn't find Radar Ship")

        tship.body.position = self.game.world.mid_point(-75, 0)
        rship.body.position = self.game.world.mid_point(75, 0)

        time.sleep(1)

        self.assertEqual(len(self._env_radar["RADARDATA"]), 1, "Radar Data Doesn't Contain 1 Item")
        self.assertEqual(self._env_radar["RADARDATA"][0]["ID"], tship.id, "Radar Doesn't Contain Target Ship")
        
        self.assertIsNone(self._env_target["RADARDATA"], "Target Radar Should Not Contain Data")

        time.sleep(1)

        self._endServer()

        time.sleep(2)

        self.assertFalse(self.targetship.isconnected(), "Target Client still connected to server after disconnect.")
        self.assertFalse(self.radarship.isconnected(), "Radar Client still connected to server after disconnect.")

        time.sleep(0.5)

    def test_two_ships_no_radar_when_cloaked(self):
        """
        Test adding two networked clients to a server and that one can't radar the other when it's cloaked
        """
        self._env_target = None
        self._env_radar = None

        self.targetship = AIShip_Network_Harness("Cloak", self.__cloak_ship)
        self.assertTrue(self.targetship.connect(self.cfg.getint("Server", "port")), "Target Didn't connect to server.")

        self.radarship = AIShip_Network_Harness("Radar", self.__radar_ship)
        self.assertTrue(self.radarship.connect(self.cfg.getint("Server", "port")), "Radar Didn't connect to server.")

        time.sleep(0.5)

        self.assertTrue(self.targetship.isconnected(), "Target Client not connected to server.")
        self.assertTrue(self.radarship.isconnected(), "Radar Client not connected to server.")

        self.assertIsNotNone(self._env_target, "Target Never received environment.")
        self.assertIsNotNone(self._env_radar, "Radar Never received environment.")

        tship = None
        rship = None

        for obj in self.game.world:
            if "Cloak" in obj.player.name:
                tship = obj
            elif "Radar" in obj.player.name:
                rship = obj
        
        self.assertIsNotNone(tship, "Couldn't find Target Ship")
        self.assertIsNotNone(rship, "Couldn't find Radar Ship")

        tship.body.position = self.game.world.mid_point(-75, 0)
        rship.body.position = self.game.world.mid_point(75, 0)

        time.sleep(1)

        self.assertEqual(len(self._env_radar["RADARDATA"]), 0, "Radar Data Contains Cloaked Ship")
        self.assertIsNone(self._env_target["RADARDATA"], "Target Radar Should Not Contain Data")

        time.sleep(1)

        self._endServer()

        time.sleep(2)

        self.assertFalse(self.targetship.isconnected(), "Target Client still connected to server after disconnect.")
        self.assertFalse(self.radarship.isconnected(), "Radar Client still connected to server after disconnect.")

        time.sleep(0.5)

    def test_two_ships_no_radar_when_nebula(self):
        """
        Test adding two networked clients to a server and that one can't radar the other when it's in a nebula
        """
        self._env_target = None
        self._env_radar = None

        self.targetship = AIShip_Network_Harness("Nebula", self.__target_ship)
        self.assertTrue(self.targetship.connect(self.cfg.getint("Server", "port")), "Target Didn't connect to server.")

        self.radarship = AIShip_Network_Harness("Radar", self.__radar_ship)
        self.assertTrue(self.radarship.connect(self.cfg.getint("Server", "port")), "Radar Didn't connect to server.")

        nebula = Nebula(self.game.world.mid_point(-128,0), (384, 256))
        self.game.world.append(nebula)

        time.sleep(0.5)

        self.assertTrue(self.targetship.isconnected(), "Target Client not connected to server.")
        self.assertTrue(self.radarship.isconnected(), "Radar Client not connected to server.")

        self.assertIsNotNone(self._env_target, "Target Never received environment.")
        self.assertIsNotNone(self._env_radar, "Radar Never received environment.")

        tship = None
        rship = None

        for obj in self.game.world:
            if isinstance(obj, Ship):
                if "Nebula" in obj.player.name:
                    tship = obj
                elif "Radar" in obj.player.name:
                    rship = obj
        
        self.assertIsNotNone(tship, "Couldn't find Target Ship")
        self.assertIsNotNone(rship, "Couldn't find Radar Ship")

        tship.body.position = self.game.world.mid_point(-75, 0)
        rship.body.position = self.game.world.mid_point(100, 0)

        time.sleep(1)

        self.assertEqual(len(self._env_radar["RADARDATA"]), 1, "Radar Data Contains more than Nebula")
        self.assertIsNone(self._env_target["RADARDATA"], "Target Radar Should Not Contain Data")

        time.sleep(1)

        self._endServer()

        time.sleep(2)

        self.assertFalse(self.targetship.isconnected(), "Target Client still connected to server after disconnect.")
        self.assertFalse(self.radarship.isconnected(), "Radar Client still connected to server after disconnect.")

        time.sleep(0.5)

    def test_two_ships_cant_read_command_queue_and_energy(self):
        """
        Test adding two networked clients to a server and that one can't read the command queue of the other
        """
        self._env_target = None
        self._env_radar = None

        self.targetship = AIShip_Network_Harness("Target", self.__target_ship)
        self.assertTrue(self.targetship.connect(self.cfg.getint("Server", "port")), "Target Didn't connect to server.")

        self.radarship = AIShip_Network_Harness("Radar", self.__radar_ship)
        self.assertTrue(self.radarship.connect(self.cfg.getint("Server", "port")), "Radar Didn't connect to server.")

        time.sleep(0.5)

        self.assertTrue(self.targetship.isconnected(), "Target Client not connected to server.")
        self.assertTrue(self.radarship.isconnected(), "Radar Client not connected to server.")

        self.assertIsNotNone(self._env_target, "Target Never received environment.")
        self.assertIsNotNone(self._env_radar, "Radar Never received environment.")

        tship = None
        rship = None

        for obj in self.game.world:
            if "Target" in obj.player.name:
                tship = obj
            elif "Radar" in obj.player.name:
                rship = obj
        
        self.assertIsNotNone(tship, "Couldn't find Target Ship")
        self.assertIsNotNone(rship, "Couldn't find Radar Ship")

        tship.body.position = self.game.world.mid_point(-75, 0)
        rship.body.position = self.game.world.mid_point(75, 0)

        time.sleep(1)

        self.assertEqual(len(self._env_radar["RADARDATA"]), 1, "Radar Data Doesn't Contain 1 Item")
        self.assertEqual(self._env_radar["RADARDATA"][0]["ID"], tship.id, "Radar Doesn't Contain Target Ship")
        self.assertFalse("CURENERGY" in self._env_radar["RADARDATA"][0], "Radar shouldn't contain Target's Energy Level")
        self.assertFalse("CMDQ" in self._env_radar["RADARDATA"][0], "Radar shouldn't contain Target's Command Queue")
        
        self.assertIsNone(self._env_target["RADARDATA"], "Target Radar Should Not Contain Data")
        self.assertIsNotNone(self._env_target["SHIPDATA"], "Target Should Contain Ship Data")
        self.assertIsNotNone(self._env_target["SHIPDATA"]["CURENERGY"], "Target Ship Should Know It's Energy Level.")
        self.assertEqual(self._env_target["SHIPDATA"]["CURENERGY"], self._env_target["SHIPDATA"]["MAXENERGY"], "Target Ship Should have all its energy.")
        self.assertIsNotNone(self._env_target["SHIPDATA"]["CMDQ"], "Target Ship Should Know It's Command Queue.")

        time.sleep(1)

        self._endServer()

        time.sleep(2)

        self.assertFalse(self.targetship.isconnected(), "Target Client still connected to server after disconnect.")
        self.assertFalse(self.radarship.isconnected(), "Radar Client still connected to server after disconnect.")

        time.sleep(0.5)

    def __target_ship(self, ship, env):
        logging.info("Test Case got Callback from Network for Target Ship")
        self._env_target = env
        return RotateCommand(ship, 6)

    def __cloak_ship(self, ship, env):
        logging.info("Test Case got Callback from Network for Cloak Ship")
        if self._env_target == None:
            self._env_target = env
            return CloakCommand(ship, 8.0)

        self._env_target = env
        return IdleCommand(ship, 2.0)

    def __radar_ship(self, ship, env):
        logging.info("Test Case got Callback from Network for Radar Ship")
        self._env_radar = env
        return RadarCommand(ship, 5)

if __name__ == '__main__':
    unittest.main()
