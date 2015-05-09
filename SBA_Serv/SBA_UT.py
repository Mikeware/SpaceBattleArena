"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2015 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

__author__ = "Michael A. Hawker"
__copyright__ = "Copyright 2012-2015 Mikeware"
__license__ = "GPLv2"
__version__ = "1.0"
__email__ = "questions@mikeware.com"
__status__ = "beta"

title = "Space Battle Arena"
titlever = title + " v" + __version__

import logging

import sys, traceback, glob, os.path
import time
import thread
from GUI import main
from importlib import import_module

import Server.WorldServer as WorldServer
import World.WorldMap as WorldMap
from World.WorldEntities import *
from World.WorldGenerator import ConfiguredWorld
from Game.Game import BasicGame
from World.WorldCommands import *
from World.AIShips import *

from ConfigParser import ConfigParser

import Server.MWNL2 as MWNL2

import unittest

#TODO: Investigate the best way to inject this wrapper around any Subgame
class TestGame(BasicGame):
    """
    Class to emulate a game but hook into world creations.
    """
    def __init__(self, cfg, testcase):
        self._testcase = testcase

        super(TestGame, self).__init__(cfg)

    def createWorld(self, pys = True):
        return self._testcase.createWorld(ConfiguredWorld(self, self.cfg, empty=True))

class SBAWorldTestCase(unittest.TestCase):
    """
    Base Test Case which sets up a blank world and game for testing without the server or UI.
    """
    def setUp(self):
        with open("SBA_Test"+self._testMethodName+".log", "w") as file:
            pass
        logging.basicConfig(level=logging.DEBUG, filename="SBA_Test"+self._testMethodName+".log", format='%(asctime)s|%(relativeCreated)d|%(levelname)s|%(threadName)s|%(module)s|%(lineno)d|%(funcName)s|%(message)s')
        logging.info("Running Test: %s", self._testMethodName)

        self.cfg = ConfigParser()
        self.cfg.readfp(open(self.get_config_filename()))
        self.game = TestGame(self.cfg, self)

        # Create Dummy Test Player
        #self.game.registerPlayer("Test", (255, 0, 0), 0, 0) # TODO: check last parameter for netid to see what it should be
        #self.player = self.game.getPlayerByNetId(0)

    def tearDown(self):
        self.game.world.endGameLoop()
        logging.info("Done Running Test: %s", self._testMethodName)

    def get_config_filename(self):
        return "test.cfg"

    # TODO: can I just grab from config instead and they'll need custom to change game anyway...
    def get_game_name(self):
        return "TestGame"

    def createWorld(self, world):
        """
        Test Case should override this method to generate a world for their test.
        """
        return world

class SBAServerTestCase(SBAWorldTestCase):
    """
    Test Case which needs a server running
    """
    def setUp(self):
        super(SBAServerTestCase, self).setUp()

        self.server = WorldServer.WorldServer(self.cfg.getint("Server", "port"), self.game)

    def tearDown(self):
        super(SBAServerTestCase, self).tearDown()

        self.server.disconnectAll()

class SBAGUITestCase(SBAWorldTestCase):

    def setUp(self):
        super(SBAGUITestCase, self).setUp()

        self.donetest = False

        # TODO: Investigate doing this statically, so it remains open for multiple tests in a suite???
        # Start GUI in separate Thread, so test can run
        thread.start_new_thread(main.startGame, (titlever + " - " + self._testMethodName, self.game, False, (self.cfg.getint("Application", "horz_res"), self.cfg.getint("Application", "vert_res")), self.cfg.getboolean("Application", "showstats"), self.cfg.getboolean("Application", "sound"), self))

    def tearDown(self):
        self.donetest = True

        time.sleep(1)

        super(SBAGUITestCase, self).tearDown()

########################## TODO: Split Test Cases to different files

class CreatePlanetTestCase(SBAWorldTestCase):
    """
    Dummy test to create a planet and check it was added to the world of the game.
    """
    def createWorld(self, world):
        self._planet = Planet((300, 300))
        world.append(self._planet)

        return world

    def test_planet_exists(self):
        self.assertNotEqual(self.game.world[self._planet.id], None, 'Planet Missing')


class ServerConnectTestCase(SBAServerTestCase):

    def test_make_connection(self):
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

    def callback(self, sender, cmd):
        pass

class FrontEndTestCase(SBAGUITestCase):

    def test_steer_vs_thrust(self):
        self.ship = AIShip_SetList("Steer", self.game.world.mid_point(-50), self.game.world, [
                "ThrustCommand(self, 'B', 3.0)",
                "IdleCommand(self, 3.0)",
                "RotateCommand(self, 90)",
                "SteerCommand(self, 90)",                
                "IdleCommand(self, 5.0)"
            ])
        self.ship.rotationAngle = 180
        self.ship2 = AIShip_SetList("Thrust", self.game.world.mid_point(50), self.game.world, [
                "ThrustCommand(self, 'B', 3.0)",
                "IdleCommand(self, 3.0)",
                #"RotateCommand(self, 90)",
                "ThrustCommand(self, 'L', 5.0, 0.5)",
                "ThrustCommand(self, 'F', 5.0, 0.5)",
                "IdleCommand(self, 5.0)"
            ])
        self.ship2.rotationAngle = 0
        self.game.world.append(self.ship)
        self.game.world.append(self.ship2)
        
        while len(self.ship.cmdlist) > 0:
            time.sleep(0.02)

        time.sleep(5)

        x = self.ship.body.position[0]

class ShapesTestCase(SBAGUITestCase):

    def test_rect(self):
        center = self.game.world.mid_point(0)
        self.ship = AIShip_SetListLoop("Rectangle", center, self.game.world, [
                "DeployLaserBeaconCommand(self)",
                "ThrustCommand(self, 'B', 3.5)",
                "IdleCommand(self, 4)",
                "BrakeCommand(self, 0)",
                "IdleCommand(self, 4)",
                "RotateCommand(self, 90)",
                "DeployLaserBeaconCommand(self)"
            ], 4)
        self.ship.rotationAngle = 90
        self.game.world.append(self.ship)
        
        while len(self.ship.cmdlist) > 0:
            time.sleep(0.02)

        time.sleep(5)

        logging.debug("Ship Position %s, expected position %s", repr(self.ship.body.position), repr(center))
        self.assertAlmostEqual(float(self.ship.body.position[0]), center[0], None, "Ship X not the same as Start", 3)
        self.assertAlmostEqual(float(self.ship.body.position[1]), center[1], None, "Ship Y not the same as Start", 3)

    def test_spiral(self):
        self.ship = AIShip_SetListLoop("Spiral", self.game.world.mid_point(0), self.game.world, [
                "DeployLaserBeaconCommand(self)",
                "ThrustCommand(self, 'B', 0.5)",
                "RotateCommand(self, 20)",
                "SteerCommand(self, 20)",
                "DeployLaserBeaconCommand(self)"
            ])
        self.ship.rotationAngle = 90
        self.game.world.append(self.ship)
        
        time.sleep(40)

        x = self.ship.body.position[0]

if __name__ == '__main__':
    unittest.main()

"""
    game = None
    if rungame != "BasicGame" and rungame != None and rungame.strip() != "":
        mod = None
        try:
            mod = import_module("Game."+rungame)
            game = mod.__dict__[rungame+"Game"](cfg)
            logging.info("Running Game: " + rungame)
        except:
            logging.error("Could not start Game " + rungame)
            logging.error(traceback.format_exc())
            print traceback.format_exc()        
    #eif
"""
