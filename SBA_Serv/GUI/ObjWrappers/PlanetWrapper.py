import pygame, random

from .GUIEntity import GUIEntity
from World.WorldMath import intpos
from GUI.Helpers import wrapcircle, debugfont
from World.WorldEntities import BlackHole, Star, Influential, Constellation
from GUI.GraphicsCache import Cache

class PlanetGUI(GUIEntity):
    """description of class"""
    def __init__(self, planet, world):
        super(PlanetGUI, self).__init__(planet, world)

        self.anicount = 0
        self.anirot = 0

        if isinstance(planet, BlackHole):
            self._imageName = "Planets/BlackHole"
            self.anispeed = random.randint(12, 24)
            self.anidirection = -1
            self.zorder = -3
        elif isinstance(planet, Star):
            self._imageName = "Planets/Star"
            self.anispeed = random.randint(2, 4)
            self.anidirection = -1
            self.zorder = -2
        elif isinstance(planet, Constellation):
            self._imageName = "Constellations/Constellation"
            self.anispeed = 0
            self.anidirection = 0
            self.anirot = random.randint(-180, 180)
            self.zorder = -4
        else:
            self._imageName = "Planets/Planet"
            self.anispeed = random.randint(24, 48)
            self.anidirection = random.randint(0, 1)
            self.zorder = -1
        #eif
        self._imageName = self._imageName + str(random.randint(1, Cache().getMaxImages(self._imageName)))
        
        if self.anidirection == 0: self.anidirection = -1

    def draw(self, surface, flags):      
        self.anicount += 1
        if self.anicount == self.anispeed:
            self.anicount = 0
            self.anirot += self.anidirection
            if self.anirot >= 360: self.anirot = 0
            elif self.anirot <= 0: self.anirot = 360
        rotimg = Cache().getRotatedImage(self._imageName, self.anirot)
        w, h = rotimg.get_rect().size
        #TODO: convert world to graphics coordinates
        surface.blit(rotimg, (self._worldobj.body.position[0] -w/2, self._worldobj.body.position[1] -h/2))

        if flags["DEBUG"] and isinstance(self._worldobj, Influential) and self._worldobj.influence_range > 0:
            bp = intpos(self._worldobj.body.position)
            wrapcircle(surface, (64, 64, 255), bp, self._worldobj.influence_range, self._world.size, 3)
            pygame.draw.line(surface, (64, 128, 255), intpos(self._worldobj.body.position - (0, self._worldobj.influence_range)), intpos(self._worldobj.body.position - (0, self._worldobj.influence_range - self._worldobj.pull)))
            pygame.draw.line(surface, (64, 128, 255), intpos(self._worldobj.body.position - (self._worldobj.influence_range, 0)), intpos(self._worldobj.body.position - (self._worldobj.influence_range - self._worldobj.pull, 0)))
            pygame.draw.line(surface, (64, 128, 255), intpos(self._worldobj.body.position + (self._worldobj.influence_range, 0)), intpos(self._worldobj.body.position + (self._worldobj.influence_range - self._worldobj.pull, 0)))
            pygame.draw.line(surface, (64, 128, 255), intpos(self._worldobj.body.position + (0, self._worldobj.influence_range)), intpos(self._worldobj.body.position + (0, self._worldobj.influence_range - self._worldobj.pull)))
            # radius
            surface.blit(debugfont().render(repr(self._worldobj.influence_range), False, (255, 255, 192)), intpos((bp[0], bp[1] - self._worldobj.influence_range - 16)))

        super(PlanetGUI, self).draw(surface, flags)