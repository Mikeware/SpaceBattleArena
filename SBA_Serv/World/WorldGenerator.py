"""
Module with functions related to World Generation. (i.e. placement of Planets, BlackHoles, and Asteroids)
"""

from World.WorldMap import GameWorld
from World.WorldEntities import Planet, BlackHole, Asteroid
import random

def getPositionAwayFromOtherObjects(world, radius, edgebuffer, force=False):
    """Returns a Position in the world that is away from other objects in it.

    Args:
        radius: integer range to detect other objects.
        edgebuffer: integer range to keep away from the edge of the world.
        force: internal for the physics engine.

    Returns:
        position tuple
    """
    size = world.size
    x = random.randint(edgebuffer, size[0] - edgebuffer)
    y = random.randint(edgebuffer, size[1] - edgebuffer)
    i = 0
    while len(world.getObjectsInArea((x, y), radius, force)) > 0 and i < 15:
        i += 1
        x = random.randint(edgebuffer, size[0] - edgebuffer)
        y = random.randint(edgebuffer, size[1] - edgebuffer)
    return (x, y)

def SimpleWorld(game, size, numplanets=1, numblackholes=0, numasteroids=2):
    """Returns a simple world object with the number of objects specified.

    Args:
        game: Game object.
        size: (width, height) tuple.
        numplanets: integer Number of Planets.
        numblackholes: integer Number of BlackHoles.
        numasteroids: integer Number of Asteroids.

    Returns:
        new World object.
    """
    world = GameWorld(game, size)

    for p in xrange(numplanets):
        world.append(Planet(getPositionAwayFromOtherObjects(world, 200, 100)))
    #next p 

    for bh in xrange(numblackholes):
        world.append(BlackHole(getPositionAwayFromOtherObjects(world, 250, 100)))
    #next bh

    for ast in xrange(numasteroids):
        world.append(Asteroid(getPositionAwayFromOtherObjects(world, 100, 30)))
    #next ast

    #world.append(Planet((100, 100)))

    return world

def ConfiguredWorld(game, cfg, pys=True):
    """Generates a World from a Configuration Object.

    Args:
        game: Game object.
        cfg: ConfigParser object.
        pys: Physics flag.

    Returns:
        new World object.
    """
    world = GameWorld(game, (cfg.getint("World","width"), cfg.getint("World","height")), pys)

    for p in xrange(cfg.getint("Planet", "number")):
        world.append(Planet(getPositionAwayFromOtherObjects(world, 200, 100)))
    #next p 

    for bh in xrange(cfg.getint("BlackHole", "number")):
        world.append(BlackHole(getPositionAwayFromOtherObjects(world, 250, 100)))
    #next bh

    for ast in xrange(cfg.getint("Asteroid", "number")):
        world.append(Asteroid(getPositionAwayFromOtherObjects(world, 100, 30)))
    #next ast

    #world.append(Planet((100, 100)))

    return world
