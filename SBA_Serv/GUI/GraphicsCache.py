
import pygame

MIN_STEP = 10

def Cache():
    if not GraphicsCache._Instance:
        GraphicsCache._Instance = GraphicsCache("GUI/Graphics/")
    return GraphicsCache._Instance

class GraphicsCache(object):
    """
    Loads Surface Images from Pygame and Stores them for Reuse
    """

    _Instance = None

    def __init__(self, rootdir="", ext="png"):
        self.__rootdir = rootdir
        if ext != "":
            self.__ext = "." + ext
        else:
            self.__ext = ""
        self.__cache = {}

    def getImage(self, key):
        if not self.__cache.has_key(key):
            self.__cache[key] = {}
            self.__cache[key][0] = pygame.image.load(self.__rootdir + key + self.__ext).convert_alpha()
        return self.__cache[key][0]  
   
    def getRotatedImage(self, key, angle): 
        #return pygame.transform.rotate(self.getImage(key), angle)               
        while angle < 0:
            angle += 360
        while angle > 360:
            angle -= 360
        angle = int(angle / MIN_STEP + 0.5) * MIN_STEP
        image = None
        if not self.__cache.has_key(key):            
            image = self.getImage(key)
        main = self.__cache[key]
        if not main.has_key(angle):
            if image == None:
                image = main[0]
            main[angle] = pygame.transform.rotate(image, angle).convert_alpha()
        return main[angle]        
