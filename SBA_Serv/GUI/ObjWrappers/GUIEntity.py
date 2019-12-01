
import pygame
from World.Entities import Entity
from World.WorldMath import intpos
from GUI.Helpers import wrapcircle, debugfont, namefont
from GUI.GraphicsCache import Cache

class GUIEntity(object):
    _healthbar = None
    _energybar = None

    def __init__(self, worldobj, world):
        self._worldobj = worldobj
        self._world = world
        self.dying = False
        self.dead = False
        self._points = None
        if "points" in self._worldobj.__dict__:
            self._dist = int(max(self._worldobj.points[0]))
            self._points = self.get_world_points(self._worldobj)
            self._lp = self._worldobj.body.position.int_tuple
        elif "radius" in self._worldobj.__dict__:
            self._dist = int(self._worldobj.radius)
        else:
            self._dist = 16

        if GUIEntity._healthbar == None:
            GUIEntity._healthbar = Cache().getImage("HUD/Health")
            GUIEntity._energybar = Cache().getImage("HUD/Energy")

    def draw(self, surface, flags, pos_override = None): # pos_override for ship debug tracker in GUI
        if pos_override != None:
            bp = pos_override
        else:
            bp = self._worldobj.body.position.int_tuple

        if self._points != None and bp != self._lp:
            self._lp = bp
            self._points = self.get_world_points(self._worldobj)

        if flags["DEBUG"]:
            # position text
            surface.blit(debugfont().render(repr((bp[0], bp[1])), False, (192, 192, 192)), (bp[0]-30, bp[1]-self._dist-30))
            # id text
            surface.blit(debugfont().render("#"+str(self._worldobj.id), False, (192, 192, 192)), (bp[0]-4, bp[1]+self._dist+4))
            # collision circle
            if "points" in self._worldobj.__dict__: #Polygon
                if len(self._worldobj.in_celestialbody) > 0:
                    self.draw_poly(surface, (255, 64, 64), bp, self._points, 4)
                else:
                    self.draw_poly(surface, (192, 192, 192), bp, self._points, 2)
            else: 
                if len(self._worldobj.in_celestialbody) > 0:
                    wrapcircle(surface, (255, 64, 64), bp, self._dist, self._world.size, 4)
                else:
                    wrapcircle(surface, (192, 192, 192), bp, self._dist, self._world.size, 2)            

            # velocity vector
            pygame.draw.line(surface, (255, 0, 0), bp, self._worldobj.body.velocity + bp) # Velocity

        if flags["STATS"] and self._worldobj.health.maximum > 0:
            # Health Bar Background
            pygame.draw.rect(surface, (64, 0, 0), pygame.Rect(bp[0]-16, bp[1] - 25, 32, 8))

            if flags["DEBUG"]:
                surface.blit(debugfont().render(repr(int(100 * self._worldobj.health.percent)), False, (255, 255, 255)), (bp[0]+18, bp[1] - 26))
            # Health Bar
            surface.blit(GUIEntity._healthbar, (bp[0]-15, bp[1] - 24), pygame.Rect(0, 0, 30 * self._worldobj.health.percent, 6))
        
        if flags["STATS"] and self._worldobj.energy.maximum > 0:
            # Energy Bar
            pygame.draw.rect(surface, (0, 64, 0), pygame.Rect(bp[0]-16, bp[1] + 26, 32, 5))

            if flags["DEBUG"]:
                surface.blit(debugfont().render(repr(int(100 * self._worldobj.energy.percent)), False, (255, 255, 255)), (bp[0]+18, bp[1] + 24))
            surface.blit(GUIEntity._energybar, (bp[0]-15, bp[1] + 27), pygame.Rect(0, 0, 30 * self._worldobj.energy.percent, 3))

    def draw_poly(self, surface, color, position, points, width=1):
        pygame.draw.lines(surface, color, False, points, width)

    def get_world_points(self, worldobj):
        points = []
        # rotate to world coordinates http://www.pymunk.org/en/latest/pymunk.html#pymunk.Poly.get_vertices
        for vertex in worldobj.shape.get_vertices():
            points += [(vertex.rotated(worldobj.body.angle) + worldobj.body.position).int_tuple]
        points += [points[0]] # close loop

        return points

    def __eq__(self, other):
        if isinstance(self, GUIEntity) and isinstance(other, GUIEntity):
            return self._worldobj == other._worldobj
        elif isinstance(self, GUIEntity) and isinstance(other, Entity):
            return self._worldobj == other
        else:
            return False