
import pygame

__df = None
__nf = None
__if = None

def debugfont():
    global __df
    if __df == None:
        __df = pygame.font.Font("freesansbold.ttf", 12)
    
    return __df

def infofont():
    global __if
    if __if == None:
        __if = pygame.font.Font("freesansbold.ttf", 16)
    
    return __if
    
def namefont():
    global __nf
    if __nf == None:
        __nf = pygame.font.Font("freesansbold.ttf", 22)
    
    return __nf

def wrapcircle(surface, color, pos, radius, worldsize, thickness=0):
    pygame.draw.circle(surface, color, pos, radius, thickness)
    if pos[0] < radius:
        pygame.draw.circle(surface, color, (pos[0] + worldsize[0], pos[1]), radius, thickness)
    elif pos[0] > worldsize[0] - radius:
        pygame.draw.circle(surface, color, (pos[0] - worldsize[0], pos[1]), radius, thickness)

    if pos[1] < radius:
        pygame.draw.circle(surface, color, (pos[0], pos[1] + worldsize[1]), radius, thickness)
    elif pos[1] > worldsize[1] - radius:
        pygame.draw.circle(surface, color, (pos[0], pos[1] - worldsize[1]), radius, thickness)
