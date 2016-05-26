import pygame, random, math

from GUIEntity import GUIEntity
from World.WorldMath import intpos
from GUI.Helpers import wrapcircle, debugfont
from World.WorldEntities import Dragon
from GUI.GraphicsCache import Cache

class AsteroidGUI(GUIEntity):
    """
    GUI Wrapper for an Asteroid
    
    Rotates Image to be in line with Velocity
    Asteroid Tails are assumed to go to the top-left of the image

    Asteroids are not centered on their images, they're spaced in the bottom-right corner
    """
    def __init__(self, asteroid, world):
        super(AsteroidGUI, self).__init__(asteroid, world)
        if not hasattr(self, '_imageName'): # so Dragons can use this
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

class DragonGUI(AsteroidGUI):
    """
    GUI Wrapper for a Dragon (similar to Asteroid)
    
    Rotates Image to be in line with Velocity
    Asteroid Tails are assumed to go to the top-left of the image

    Dragons are not centered on their images, they're spaced in the bottom-right corner
    """
    def __init__(self, dragon, world):
        self._imageName = "Creatures/Dragon"
        super(DragonGUI, self).__init__(dragon, world)

    def draw(self, surface, flags):      
        super(DragonGUI, self).draw(surface, flags)

        # Draw Dragon attack area
        if flags["DEBUG"] and isinstance(self._worldobj, Dragon) and self._worldobj.influence_range > 0:
            bp = intpos(self._worldobj.body.position)
            wrapcircle(surface, (64, 64, 255), bp, self._worldobj.influence_range, self._world.size, 3)
            pygame.draw.line(surface, (64, 128, 255), intpos(self._worldobj.body.position - (0, self._worldobj.influence_range)), intpos(self._worldobj.body.position - (0, self._worldobj.influence_range + self._worldobj.attack_speed)))
            pygame.draw.line(surface, (64, 128, 255), intpos(self._worldobj.body.position - (self._worldobj.influence_range, 0)), intpos(self._worldobj.body.position - (self._worldobj.influence_range + self._worldobj.attack_speed, 0)))
            pygame.draw.line(surface, (64, 128, 255), intpos(self._worldobj.body.position + (self._worldobj.influence_range, 0)), intpos(self._worldobj.body.position + (self._worldobj.influence_range + self._worldobj.attack_speed, 0)))
            pygame.draw.line(surface, (64, 128, 255), intpos(self._worldobj.body.position + (0, self._worldobj.influence_range)), intpos(self._worldobj.body.position + (0, self._worldobj.influence_range + self._worldobj.attack_speed)))
            # radius
            surface.blit(debugfont().render(repr(self._worldobj.influence_range), False, (255, 255, 192)), intpos((bp[0], bp[1] - self._worldobj.influence_range - 16)))

            # speed
            surface.blit(debugfont().render(repr(int(self._worldobj.body.velocity.length)), False, (255, 255, 255)), (bp[0]+20, bp[1]))

            if self._worldobj.target != None:
                # highlight
                wrapcircle(surface, (64, 64, 192), intpos(self._worldobj.target[1].body.position), 32, self._world.size, 2)

            #TODO: Highlight Target
