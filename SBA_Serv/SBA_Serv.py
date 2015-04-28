"""
Main Class to Start Server
"""

__author__ = "Michael A. Hawker"
__copyright__ = "Copyright 2012-2015 Mikeware"
__license__ = "Proprietary"
__version__ = "1.0"
__email__ = "questions@mikeware.com"
__status__ = "beta"

title = "Space Battle Arena"
titlever = title + " v" + __version__

import logging

import sys, traceback, glob, os.path
from GUI import main
from importlib import import_module

import Server.WorldServer as WorldServer
import World.WorldMap as WorldMap
from World.WorldGenerator import SimpleWorld
from Game.Game import BasicGame

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

    game = None
    if rungame != "BasicGame" or rungame.strip() != "" or rungame != None:
        mod = None
        try:
            mod = import_module("Game."+rungame)
            game = mod.__dict__[rungame+"Game"](cfg)
            logging.info("Running Game: " + rungame)
        except:
            pass #ignore
    #eif
    
    if game == None or rungame == "BasicGame" or rungame == None or rungame.strip() == "":
        logging.info("Running Basic Game")
        game = BasicGame(cfg)

    print "Game: ", game
    
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
