"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2015 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from TestCaseRigging import SBAWorldTestCase
from World.WorldEntities import *

class CreatePlanetTestCase(SBAWorldTestCase):
    """
    Dummy test to create a planet and check it was added to the world of the game.
    """
    def world_create(self, world):
        self._planet = Planet((300, 300))
        world.append(self._planet)

        return world

    def test_planet_exists(self):
        self.assertNotEqual(self.game.world[self._planet.id], None, 'Planet Missing')

if __name__ == '__main__':
    unittest.main()
