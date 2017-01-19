"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2016 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

import sys, traceback, glob, os.path

import logging
import unittest

from Game.Game import BasicGame
from Game.CombatExercise import CombatExerciseGame
from Game.FindTheMiddle import FindTheMiddleGame
from Game.Survivor import SurvivorGame

from Game.HungryHungryBaubles import HungryHungryBaublesGame
from Game.BaubleHunt import BaubleHuntGame
from Game.KingOfTheBubble import KingOfTheBubbleGame
from Game.DiscoveryQuest import DiscoveryQuestGame
from Game.TheHungerBaubles import TheHungerBaublesGame

from ConfigParser import ConfigParser
import Server.WorldServer as WorldServer

import thread
from GUI import main
from importlib import import_module

import time

class TestGame(BasicGame):

    def world_create(self):
        """
        Method called by game to construct world, by default calls the testcase's world_create with an empty configured world.

        If they pass None, then will use the game's default world construction.
        """
        super(TestGame, self).world_create()
        self._testcase.world_create(self)        

#TODO: Investigate the best way to inject this wrapper around any Subgame
class TestBasicGame(TestGame):
    def __init__(self, cfg, testcase):
        self._testcase = testcase

        super(TestBasicGame, self).__init__(cfg)

class TestFindTheMiddleGame(TestGame, FindTheMiddleGame):
    def __init__(self, cfg, testcase):
        self._testcase = testcase

        super(TestFindTheMiddleGame, self).__init__(cfg)

class TestCombatExerciseGame(TestGame, CombatExerciseGame):
    def __init__(self, cfg, testcase):
        self._testcase = testcase

        super(TestCombatExerciseGame, self).__init__(cfg)

class TestSurvivorGame(TestGame, SurvivorGame):
    def __init__(self, cfg, testcase):
        self._testcase = testcase

        super(TestSurvivorGame, self).__init__(cfg)

class TestHungryHungryBaublesGame(TestGame, HungryHungryBaublesGame):
    def __init__(self, cfg, testcase):
        self._testcase = testcase

        super(TestHungryHungryBaublesGame, self).__init__(cfg)

class TestBaubleHuntGame(TestGame, BaubleHuntGame):
    def __init__(self, cfg, testcase):
        self._testcase = testcase

        super(TestBaubleHuntGame, self).__init__(cfg)

class TestKingOfTheBubbleGame(TestGame, KingOfTheBubbleGame):
    def __init__(self, cfg, testcase):
        self._testcase = testcase

        super(TestKingOfTheBubbleGame, self).__init__(cfg)

class TestDiscoveryQuestGame(TestGame, DiscoveryQuestGame):
    def __init__(self, cfg, testcase):
        self._testcase = testcase

        super(TestDiscoveryQuestGame, self).__init__(cfg)

class TestTheHungerBaublesGame(TestGame, TheHungerBaublesGame):
    def __init__(self, cfg, testcase):
        self._testcase = testcase

        super(TestTheHungerBaublesGame, self).__init__(cfg)

class SBAWorldTestCase(unittest.TestCase):
    """
    Base Test Case which sets up a blank world and game for testing without the server or UI.
    """
    def setUp(self):
        try:
            import coverage
            coverage.process_startup()
        except ImportError, EnvironmentError:
            pass

        try:
            classname = str(self.__class__)        
            classname = classname[classname.find(".")+1:-2]
            print classname
            with open("SBA_Test_"+classname+"_"+self._testMethodName+".log", "w") as file:
                pass
            logging.basicConfig(level=logging.DEBUG, filename="SBA_Test_"+classname+"_"+self._testMethodName+".log", format='%(asctime)s|%(relativeCreated)d|%(levelname)s|%(threadName)s|%(module)s|%(lineno)d|%(funcName)s|%(message)s')
            logging.info("Running Test: %s", self._testMethodName)

            self.cfg = ConfigParser()
            self.cfg.readfp(open("Tests/defaulttest.cfg"))
            configs = self.get_config_filename()
            if configs != None:
                if isinstance(configs, str):
                    configs = [configs]
                for config in configs:
                    self.cfg.readfp(open("Tests/"+config))
            self.game = globals()["Test"+self.cfg.get("Game", "game")+"Game"](self.cfg, self)
            logging.info("Using Game %s", repr(self.game))
        except:
            logging.error(traceback.format_exc())
            print traceback.format_exc()
            self.fail()

    def tearDown(self):
        self.assertFalse(self.game.world.gameerror, "Gameloop Exception Occured")
        # finish round
        if not self.game.world.gameerror:
            self.game._tournament = True # force it to not restart timers again
            self.game.round_over()

            self.game.world.endGameLoop()
        logging.info("Done Running Test: %s", self._testMethodName)

    def get_config_filename(self):
        return None

    def world_create(self, game):
        """
        Test Case should override this method to generate the base world for their test cases.
        Called by 'TestGame'

        pys - main world instance or not

        Return None to return to the game's default generation methods.

        The default return is an empty 'ConfiguredWorld'.
        """
        pass

class SBAServerTestCase(SBAWorldTestCase):
    """
    Test Case which needs a server running
    """
    def setUp(self):
        self.started = False

        super(SBAServerTestCase, self).setUp()

        self._startServer()

    def _startServer(self):
        if not self.started:
            self.server = WorldServer.WorldServer(self.cfg.getint("Server", "port"), self.game)
            self.started = True

    def _endServer(self):
        if self.server != None:
            self.server.disconnectAll()
            self.server = None
            self.started = False

    def tearDown(self):
        super(SBAServerTestCase, self).tearDown()

        self._endServer()

class SBAGUITestCase(SBAWorldTestCase):
    """
    Test Case with GUI hook for visualization
    """
    def setUp(self):        
        super(SBAGUITestCase, self).setUp()

        self.donetest = False
        self.flashcolor = False # Used to flash a border of color around the GUI, set to triplet
        #self.resettimer = False # TODO: Used to reset timer in GUI when set to true (need different timing mechanism, should record 'laps'/legs underneath timer each time...)

        # TODO: Investigate doing this statically, so it remains open for multiple tests in a suite???
        # Start GUI in separate Thread, so test can run
        thread.start_new_thread(main.startGame, ("Space Battle Tests - " + self._testMethodName, self.game, False, (self.cfg.getint("Application", "horz_res"), self.cfg.getint("Application", "vert_res")), self.cfg, self))

    def tearDown(self):
        self._resultForDoCleanups.printErrors()

        logging.error(self._resultForDoCleanups.errors)

        self.donetest = True

        time.sleep(1)

        super(SBAGUITestCase, self).tearDown()

class SBAGUIWithServerTestCase(SBAGUITestCase, SBAServerTestCase):
    """
    Test Case with both GUI and Server backend.
    """
    def setUp(self):
        super(SBAGUIWithServerTestCase, self).setUp()

        self._startServer()

    def tearDone(self):
        super(SBAGUIWithServerTestCase, self).tearDown()

        self._endServer()

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
