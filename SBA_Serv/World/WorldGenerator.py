
from World.WorldMap import GameWorld
from World.Entities import Planet, BlackHole, Asteroid
import random

class WorldGenerator(object):
    """description of class"""
    pass

def addObjectAwayFromOthers(world, radius, edgebuffer, force=False):    
    size = world.size
    x = random.randint(edgebuffer, size[0] - edgebuffer)
    y = random.randint(edgebuffer, size[1] - edgebuffer)
    i = 0
    while len(world.getObjectsInArea((x, y), radius, force)) > 0 and i < 15:
        i += 1
        x = random.randint(edgebuffer, size[0] - edgebuffer)
        y = random.randint(edgebuffer, size[1] - edgebuffer)
    return (x, y)

def SimpleWorld(size, numplanets=1, numblackholes=0, numasteroids=2):
    world = GameWorld(size)

    for p in xrange(numplanets):
        world.append(Planet(addObjectAwayFromOthers(world, 200, 100)))
    #next p 

    for bh in xrange(numblackholes):
        world.append(BlackHole(addObjectAwayFromOthers(world, 250, 100)))
    #next bh

    for ast in xrange(numasteroids):
        world.append(Asteroid(addObjectAwayFromOthers(world, 100, 30)))
    #next ast

    #world.append(Planet((100, 100)))

    return world

def ConfiguredWorld(game, cfg, pys=True):
    world = GameWorld(game, (cfg.getint("World","width"), cfg.getint("World","height")), pys)

    for p in xrange(cfg.getint("Planet", "number")):
        world.append(Planet(addObjectAwayFromOthers(world, 200, 100)))
    #next p 

    for bh in xrange(cfg.getint("BlackHole", "number")):
        world.append(BlackHole(addObjectAwayFromOthers(world, 250, 100)))
    #next bh

    for ast in xrange(cfg.getint("Asteroid", "number")):
        world.append(Asteroid(addObjectAwayFromOthers(world, 100, 30)))
    #next ast

    #world.append(Planet((100, 100)))

    return world
