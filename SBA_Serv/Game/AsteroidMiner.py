"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2015 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from Game import BasicGame
from Utils import CallbackTimer
from World.Entities import Entity
from World.WorldEntities import Ship, Asteroid, Torpedo
from GUI.ObjWrappers.GUIEntity import GUIEntity
from World.WorldMath import intpos, friendly_type, PlayerStat, getPositionAwayFromOtherObjects
from GUI.GraphicsCache import Cache
from GUI.Helpers import debugfont
import logging
import pygame
from operator import attrgetter

class AsteroidMinerGame(BasicGame):
    
    def __init__(self, cfgobj):
        super(AsteroidMinerGame, self).__init__(cfgobj)

        self.__torpedopoints = self.cfg.getint("AsteroidMiner", "points_torpedo")
        self.__shippoints = self.cfg.getint("AsteroidMiner", "points_ship")
    
    def world_add_remove_object(self, wobj, added):
        logging.debug("BH Add Object(%s): #%d (%s)", repr(added), wobj.id, friendly_type(wobj))
        if not added and isinstance(wobj, Asteroid) and hasattr(wobj, "killedby") and wobj.killedby != None:
            obj = wobj.killedby
            if isinstance(obj, Torpedo):
                self.player_update_score(obj.owner.player, self.__torpedopoints)
                    
                logging.info("Torpedo Owner (#%d) Destroyed Asteroid", obj.owner.id)
            elif isinstance(obj, Ship) and obj.health.value > 0:
                self.player_update_score(obj.player, self.__shippoints)
                    
                logging.info("Ship (#%d) Destroyed Asteroid", obj.id)
        
        super(AsteroidMinerGame, self).world_add_remove_object(wobj, added)

