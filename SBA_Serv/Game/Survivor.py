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
from World.Entities import Entity
from World.WorldEntities import Ship
from GUI.ObjWrappers.GUIEntity import GUIEntity
from World.WorldMath import intpos, friendly_type, PlayerStat, in_circle
from GUI.GraphicsCache import Cache
from GUI.Helpers import debugfont, wrapcircle, namefont
import logging, random
import pygame
from operator import attrgetter

# Basic Game - Survivor
# Preliminary Exercise to motivate students to learn about Radar
# 
# Students score is based on how long their ship has lived.
# Introduces the notion of a 'best' score for a session.

class SurvivorGame(BasicGame):
    
    def game_update(self, t):
        for player in self.game_get_current_player_list():
            self.player_update_score(player, t)

        super(SurvivorGame, self).game_update(t)

    def player_get_stat_string(self, player):        
        return "%.2f" % getattr(player, self._primary_victory) + "  " + "%.2f" % getattr(player, self._secondary_victory) + " : " + player.name