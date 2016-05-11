"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2016 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

from Game import BasicGame
from World.Entities import Entity
from World.WorldEntities import Ship
from GUI.ObjWrappers.GUIEntity import GUIEntity
from World.WorldMath import intpos, friendly_type, PlayerStat, in_circle, getPositionAwayFromOtherObjects
from GUI.GraphicsCache import Cache
from GUI.Helpers import debugfont, wrapcircle, namefont
import logging, random
import pygame

# Basic Game - Find The Middle
# Preliminary Exercise to introduce students to the world of Space Battle
# 
# Creates a circle in the middle of the world
# Students must create a ship to navigate to the center of the world
# Once there for a sufficient amount of time, they will be warped away, and must try again

class FindTheMiddleGame(BasicGame):
    
    def __init__(self, cfgobj):
        self.__objective_radii = map(int, cfgobj.get("FindTheMiddle", "objective_radii").split(","))
        self.__objective_points = map(int, cfgobj.get("FindTheMiddle", "objective_points").split(","))
        self.__objective_time = float(cfgobj.getint("FindTheMiddle", "objective_time"))
        self.__objective_velocity = cfgobj.getint("FindTheMiddle", "objective_velocity")
        self.__reset_timer = cfgobj.getboolean("FindTheMiddle", "reset_timer")

        super(FindTheMiddleGame, self).__init__(cfgobj)

    def world_create(self):
        self.midpoint = (int(self.world.width / 2), int(self.world.height / 2))

        super(FindTheMiddleGame, self).world_create()

    def player_added(self, player, reason):
        player.time = 0

        super(FindTheMiddleGame, self).player_added(player, reason)

    def player_get_stat_string(self, player):
        return repr(int(player.score)) + "  " + player.name
    
    def player_get_start_position(self, force=False):
        # make sure player doesn't spawn in middle
        pos = (random.randint(50, self.world.width - 50),
               random.randint(50, self.world.height - 50))
        x = 0
        while ((len(self.world.getObjectsInArea(pos, 75)) > 0 and x < 25) or in_circle(self.midpoint, self.__objective_radii[-1] + 32, pos)):
            x += 1
            pos = (random.randint(50, self.world.width - 50),
                   random.randint(50, self.world.height - 50))
        return pos

    def game_update(self, t):
        if self.round_get_has_started():
            ships = []
            for obj in self.world.getObjectsInArea(self.midpoint, self.__objective_radii[-1] + 28): # add the ship radius so it looks like you get points if you overlap
                if isinstance(obj, Ship):
                    ships.append(obj)
        
            # decrease the time for ships that are moving slowly in the bubble
            for ship in ships:
                if ship.body.velocity.length < self.__objective_velocity:
                    ship.player.time += t
                    if ship.player.time >= self.__objective_time:
                        # slowed enough, figure out how many points to give
                        x = 0
                        for radius in self.__objective_radii:
                            if in_circle(self.midpoint, radius + 28, ship.body.position):
                                break
                            x += 1
                        ship.body.position = self.player_get_start_position() 
                        self.player_update_score(ship.player, self.__objective_points[x])
                        ship.player.time = 0
                elif self.__reset_timer:
                    ship.player.time = 0

        super(FindTheMiddleGame, self).game_update(t)

    def gui_draw_game_world_info(self, surface, flags, trackplayer):
        # Draw circles in middle of world
        if self.round_get_has_started():
            x = 1
            inc = int(255 / len(self.__objective_radii))
            for radius in self.__objective_radii:
                pygame.draw.circle(surface, (0, inc * x, 255 - inc * x), self.midpoint, radius, len(self.__objective_radii) - x + 1)
                text = self._dfont.render(repr(int(self.__objective_points[x-1])) + " Points", False, (128, 128, 128))
                surface.blit(text, (self.midpoint[0]-text.get_width()/2, self.midpoint[1]-radius+18))
                text = self._dfont.render("Radius " + repr(int(self.__objective_radii[x-1])), False, (128, 128, 128))
                surface.blit(text, (self.midpoint[0]-text.get_width()/2, self.midpoint[1]+radius-36))
                x += 1

            for player in self.game_get_current_player_list():
                obj = player.object
                if obj != None and player.time > 0:
                    # draw time left in bubble for player
                    text = self._dfont.render("%.1f" % (self.__objective_time - player.time), False, player.color)
                    surface.blit(text, (obj.body.position[0]+30, obj.body.position[1]-4))
