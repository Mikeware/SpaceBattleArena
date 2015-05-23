"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2015 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from Game import BasicGame, RoundTimer
from World.WorldGenerator import ConfiguredWorld, getPositionAwayFromOtherObjects
from World.Entities import Entity, PhysicalEllipse
from World.WorldEntities import Ship
from GUI.ObjWrappers.GUIEntity import GUIEntity
from World.WorldMath import intpos, friendly_type, PlayerStat
from GUI.GraphicsCache import Cache
from GUI.Helpers import debugfont, wrapcircle, namefont
import logging, random
import pygame

class DiscoveryQuestGame(BasicGame):
    """
    Discovery Quest is an exploration game.


    """
    
    def __init__(self, cfgobj):
        super(DiscoveryQuestGame, self).__init__(cfgobj)

        self.world.append(Outpost(getPositionAwayFromOtherObjects(self.world, 80, 30)))

class OutpostWrapper(GUIEntity):
    def __init__(self, obj, world):
        super(OutpostWrapper, self).__init__(obj, world)
        self.surface = Cache().getImage("Games/Outpost" + str(random.randint(1, Cache().getMaxImages("Games/Outpost"))))

    def draw(self, surface, flags):
        bp = intpos(self._worldobj.body.position)
        surface.blit(self.surface, (bp[0] - 32, bp[1] - 64))

        # TODO: Owner ID Display

        #if flags["NAMES"]:
            # HACK TODO: Ship name should be from team
            #text = debugfont().render(self._worldobj.owner.player.name, False, self._worldobj.owner.player.color)
            #surface.blit(text, (bp[0]-text.get_width()/2, bp[1]-18))

        #if flags["STATS"]:
        #    text = debugfont().render(repr(self._worldobj.stored), False, self._worldobj.owner.player.color)
        #    surface.blit(text, (bp[0]-text.get_width()/2, bp[1]+4))

        super(OutpostWrapper, self).draw(surface, flags)

class Outpost(PhysicalEllipse):
    WRAPPERCLASS = OutpostWrapper
    """
    Baubles are small prizes worth different amounts of points
    """
    def __init__(self, pos):
        super(Outpost, self).__init__((60, 120), 4000, pos)
        self.shape.elasticity = 0.8
        self.health = PlayerStat(0)

        self.body.velocity_limit = 0
        
        self.shape.group = 1

        self.stored = 0

    def collide_start(self, otherobj):
        return False

    #def getExtraInfo(self, objData):
    #    objData["OWNERID"] = self.owner.id
        
    #def newOwner(self, ship):
    #    self.owner = ship
