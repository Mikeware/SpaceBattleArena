"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2015 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

import sys, traceback, glob, os.path

import logging
import unittest

from Game.Game import BasicGame

from ConfigParser import ConfigParser
from World.WorldGenerator import ConfiguredWorld
import Server.WorldServer as WorldServer

import thread
from GUI import main
from importlib import import_module

import time

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
        thread.start_new_thread(main.startGame, ("Space Battle Tests - " + self._testMethodName, self.game, False, (self.cfg.getint("Application", "horz_res"), self.cfg.getint("Application", "vert_res")), self.cfg.getboolean("Application", "showstats"), self.cfg.getboolean("Application", "sound"), self))

    def tearDown(self):
        self.donetest = True

        time.sleep(1)

        super(SBAGUITestCase, self).tearDown()

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
