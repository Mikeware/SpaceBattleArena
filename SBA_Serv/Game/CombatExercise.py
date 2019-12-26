"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2020 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from .Game import BasicGame
from World.Entities import Entity
from World.WorldEntities import *
from GUI.ObjWrappers.GUIEntity import GUIEntity
from World.WorldMath import intpos, friendly_type, PlayerStat, getPositionAwayFromOtherObjects
from GUI.GraphicsCache import Cache
from GUI.Helpers import debugfont
import logging
import pygame
from operator import attrgetter

# Game which keeps track of statistics about combat to score points
# Each ship is worth a number of points when killed equal to how long its been alive (this.timealive / 10)
#
# TODO: When a ship has been killed and respawns there will be 100 'revenge' points available to the ship destroyed if they can destroy the ship
#  that killed them.  This bonus decreases for every second elapsed since respawn.

# fraction based on damage?
# See Torpedo.owner

# Detect blocking w/ Shield and get points?
# Award points for Asteroids? Spawn Asteroids over time? (See Asteroid Miner?)
# TODO: Lose points if killed by Asteroid or self
class CombatExerciseGame(BasicGame):

    """
    def player_died(self, player, gone):
        if player.object != None and \
           player.object.killedby != None and \
           player.object.killedby.owner != None and \
           player.object.killedby.owner.player != None:
           player.object.killedby.owner.player.update_score(player.object.timealive / self.cfg.getint("CombatExercise", "points_time_alive_divide_by"))

        super(CombatExerciseGame, self).player_died(player, gone)
    """

    def world_add_remove_object(self, wobj, added):
        logging.debug("CE Add Object(%s): #%d (%s)", repr(added), wobj.id, friendly_type(wobj))
        if not added and isinstance(wobj, Asteroid) and hasattr(wobj, "killedby") and wobj.killedby != None:
            obj = wobj.killedby
            if isinstance(obj, Torpedo):
                obj.owner.player.update_score(self.cfg.getint("CombatExercise", "points_shoot_asteroid"))
                    
                logging.info("Torpedo Owner (#%d) Destroyed Asteroid", obj.owner.id)
            """
            elif isinstance(obj, Ship) and obj.health.value > 0:
                self.player_update_score(obj.player, self.__shippoints)
                    
                logging.info("Ship (#%d) Destroyed Asteroid", obj.id)
            """
        elif not added and isinstance(wobj, Ship) and hasattr(wobj, "killedby") and wobj.killedby != None:
            obj = wobj.killedby
            if isinstance(obj, Torpedo):
                obj.owner.player.update_score(wobj.timealive / self.cfg.getint("CombatExercise", "points_time_alive_divide_by"))

                logging.info("Torpedo Owner (#%d) Destroyed Ship (#%d)", obj.owner.id, wobj.id)
            elif isinstance(obj, Ship) and obj.health.value > 0:
                obj.player.update_score(wobj.timealive / self.cfg.getint("CombatExercise", "points_time_alive_divide_by"))
                    
                logging.info("Ship (#%d) Destroyed Ship (#%d)", obj.id, wobj.id)

        super(CombatExerciseGame, self).world_add_remove_object(wobj, added)

    def gui_draw_game_world_info(self, surface, flags, trackplayer):
        for player in self.game_get_current_player_list():
            obj = player.object
            if obj != None:
                # draw time alive by player
                text = self._dfont.render("%.1f" % obj.timealive, False, player.color)
                surface.blit(text, (obj.body.position[0]+30, obj.body.position[1]-4))
