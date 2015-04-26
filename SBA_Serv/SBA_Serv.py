__author__ = "Michael A. Hawker"
__copyright__ = "Copyright 2012-2014 Mikeware"
__license__ = "Proprietary"
__version__ = "0.95"
__email__ = "questions@mikeware.com"
__status__ = "alpha"

title = "Space Battle Arena"
titlever = title + " v" + __version__

import logging

import sys, traceback
from GUI import main

import Server.WorldServer as WorldServer
import World.WorldMap as WorldMap
from World.WorldGenerator import SimpleWorld
from Game.Game import BasicGame
from Game.CombatExercise import CombatExerciseGame
from Game.KingOfTheBubble import KingOfTheBubbleGame
from Game.AsteroidMiner import AsteroidMinerGame
from BaubleHunt.BaubleHunt import BaubleHuntGame
from BaubleHunt.BaubleHuntSCV import BaubleHuntSCVGame

from optparse import OptionParser
from ConfigParser import ConfigParser

parser = OptionParser()
parser.add_option("-c", "--config", type="string", dest="configfile",
                  help="specify configuration file used to configure game server")
parser.add_option("-2", "--config2", type="string", dest="configfile2",
                  help="specify a secondary configuration file to override defaults")
parser.add_option("-g", "--headless", action="store_true", dest="headless", default=False,
                  help="use to run the server without the GUI")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                  help="turns logging to DEBUG (from INFO)")
parser.add_option("-l", "--logfile", action="store", dest="logfilename", default="SBA_Serv.log",
                  help="specifies the file to log info to")
parser.add_option("-n", "--nolog", action="store_true", dest="nolog", default=False,
                  help="turns logging off")
#TODO: Add verbosity...

(options, args) = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
else:
    cfg = ConfigParser()
    cfg.readfp(open(options.configfile))
    if options.configfile2:
        cfg.read(options.configfile2)
    
    # School Server Project Resolution is 1280x1024
    # SimpleWorld((worldwidth, worldheight), numplanet, numblackhole, numasteroid)
    
    if not options.nolog:
        if options.verbose:
            logging.basicConfig(level=logging.DEBUG, filename=options.logfilename)
        else:
            logging.basicConfig(level=logging.INFO, filename=options.logfilename)
        #eif
        logging.info("Starting " + titlever)
        logging.info("Logging to " + options.logfilename + " Verbose: " + str(options.verbose))
    else:
        print "LOGGING DISABLED"          
    
    rungame = cfg.get("Game","rungame")
    if rungame == "BaubleHunt":
        game = BaubleHuntGame(cfg)
    elif rungame == "BaubleHuntSCV":
        game = BaubleHuntSCVGame(cfg)
    elif rungame == "CombatExercise":
        game = CombatExerciseGame(cfg)
    elif rungame == "KingOfTheBubble":
        game = KingOfTheBubbleGame(cfg)
    elif rungame == "AsteroidMiner":
        game = AsteroidMinerGame(cfg)
    else:
        game = BasicGame(cfg)
    #eif
    
    logging.info("Starting Game Network Server...")

    server = WorldServer.WorldServer(cfg.getint("Server", "port"), game)

    try:
        if options.headless:
            logging.info("Running Headless without GUI")
            #TODO: Set World Size Here?
        else:
            # startGame(title, world, fullscreen?, (xres, yres))
            main.startGame(titlever, game, cfg.getboolean("Screen", "fullscreen"), (cfg.getint("Screen", "horz_res"), cfg.getint("Screen", "vert_res")), cfg.getboolean("Screen", "showstats"), cfg.getboolean("Game", "sound"))
    except:
        logging.error(traceback.format_exc())
        print traceback.format_exc()

    logging.debug("End of Main")
    server.disconnectAll()
    logging.debug("All done?")