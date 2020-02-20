"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2020 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from .Game import BasicGame
from GUI.ObjWrappers.GUIEntity import GUIEntity, debugfont
from GUI.GraphicsCache import Cache
from World.WorldMath import intpos, friendly_type, PlayerStat, aligninstances, getPositionAwayFromOtherObjects
from World.Entities import PhysicalRound, Entity
import random
import logging
import pygame
from operator import attrgetter
from pymunk import ShapeFilter

class BaseBaubleGame(BasicGame):
    """
    Base Class for Creating Bauble Games which spawn Baubles of various colors/point values.

    Used by Hungry Hungry Baubles Basic Game and Advanced Bauble Hunt game.
    """
    VALUE_TABLE = []
    WEIGHT_TABLE = []
    INVERTWEIGHT_TABLE = []

    def __init__(self, cfgobj):
        percents = list(map(float, cfgobj.get("BaubleGame", "bauble_percent").split(",")))
        points = list(map(int, cfgobj.get("BaubleGame", "bauble_points").split(",")))

        weights = list(map(int, cfgobj.get("BaubleGame", "bauble_weights").split(",")))
        weight_percents = list(map(float, cfgobj.get("BaubleGame", "bauble_weight_percent").split(",")))

        # Create list of values/percents
        BaseBaubleGame.VALUE_TABLE = []
        x = 0.0
        i = 0
        for percent in percents:
            x += percent
            BaseBaubleGame.VALUE_TABLE.append((x, points[i]))
            i += 1

        # Create list of weights/percents
        BaseBaubleGame.WEIGHT_TABLE = []
        x = 0.0
        i = 0
        for percent in weight_percents:
            x += percent
            BaseBaubleGame.WEIGHT_TABLE.append((x, weights[i]))
            i += 1

        weight_percents_r = weight_percents[:]
        weight_percents_r.reverse()

        BaseBaubleGame.INVERTWEIGHT_TABLE = []
        x = 0.0
        i = 0
        for percent in weight_percents_r:
            x += percent
            BaseBaubleGame.INVERTWEIGHT_TABLE.append((x, weights[i]))
            i += 1

        super(BaseBaubleGame, self).__init__(cfgobj)

class BaubleWrapper(GUIEntity):
    def __init__(self, obj, world):
        self.surface = Cache().getScaledImage("Games/Bauble" + str(obj.value), obj.weight ** 0.27)
        self.adjust = self.surface.get_width() / 2
        super(BaubleWrapper, self).__init__(obj, world)

    def draw(self, surface, flags):
        surface.blit(self.surface, intpos((self._worldobj.body.position[0] - self.adjust, self._worldobj.body.position[1] - self.adjust)))

        if flags["DEBUG"] and self._worldobj.weight > 1:
            bp = self._worldobj.body.position.int_tuple
            # id text
            surface.blit(debugfont().render(str(self._worldobj.weight), False, (192, 192, 192)), (bp[0]+self.adjust, bp[1]-4))

        super(BaubleWrapper, self).draw(surface, flags)

class Bauble(PhysicalRound):
    WRAPPERCLASS = BaubleWrapper
    """
    Baubles are small prizes worth different amounts of points
    """
    def __init__(self, pos, value=1, weight=1):
        super(Bauble, self).__init__(8, 2000, pos)
        self.shape.elasticity = 0.8
        self.health = PlayerStat(0)

        self.shape.filter = ShapeFilter(group=1)

        self.value = value
        self.weight = weight

        # Make sure Baubles aren't effected by gravity or explosions
        self.explodable = False
        self.gravitable = False

    def collide_start(self, otherobj):
        return False

    def getExtraInfo(self, objData, player):
        objData["VALUE"] = self.value
        objData["MASS"] = self.weight

    @staticmethod
    def spawn(world, cfg, pos=None, value=None):
        if pos == None:
            pos = getPositionAwayFromOtherObjects(world, cfg.getint("Bauble", "buffer_object"), cfg.getint("Bauble", "buffer_edge"))

        # Get value within tolerances
        r = random.random()
        v = 0
        vi = 0
        if value == None:
            for ent in BaseBaubleGame.VALUE_TABLE:
                if r < ent[0]:
                    v = ent[1]
                    break
                vi += 1
        else:
            for ent in BaseBaubleGame.VALUE_TABLE:
                if ent[1] == value:
                    v = ent[1]
                    break
                vi += 1

        if cfg.has_option("BaubleGame", "bauble_invert_ratio_percent"):
            wvr = list(map(float, cfg.get("BaubleGame", "bauble_invert_ratio_percent").split(",")))[vi]
        else:
            wvr = 0.0

        if random.random() < wvr:
            r = random.random()
            w = 0
            for ent in BaseBaubleGame.INVERTWEIGHT_TABLE:
                if r < ent[0]:
                    w = ent[1]
                    break
        else:
            r = random.random()
            w = 0
            for ent in BaseBaubleGame.WEIGHT_TABLE:
                if r < ent[0]:
                    w = ent[1]
                    break

        b = Bauble(pos, v, w)
        world.append(b)
        return b
