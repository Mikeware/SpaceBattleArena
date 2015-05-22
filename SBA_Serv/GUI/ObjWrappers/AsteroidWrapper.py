import pygame, random, math

from GUIEntity import GUIEntity
from World.WorldMath import intpos
from GUI.Helpers import wrapcircle
from GUI.GraphicsCache import Cache

class AsteroidGUI(GUIEntity):
    """
    GUI Wrapper for an Asteroid
    
    Rotates Image to be in line with Velocity
    Asteroid Tails are assumed to go to the top-left of the image

    Asteroids are not centered on their images, they're spaced in the bottom-right corner
    """
    def __init__(self, planet, world):
        super(AsteroidGUI, self).__init__(planet, world)
        self._imageName = "Asteroids/Asteroid"
        self._imageName = self._imageName + str(random.randint(1, Cache().getMaxImages(self._imageName)))
        self.__extra = (Cache().getImage(self._imageName).get_width() - 32) / 1.5

    def draw(self, surface, flags):      
        ang = 45 - self._worldobj.body.velocity.angle_degrees
        rang = math.radians(self._worldobj.body.velocity.angle_degrees)
        #rotimg = pygame.transform.rotate(self.surface, ang)
        rotimg = Cache().getRotatedImage(self._imageName, ang)
        w, h = rotimg.get_rect().size
        #TODO: convert world to graphics coordinates
        surface.blit(rotimg, (self._worldobj.body.position[0] - w / 2 - self.__extra * math.cos(rang), self._worldobj.body.position[1] - h / 2 - self.__extra * math.sin(rang)))

        super(AsteroidGUI, self).draw(surface, flags)