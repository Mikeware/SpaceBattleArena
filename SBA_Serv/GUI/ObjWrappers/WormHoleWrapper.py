import pygame, random
import math

from .GUIEntity import GUIEntity
from World.WorldMath import intpos
from GUI.Helpers import wrapcircle, debugfont
from World.WorldEntities import WormHole
from GUI.GraphicsCache import Cache

class WormHoleGUI(GUIEntity):
    """description of class"""
    def __init__(self, wormhole, world):
        super(WormHoleGUI, self).__init__(wormhole, world)
        self._imageName = "WormHoles/WormHole"
        self._imageName = self._imageName + str(random.randint(1, Cache().getMaxImages(self._imageName)))
        #self._dist = wormhole.minor
        self.zorder = -4

    def draw(self, surface, flags):              
        bp = intpos(self._worldobj.body.position)
        rotimg = Cache().getRotatedImage(self._imageName, math.degrees(-self._worldobj.body.angle))
        w, h = rotimg.get_rect().size
        #TODO: convert world to graphics coordinates
        surface.blit(rotimg, (bp[0] -w/2, bp[1] -h/2))

        #if flags["DEBUG"]:
        #pygame.draw.line(surface, (64, 128, 255), bp, intpos(self._worldobj.body.position - (self._worldobj.pull / 50, 0)))
        if flags["DEBUG"]:
            bp = intpos(self._worldobj.body.position)
            wrapcircle(surface, (64, 64, 255), bp, self._worldobj.influence_range, self._world.size, 3)
            if self._worldobj.type == WormHole.RANDOM:
                # make 'X' for Random
                pygame.draw.line(surface, (64, 64, 255), intpos(self._worldobj.body.position - (self._worldobj.influence_range, self._worldobj.influence_range)), intpos(self._worldobj.body.position + (self._worldobj.influence_range, self._worldobj.influence_range)), 5)
                pygame.draw.line(surface, (64, 64, 255), intpos(self._worldobj.body.position - (-self._worldobj.influence_range, self._worldobj.influence_range)), intpos(self._worldobj.body.position + (-self._worldobj.influence_range, self._worldobj.influence_range)), 5)
            elif self._worldobj.type == WormHole.FIXED_POINT:
                pygame.draw.line(surface, (64, 64, 255), bp, intpos(self._worldobj.exit))
                wrapcircle(surface, (64, 64, 255), intpos(self._worldobj.exit), self._worldobj.radius // 2, self._world.size, 2) # 'target'
            elif self._worldobj.type == WormHole.OTHER_CELESTIALBODY:
                c = (64, 64, 255)
                if isinstance(self._worldobj.exit, WormHole) and isinstance(self._worldobj.exit.exit, WormHole) and self._worldobj.exit.exit == self._worldobj:
                    c = (128, 192, 255) # check if linked in both directions - make brighter if two-way wormhole
                pygame.draw.line(surface, c, bp, intpos(self._worldobj.exit.body.position))
                wrapcircle(surface, c, intpos(self._worldobj.exit.body.position), self._worldobj.radius // 2, self._world.size, 2) # 'target'

        super(WormHoleGUI, self).draw(surface, flags)


