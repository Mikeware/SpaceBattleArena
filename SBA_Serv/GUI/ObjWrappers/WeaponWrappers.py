import pygame

from GUIEntity import GUIEntity
from World.WorldCommands import ThrustCommand, BrakeCommand, WarpCommand
from World.WorldMath import intpos
from GUI.Helpers import wrapcircle, debugfont, namefont
from GUI.GraphicsCache import Cache

class TorpedoGUI(GUIEntity):
    def __init__(self, obj, world):
        super(TorpedoGUI, self).__init__(obj, world)
        self.surface = Cache().getImage("Ships/Torpedo")

    def draw(self, surface, flags):
        bp = intpos(self._worldobj.body.position)
        surface.blit(self.surface, (bp[0] - 4, bp[1] - 4))
        
        if flags["DEBUG"]:                        
            # position text
            #surface.blit(debugfont().render(repr((bp[0], bp[1])), False, (192, 192, 192)), (bp[0]-30, bp[1]-self._worldobj.radius-30))
            # id text
            surface.blit(debugfont().render("#"+str(self._worldobj.id), False, (192, 192, 192)), (bp[0]-4, bp[1]+self._worldobj.radius+4))

        #super(TorpedoGUI, self).draw(surface, flags)

class SpaceMineGUI(GUIEntity):
    _mine_surface = None

    def __init__(self, obj, world):
        super(SpaceMineGUI, self).__init__(obj, world)
        if SpaceMineGUI._mine_surface == None:
            SpaceMineGUI._mine_surface = Cache().getImage("Mines/Mine")

    def draw(self, surface, flags):
        bp = intpos(self._worldobj.body.position)
        surface.blit(SpaceMineGUI._mine_surface.subsurface(pygame.Rect(16 * (self._worldobj.active + (self._worldobj.target != None)), 0, 16, 16)), (bp[0] - 8, bp[1] - 8))
        
        if flags["DEBUG"]:                        
            # position text
            if self._worldobj.mode == 3:
                surface.blit(debugfont().render(repr(self._worldobj.target), False, (192, 192, 192)), (bp[0]-30, bp[1]-self._worldobj.radius-4))
            # id text
            surface.blit(debugfont().render("#"+str(self._worldobj.id)+" "+repr(self._worldobj.mode), False, (192, 192, 192)), (bp[0]-8, bp[1]+self._worldobj.radius+4))

        #super(TorpedoGUI, self).draw(surface, flags)
