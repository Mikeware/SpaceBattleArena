
import random
import pygame

class Star(object):
    SURFACE = pygame.image.load("GUI\Graphics\Backgrounds\stars.png")

    """description of class"""
    def __init__(self, pos):
        self.pos = (pos[0] - 4, pos[1] - 4)        
        self.curframe = 0
        self.maxframe = 8
        self.anispeed = random.randint(4, 16)
        self.anicount = 0
        self.set = random.randint(0, 3)

    def draw(self, surface):
        self.anicount += 1
        if self.anicount == self.anispeed:
            self.anicount = 0
            self.curframe += 1
            if self.curframe >= self.maxframe: self.curframe = 0

        surface.blit(Star.SURFACE, self.pos, pygame.Rect(8 * self.curframe, 8 * self.set, 8, 8))