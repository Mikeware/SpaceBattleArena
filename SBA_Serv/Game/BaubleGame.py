"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2016 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from Game import BasicGame
from GUI.ObjWrappers.GUIEntity import GUIEntity
from GUI.GraphicsCache import Cache
from World.WorldMath import intpos, friendly_type, PlayerStat, aligninstances, getPositionAwayFromOtherObjects
from World.Entities import PhysicalRound, Entity
import random
import logging
import pygame
from operator import attrgetter

class BaseBaubleGame(BasicGame):
    """
    Base Class for Creating Bauble Games which spawn Baubles of various colors/point values.

    Used by Hungry Hungry Baubles Basic Game and Advanced Bauble Hunt game.
    """
    VALUE_TABLE = []

    def __init__(self, cfgobj):
        percents = map(float, cfgobj.get("BaubleGame", "bauble_percent").split(","))
        points = map(int, cfgobj.get("BaubleGame", "bauble_points").split(","))

        BaseBaubleGame.VALUE_TABLE = []
        x = 0.0
        i = 0
        for percent in percents:
            x += percent
            BaseBaubleGame.VALUE_TABLE.append((x, points[i]))
            i += 1

        super(BaseBaubleGame, self).__init__(cfgobj)

class BaubleWrapper(GUIEntity):
    def __init__(self, obj, world):
        super(BaubleWrapper, self).__init__(obj, world)
        self.surface = Cache().getImage("Games/Bauble" + str(obj.value))

    def draw(self, surface, flags):
        surface.blit(self.surface, intpos((self._worldobj.body.position[0] - 8, self._worldobj.body.position[1] - 8)))

        super(BaubleWrapper, self).draw(surface, flags)

class Bauble(PhysicalRound):
    WRAPPERCLASS = BaubleWrapper
    """
    Baubles are small prizes worth different amounts of points
    """
    def __init__(self, pos, value=1):
        super(Bauble, self).__init__(8, 2000, pos)
        self.shape.elasticity = 0.8
        self.health = PlayerStat(0)

        self.shape.group = 1

        self.value = value

        # Make sure Baubles aren't effected by gravity or explosions
        self.explodable = False
        self.gravitable = False

    def collide_start(self, otherobj):
        return False

    def getExtraInfo(self, objData, player):
        objData["VALUE"] = self.value

    @staticmethod
    def spawn(world, cfg, pos=None):
        if pos == None:
            pos = getPositionAwayFromOtherObjects(world, cfg.getint("Bauble", "buffer_object"), cfg.getint("Bauble", "buffer_edge"))

        # Get value within tolerances
        r = random.random()
        v = 0
        for ent in BaseBaubleGame.VALUE_TABLE:
            if r < ent[0]:
                v = ent[1]
                break

        b = Bauble(pos, v)
        world.append(b)
        return b
