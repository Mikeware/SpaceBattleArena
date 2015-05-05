"""
Module with functions related to World Generation. (i.e. placement of Planets, BlackHoles, and Asteroids)
"""

from World.WorldMap import GameWorld
from World.WorldEntities import Planet, BlackHole, Asteroid, Nebula
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

    av_sizes = eval(cfg.get("Nebula", "sizes"))
    for neb in xrange(cfg.getint("Nebula", "number")):
        world.append(Nebula(getPositionAwayFromOtherObjects(world, 30, 30), random.choice(av_sizes), cfg_rand_min_max(cfg, "Nebula", "pull")))
    #next ast

    for p in xrange(cfg.getint("Planet", "number")):
        world.append(Planet(getPositionAwayFromOtherObjects(world, 200, 100), cfg_rand_min_max(cfg, "Planet", "range"), cfg_rand_min_max(cfg, "Planet", "pull")))
    #next p 

    for bh in xrange(cfg.getint("BlackHole", "number")):
        world.append(BlackHole(getPositionAwayFromOtherObjects(world, 250, 100), cfg_rand_min_max(cfg, "BlackHole", "range"), cfg_rand_min_max(cfg, "BlackHole", "pull")))
    #next bh

    for ast in xrange(cfg.getint("Asteroid", "number")):
        world.append(Asteroid(getPositionAwayFromOtherObjects(world, 100, 30)))
    #next ast

    #world.append(Planet((100, 100)))

    return world

def cfg_rand_min_max(cfg, section, option):
    """Helper method to generate a random int for a config option.

    Config option should be in the form of option_min = value and option_max = value.

    Args:
        cfg: ConfigParser object.
        section: Configuration section name.
        option: Configuration option name.
    """
    return random.randint(cfg.getint(section, option+"_min"), cfg.getint(section, option+"_max"))
