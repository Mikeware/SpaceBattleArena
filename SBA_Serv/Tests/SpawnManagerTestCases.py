"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2016 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from TestCaseRigging import SBAWorldTestCase, SBAGUITestCase
from unittest import TestCase
from World.WorldEntities import *
from World.AIShips import *
from World.WorldMath import *

import time

class SpawnManagerTestCase(SBAGUITestCase):

    def get_config_filename(self):
        return "test_spawning.cfg"

    def test_spawn_time_player(self):
        time.sleep(0.5)

        self.assertEqual(self.game.world.get_count_of_objects(Asteroid), 2, "2 Asteroids not in world")

        time.sleep(8.75)

        self.assertEqual(self.game.world.get_count_of_objects(Asteroid), 4, "2 more asteroids didn't spawn over time")

        ship = AIShip_SetList("Doomed", self.game.world.mid_point(), self.game, [])

        time.sleep(0.5)

        self.assertIn(ship, self.game.world, "Ship not in world.")
        self.assertEqual(self.game.world.get_count_of_objects(Asteroid), 4, "more asteroids spawned than should have.")
        self.assertEqual(self.game.world.get_count_of_objects(Dragon), 1, "Dragon didn't spawn")

        time.sleep(1)

        ship.take_damage(9000)

        time.sleep(1)

        # TODO: Can't test with AI ships right now...grrr
        #self.assertEqual(self.game.world.get_count_of_objects(Asteroid), 6, "Asteroid should have spawned on respawn.")

        #time.sleep(1)

    def test_spawn_min_max(self):
        time.sleep(1)

        self.assertEqual(self.game.world.get_count_of_objects(Planet), 0, "Should be no planets")
        
        for obj in self.game.world:
            obj.destroyed = True # clear out world

        time.sleep(4.5)

        self.assertEqual(self.game.world.get_count_of_objects(Asteroid), 2, "Should be 2 asteroids")
        self.assertEqual(self.game.world.get_count_of_objects(Planet), 1, "Should be 1 planet")

        time.sleep(4.5)

        self.assertEqual(self.game.world.get_count_of_objects(Asteroid), 4, "Should be 4 asteroids")
        self.assertEqual(self.game.world.get_count_of_objects(Planet), 2, "Should be 2 planets")
        self.assertEqual(self.game.world.get_count_of_objects(BlackHole), 0, "Should be 0 Black Hole")

        time.sleep(4.25)

        self.assertEqual(self.game.world.get_count_of_objects(BlackHole), 1, "Should be 1 Black Hole")
        self.assertEqual(self.game.world.get_count_of_objects(Planet), 2, "Should still be 2 planet")

    def test_spawn_when_removed(self):
        time.sleep(1)

        self.assertEqual(self.game.world.get_count_of_objects(Planet), 0, "Should be no planets")
        
        for obj in self.game.world:
            obj.destroyed = True # clear out world

        time.sleep(4.5)

        self.assertEqual(self.game.world.get_count_of_objects(Asteroid), 2, "Should be 2 asteroids")
        self.assertEqual(self.game.world.get_count_of_objects(Planet), 1, "Should be 1 planet")

        time.sleep(4.25)

        self.assertEqual(self.game.world.get_count_of_objects(Asteroid), 4, "Should be 4 asteroids")
        self.assertEqual(self.game.world.get_count_of_objects(Planet), 2, "Should be 2 planets")

        time.sleep(0.1)

        ast = []

        for obj in self.game.world:
            if isinstance(obj, Asteroid):
                ast.append(obj.id)
                obj.destroyed = True # clear out asteroids

        time.sleep(0.1)

        self.assertEqual(self.game.world.get_count_of_objects(Asteroid), 2, "Should be 2 new asteroids")
        for obj in self.game.world:
            if isinstance(obj, Asteroid):
                self.assertNotIn(obj.id, ast, "Asteroid should have been destroyed.")

        time.sleep(4.25)

        self.assertEqual(self.game.world.get_count_of_objects(Planet), 2, "Should still be 2 planet")


class SpawnManagerTestCaseMore(SBAGUITestCase):

    def get_config_filename(self):
        return "test_spawning2.cfg"

    def test_spawn_min_max_equal(self):
        time.sleep(1)

        self.assertEqual(self.game.world.get_count_of_objects(Planet), 0, "Should be no planets")
        
        for obj in self.game.world:
            obj.destroyed = True # clear out world

        time.sleep(4.5)

        self.assertEqual(self.game.world.get_count_of_objects(Asteroid), 12, "Should be 12 asteroids")
        self.assertEqual(self.game.world.get_count_of_objects(Planet), 0, "Should be no planets")
        self.assertEqual(self.game.world.get_count_of_objects(Dragon), 6, "Should be 6 Dragons")

        time.sleep(4.25)

        self.assertEqual(self.game.world.get_count_of_objects(Asteroid), 12, "Should be 12 asteroids")
        self.assertEqual(self.game.world.get_count_of_objects(Planet), 0, "Should be no planets")
        self.assertEqual(self.game.world.get_count_of_objects(Dragon), 6, "Should be 6 Dragons")


    # TODO: Add test cases around min restoring without timer...

if __name__ == '__main__':
    unittest.main()
