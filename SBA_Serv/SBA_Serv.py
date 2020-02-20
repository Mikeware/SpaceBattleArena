"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2020 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

__author__ = "Michael A. Hawker"
__copyright__ = "Copyright 2012-2020 Mikeware"
__license__ = "GPLv2"
__version__ = "1.3.0." + open("buildnum").read()
__email__ = "questions@mikeware.com"
__status__ = "Production"

title = "Space Battle Arena"
titlever = title + " v" + __version__

if __name__ == "__main__":
    import logging
    import datetime
    import threading
    import time

    import sys, traceback, glob, os.path
    from GUI import main
    from importlib import import_module

    import Server.WorldServer as WorldServer
    import World.WorldMap as WorldMap
    from Game.Game import BasicGame

    from optparse import OptionParser
    from configparser import ConfigParser

    from GUI.GraphicsCache import Cache
    from GUI.Helpers import detect_resolution

    import pygame

    parser = OptionParser(usage="Usage: %prog [options] [config_file] [more_config_files...]\n\nYou should pass at least one config file to the server. Additional config files will override/add to the options in the base file.")
    parser.add_option("-n", "--nolog", action="store_true", dest="nolog", default=False,
                      help="turns logging off")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                      help="turns logging to DEBUG (from INFO)")
    parser.add_option("-l", "--logfile", action="store", dest="logfilename", default="SBA_Serv"+datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")+".log",
                      help="specifies the file to log info to")
    """
    parser.add_option("-g", "--headless", action="store_true", dest="headless", default=False,
                      help="use to run the server without the GUI")
    """
    #TODO: Add verbosity...

    (options, args) = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()

        print("\n---\nIt is recommended to run Space Battle Arena with customized configuration.\nSee http://mikeware.github.io/SpaceBattleArena/server\n---\n\n")

    if not options.nolog:
        logformat='%(asctime)s|%(relativeCreated)d|%(levelname)s|%(threadName)s|%(module)s|%(lineno)d|%(funcName)s|%(message)s'
        if options.verbose:
            logging.basicConfig(level=logging.DEBUG, filename=options.logfilename, format=logformat)
        else:
            logging.basicConfig(level=logging.INFO, filename=options.logfilename, format=logformat)
        #eif
        logging.info("Starting " + titlever)
        print("Starting " + titlever)
        logging.info("Logging to " + options.logfilename + " Verbose: " + str(options.verbose))
        print("Logging to " + options.logfilename + " Verbose: " + str(options.verbose))
    else:
        print(" -- LOGGING DISABLED -- ")
    
    defaults = False
    cfg = ConfigParser()
    try:
        cfg.readfp(open('default.cfg')) #TODO: Need to fix? Warning Deprecated
        defaults = True
        logging.info("Loaded Default Configuration File")
    except:
        logging.error("Couldn't find default config file.")
        print("Couldn't load 'default.cfg' file, exiting...")

    if defaults:
        loaded_cfg_files = cfg.read(args)

        if len(loaded_cfg_files) != len(args):
            for file in loaded_cfg_files:
                args.remove(file)
            print("Issue Loading Configuration:", args)
            logging.error("Possible Config Files Not Loaded: %s", repr(args))

        logging.info("Loaded Configuration Files: %s", repr(loaded_cfg_files))

        if loaded_cfg_files == []:
            print("Loaded Default Configuration")
        else:
            print("Loaded Configuration:\n\t", "\n\t".join(loaded_cfg_files))
            print()

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
                resolution = detect_resolution(cfg)

            if width.find("x") != -1:
                cfg.set("World", "width", str(int(resolution[0] * float(width.replace("x",""))))) # as per doc, need to cast back to store as string, will unbox as int again later
            if height.find("x") != -1:
                cfg.set("World", "height", str(int(resolution[1] * float(height.replace("x","")))))

        max_images = cfg.getint("Application", "ship_images")
        # auto-detect number of ship images
        if max_images == 0:
            cfg.set("Application", "ship_images", str(Cache().getMaxImages("Ships/ship")+1)) # ship index starts at 0

        rungame = cfg.get("Game","game")

        print("Attempting to Load Game: ", rungame)

        game = None
        if rungame != "Basic" and rungame != None and rungame.strip() != "":
            mod = None
            try:
                mod = import_module("Game."+rungame)
                game = mod.__dict__[rungame+"Game"](cfg)
                logging.info("Running Game: " + rungame)
            except:
                logging.error("Could not start Game " + rungame)
                logging.info(traceback.format_exc())
                logging.error(traceback.format_exc())
                print(traceback.format_exc())        
        #eif
    
        if game == None or rungame == "Basic" or rungame == None or rungame.strip() == "":
            logging.info("Running Basic Game")
            title_game = ""
            game = BasicGame(cfg)
        else:
            title_game = " - " + rungame

        print("Game: ", game)
    
        logging.info("Starting Game Network Server...")

        server = WorldServer.WorldServer(cfg.getint("Server", "port"), game)

        #if options.headless:
            #logging.info("Running Headless without GUI")
            #TODO: Set World Size Here?
        #else:
        #startGame(title, game, fullscreen:bool, (xres, yres), showstats:bool, sound:bool)
        main.startGame(titlever + title_game, game, cfg.get("Application", "fullscreen"), resolution, cfg)

        print("Sending Disconnect...")
        logging.info("Server Request Disconnect All")
        server.disconnectAll()
        logging.info("Server exit main")
        time.sleep(0.5)

        print("Server Closed, Checking Threads...", end=' ')

        x = 0
        while len(threading.enumerate()) > 1 and x < 8:
            time.sleep(1)
            print("\b.", end=' ')
            x += 1

        print("\bDone!")

        tlist = threading.enumerate()
        if len(tlist) > 1: # main thread is counted
            logging.error("%d Threads Not Cleaned Up", len(tlist))
            for t in tlist:
                logging.error("Thread Not Cleaned Up %s:%s", t.getName(), repr(t))
                print(t.getName() + ":" + repr(t))
        
        pygame.quit()
    #eif
