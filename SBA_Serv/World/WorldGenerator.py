"""
Module with functions related to World Generation. (i.e. placement of Planets, BlackHoles, and Asteroids)
"""

from World.WorldMap import GameWorld
from World.WorldEntities import Planet, BlackHole, Asteroid, Nebula, Star, Dragon
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

def ConfiguredWorld(game, cfg, pys=True, empty=False, objlistener=None):
    """Generates a World from a Configuration Object.

    Args:
        game: Game object.
        cfg: ConfigParser object.
        pys: Physics flag.
        empty: if you want to populate the world with objects (used for testing)

    Returns:
        new World object.
    """
    world = GameWorld(game, (cfg.getint("World","width"), cfg.getint("World","height")), pys, objlistener)

    if not empty:
        for neb in xrange(cfg.getint("Nebula", "number")):
            spawn_Nebula(world, cfg)
        #next ast

        for p in xrange(cfg.getint("Planet", "number")):
            spawn_Planet(world, cfg)
        #next p 

        for bh in xrange(cfg.getint("BlackHole", "number")):
            spawn_BlackHole(world, cfg)
        #next bh

        for s in xrange(cfg.getint("Star", "number")):
            spawn_Star(world, cfg)
        #next bh

        for ast in xrange(cfg.getint("Asteroid", "number")):
            spawn_Asteroid(world, cfg)
        #next ast

        for dragon in xrange(cfg.getint("Dragon", "number")):
            spawn_Dragon(world, cfg)
        #next dragon
    #eif

    return world

def spawn_Nebula(world, cfg, pos=None):
    if pos == None:
        pos = getPositionAwayFromOtherObjects(world, 30, 30)
    world.append(Nebula(pos, random.choice(eval(cfg.get("Nebula", "sizes"))), cfg_rand_min_max(cfg, "Nebula", "pull")))

def spawn_Planet(world, cfg, pos=None):
    if pos == None:
        pos = getPositionAwayFromOtherObjects(world, 200, 100)
    world.append(Planet(pos, cfg_rand_min_max(cfg, "Planet", "range"), cfg_rand_min_max(cfg, "Planet", "pull")))

def spawn_BlackHole(world, cfg, pos=None):
    if pos == None:
        pos = getPositionAwayFromOtherObjects(world, 250, 100)
    world.append(BlackHole(pos, cfg_rand_min_max(cfg, "BlackHole", "range"), cfg_rand_min_max(cfg, "BlackHole", "pull")))

def spawn_Star(world, cfg, pos=None):
    if pos == None:
        pos = getPositionAwayFromOtherObjects(world, 250, 100)
    world.append(Star(pos, cfg_rand_min_max(cfg, "Star", "range"), cfg_rand_min_max(cfg, "Star", "pull")))

def spawn_Asteroid(world, cfg, pos=None):
    if pos == None:
        pos = getPositionAwayFromOtherObjects(world, 100, 30)
    world.append(Asteroid(pos))

def spawn_Dragon(world, cfg, pos=None):
    if pos == None:
        pos = getPositionAwayFromOtherObjects(world, 128, 16)
    world.append(Dragon(pos, cfg_rand_min_max(cfg, "Dragon", "range"), cfg_rand_min_max(cfg, "Dragon", "attack_speed"), cfg_rand_min_max(cfg, "Dragon", "health")))

def cfg_rand_min_max(cfg, section, option):
    """Helper method to generate a random int for a config option.

    Config option should be in the form of option_min = value and option_max = value.

    Args:
        cfg: ConfigParser object.
        section: Configuration section name.
        option: Configuration option name.
    """
    return random.randint(cfg.getint(section, option+"_min"), cfg.getint(section, option+"_max"))
