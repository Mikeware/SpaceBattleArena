
import math

def friendly_type(obj):
    """
    Returns the classname of the object.
    """
    t = repr(type(obj))
    di = t.rfind('.')
    return t[di+1:t.find("'",di)]

def intpos(pos):
    """
    Returns a rounded position of the given position.
    """
    return (int(pos[0]), int(pos[1]))

def in_circle(center, radius, point): 
    """
    Determines if the given point is within the circle positioned at center with the given radius.
    """
    return (center[0] - point[0]) ** 2 + (center[1] - point[1]) ** 2  <= radius ** 2 

def wrappos(pos, bound, worldsize):
    """
    Returns an array of up to 5 points translated to wrap around the given worldsize.

    Parameters:
        pos: the position to wrap
        bound: distance away from the position that we care about, i.e. if the position coordinate +/- bound doesn't cross an edge, an extra point won't be generated in that direction
        worldsize: dimensions of the world
    """
    pl = [pos]
    if pos[0] < bound:
        pl.append((pos[0] + worldsize[0], pos[1]))
    elif pos[0] > worldsize[0] - bound:
        pl.append((pos[0] - worldsize[0], pos[1]))

    if pos[1] < bound:
        pl.append((pos[0], pos[1] + worldsize[1]))
    elif pos[1] > worldsize[1] - bound:
        pl.append((pos[0], pos[1] - worldsize[1]))

    return pl

def aligninstances(obj1, obj2, class1, class2):
    """
    aligninstances performs two functions, it ensures that obj1 & obj2 are of the types class1 & class2
    it then returns a tuple such that the first element is that of class1 and the second is class2
    
    in the case that there is a mismatch between object and type (the pair doesn't exist), None is returned for both
    """
    if isinstance(obj1, class1) and isinstance(obj2, class2):
        return obj1, obj2
    elif isinstance(obj2, class1) and isinstance(obj1, class2):
        return obj2, obj1

    return None, None

def distancesquared(pos1x, pos1y, pos2x, pos2y):
    return (pos1x - pos2x) ** 2 + (pos1y - pos2y) ** 2

# used by clients
def getlocalposdistance(pos1, pos2, worldsize):
    # Finds and returns the closest position
    poslist = [(pos2[0], pos2[1])]
    xneg = -1
    if pos2[0] > pos1[0]:
        poslist.append((pos2[0] - worldsize[0], pos2[1]))
    else:
        xneg = 1
        poslist.append((pos2[0] + worldsize[0], pos2[1]))
    #eif
    yneg = -1
    if pos2[1] > pos1[1]:
        poslist.append((pos2[0], pos2[1] - worldsize[1]))
    else:
        yneg = 1
        poslist.append((pos2[0], pos2[1] + worldsize[1]))
    #eif
    poslist.append((pos2[0] + worldsize[0] * xneg, pos2[1] + worldsize[1] * yneg))
    dstlist = []
    for pos in poslist:
        dstlist.append(distancesquared(pos1[0], pos1[1], pos[0], pos[1]))
    m = min(dstlist)
    return (poslist[dstlist.index(m)], m)

"""
class Velocity(object):
    represents the velocity of an object as a Vector
    Magnitude and Direction
    

    # Note: all arguments accept degrees, but is converted to radians internally

    def __init__(self, mag=0, dir=0):
        # Direction is in degrees
        self.__magnitude = mag
        self.__direction = math.radians(dir)

    def __getattr__(self, name):
        if name == "magnitude":
            return self.__magnitude
        elif name == "direction":
            return math.degrees(self.__direction)

    def accelerate(self, acc, dir, t):
        pass

    def clipMaxSpeed(self, speed):
        if self.__magnitude > speed:
            self.__magnitude = speed

    def updatePosition(self, pos, t):
        #Given a tuple for positon, returns a new position with this velocity vector applied
        return (pos[0] + self.__magnitude * math.cos(self.__direction) * t, pos[1] + self.__magnitude * math.sin(self.__direction) * t)
"""

class PlayerStat(object):
    """
    Defines a statistic for the player (e.g. Health, Energy, Shield)
    Is bound by a maximum value and can't go below zero.

    Note: It is assumed the object will be manipulated numerically after creation and not directly intereact with other PlayerStat objects.
    """
    def __init__(self, maxvalue, current=-1):
        self.__maximum = maxvalue
        if current == -1: 
            self.__current = maxvalue
        else:
            self.__current = self.__checkbound(current)        
        #eif

    def __getattr__(self, name):
        if name == "value":
            return self.__current
        elif name == "maximum":
            return self.__maximum
        elif name == "percent":
            return float(self.__current) / self.__maximum

    def __checkbound(self, value):
        if value < 0: value = 0
        elif value > self.__maximum: value = self.__maximum
        return value

    def __sub__(self, other):
        return PlayerStat(self.__maximum, self.__current - other)

    def __isub__(self, other):
        self.__current = self.__checkbound(self.__current - other)        
        return self

    def __add__(self, other):
        return PlayerStat(self.__maximum, self.__current + other)

    def __iadd__(self, other):
        self.__current = self.__checkbound(self.__current + other)
        return self

    def __mul__(self, other):
        return PlayerStat(self.__maximum, self.__current * other)

    def __imul__(self, other):
        self.__current = self.__checkbound(self.__current * other)
        return self

    def __div__(self, other):
        return PlayerStat(self.__maximum, self.__current / other)

    def __idiv__(self, other):
        self.__current = self.__checkbound(self.__current / other)
        return self

    def __pow__(self, other, modulo):
        return PlayerStat(self.__maximum, self.__current ** other)    

    def __ipow__(self, other, modulo):
        self.__current = self.__checkbound(self.__current ** other)
        return self

    def __cmp__(self, other):
        return self.__current - other

    def __lt__(self, other):
        return (self.__current - other) < 0

    def __le__(self, other):
        return (self.__current - other) <= 0

    def __eq__(self, other):
        return (self.__current - other) == 0

    def __ne__(self, other):
        return (self.__current - other) != 0

    def __gt__(self, other):
        return (self.__current - other) > 0

    def __ge__(self, other):
        return (self.__current - other) >= 0

    def empty(self):
        self.__current = 0

    def full(self):
        self.__current = self.__maximum

    def setMaximum(self, value):
        self.__maximum = value