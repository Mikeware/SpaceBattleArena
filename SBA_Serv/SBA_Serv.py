"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2015 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

__author__ = "Michael A. Hawker"
__copyright__ = "Copyright 2012-2015 Mikeware"
__license__ = "GPLv2"
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

parser = OptionParser(usage="Usage: %prog [options] [config_file] [more_config_files...]\n\nYou should pass at least one config file to the server. Additional config files will override/add to the options in the base file.")
parser.add_option("-n", "--nolog", action="store_true", dest="nolog", default=False,
                  help="turns logging off")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                  help="turns logging to DEBUG (from INFO)")
parser.add_option("-l", "--logfile", action="store", dest="logfilename", default="SBA_Serv.log",
                  help="specifies the file to log info to")
"""
parser.add_option("-g", "--headless", action="store_true", dest="headless", default=False,
                  help="use to run the server without the GUI")
"""
#TODO: Add verbosity...

(options, args) = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()

    print "\n---\nIt is recommended to run Space Battle Arena with customized configuration.\nSee http://mikeware.github.io/SpaceBattleArena/server\n---\n\n"

if not options.nolog:
    logformat='%(asctime)s|%(relativeCreated)d|%(levelname)s|%(threadName)s|%(module)s|%(lineno)d|%(funcName)s|%(message)s'
    if options.verbose:
        logging.basicConfig(level=logging.DEBUG, filename=options.logfilename, format=logformat)
    else:
        logging.basicConfig(level=logging.INFO, filename=options.logfilename, format=logformat)
    #eif
    logging.info("Starting " + titlever)
    logging.info("Logging to " + options.logfilename + " Verbose: " + str(options.verbose))
else:
    print " -- LOGGING DISABLED -- "
    
defaults = False
cfg = ConfigParser()
try:
    cfg.readfp(open('default.cfg'))
    defaults = True
    logging.info("Loaded Default Configuration File")
except:
    logging.error("Couldn't find default config file.")
    print "Couldn't load 'default.cfg' file, exiting..."

if defaults:
    loaded_cfg_files = cfg.read(args)

    logging.info("Loaded Configuration Files: %s", repr(loaded_cfg_files))

    if loaded_cfg_files == []:
        print "Loaded Default Configuration"
    else:
        print "Loaded Configuration:\n\t", "\n\t".join(loaded_cfg_files)
        print

    resolution = (cfg.getint("Application", "horz_res"), cfg.getint("Application", "vert_res"))

    # enable fullscreen resolution detection
    if resolution == (0, 0):
        resolution = None
    
    # See if we've specified we want relative world size to resolution
    width = cfg.get("World", "width")
    height = cfg.get("World", "height")
    if width.find("x") != -1 or height.find("x") != -1:
        if resolution == None:
            logging.info("Detecting Resolution...")
            import pygame
            pygame.display.init()
            resolution = pygame.display.list_modes()[0]
            logging.info("Using Resolution %s", repr(resolution))

        if width.find("x") != -1:
            cfg.set("World", "width", str(int(resolution[0] * float(width.replace("x",""))))) # as per doc, need to cast back to store as string, will unbox as int again later
        if height.find("x") != -1:
            cfg.set("World", "height", str(int(resolution[1] * float(height.replace("x","")))))

    rungame = cfg.get("Game","game")

    print "Attempting to Load Game: ", rungame

    game = None
    if rungame != "Basic" and rungame != None and rungame.strip() != "":
        mod = None
        try:
            mod = import_module("Game."+rungame)
            game = mod.__dict__[rungame+"Game"](cfg)
            logging.info("Running Game: " + rungame)
        except:
            logging.error("Could not start Game " + rungame)
            logging.error(traceback.format_exc())
            print traceback.format_exc()        
    #eif
    
    if game == None or rungame == "Basic" or rungame == None or rungame.strip() == "":
        logging.info("Running Basic Game")
        game = BasicGame(cfg)

    print "Game: ", game
    
    logging.info("Starting Game Network Server...")

    server = WorldServer.WorldServer(cfg.getint("Server", "port"), game)

    try:
        #if options.headless:
            #logging.info("Running Headless without GUI")
            #TODO: Set World Size Here?
        #else:
        #startGame(title, game, fullscreen:bool, (xres, yres), showstats:bool, sound:bool)
        main.startGame(titlever, game, cfg.getboolean("Application", "fullscreen"), resolution, cfg.getboolean("Application", "showstats"), cfg.getboolean("Application", "sound"))
    except:
        logging.error(traceback.format_exc())
        print traceback.format_exc()

    print "Sending Disconnect..."
    logging.debug("End of Main")
    server.disconnectAll()
    logging.debug("All done?")
    print "Server Closed."
#eif
