
import pygame

MIN_STEP = 10

def SCache(enable=True):
    if not SoundCache._Instance:
        SoundCache._Instance = SoundCache("GUI/Sounds/", enable)
    return SoundCache._Instance

class SoundCache(object):
    """
    Loads Surface Images from Pygame and Stores them for Reuse
    """

    _Instance = None

    def __init__(self, rootdir="", enabled=True, ext="wav"):
        self.__rootdir = rootdir
        if ext != "":
            self.__ext = "." + ext
        else:
            self.__ext = ""
        self.__cache = {}
        self.__enabled = enabled

    def __getitem__(self, key):
        if not self.__cache.has_key(key):
            print "Loading Sound " + self.__rootdir + key + self.__ext
            self.__cache[key] = pygame.mixer.Sound(self.__rootdir + key + self.__ext)
        return self.__cache[key]  
   
    def play(self, key):
        if self.__enabled:
            self[key].play()