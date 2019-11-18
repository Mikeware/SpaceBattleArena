import pygame, random
import math

from .GUIEntity import GUIEntity
from World.WorldMath import intpos
from GUI.Helpers import wrapcircle, debugfont
from World.WorldEntities import Quasar
from GUI.GraphicsCache import Cache

class NebulaGUI(GUIEntity):
    """description of class"""
    def __init__(self, nebula, world):
        super(NebulaGUI, self).__init__(nebula, world)
        if isinstance(nebula, Quasar):
            self._imageName = "Nebula/Quasar"
        else:
            self._imageName = "Nebula/Nebula"
        self._imageName += repr(int(nebula.major) * 2) + "x" + repr(int(nebula.minor) * 2) + "-"
        self._imageName += str(random.randint(1, Cache().getMaxImages(self._imageName)))
        self._dist = nebula.minor
        self.zorder = -5

    def draw(self, surface, flags):              
        bp = intpos(self._worldobj.body.position)
        rotimg = Cache().getRotatedImage(self._imageName, math.degrees(-self._worldobj.body.angle))
        w, h = rotimg.get_rect().size
        #TODO: convert world to graphics coordinates
        surface.blit(rotimg, (bp[0] -w/2, bp[1] -h/2))

        if flags["DEBUG"]:            
            pygame.draw.line(surface, (64, 128, 255), bp, intpos(self._worldobj.body.position - (self._worldobj.pull / 50, 0)))

        super(NebulaGUI, self).draw(surface, flags)


