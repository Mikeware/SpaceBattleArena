"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2016 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

import pygame, sys, random, logging, math, datetime
from collections import deque
from pygame.locals import *
from operator import attrgetter

# REQUIRED FOR DEPENDENCIES IN LOADING
from World.WorldMap import GameWorld

from ObjWrappers.ShipWrapper import ShipGUI
from ObjWrappers.NebulaWrapper import NebulaGUI
from ObjWrappers.PlanetWrapper import PlanetGUI
from ObjWrappers.AsteroidWrapper import AsteroidGUI
from ObjWrappers.WormHoleWrapper import WormHoleGUI
from ObjWrappers.WeaponWrappers import TorpedoGUI, SpaceMineGUI
from Game.Utils import SpawnManager
from GraphicsCache import Cache
from World.WorldEntities import Ship, Planet, Asteroid, Torpedo, SpaceMine, BlackHole, Nebula, Star, Dragon, WormHole
from Server.MWNL2 import getIPAddress
from pymunk import Vec2d
from Helpers import infofont
from ThreadStuff.ThreadSafe import ThreadSafeDict
import threading, thread, traceback
from SoundCache import SCache

STAR_DENSITY = 75 # Higher = Less Stars

class MessageLogHandler(logging.Handler):
    def __init__(self, maxmessages=20):
        super(MessageLogHandler, self).__init__()
        self.__max = maxmessages
        self.messages = deque()
        self.filter = None

    def handle(self, record):        
        if len(self.messages) == self.__max:
            self.messages.popleft();
        if self.filter == None or (self.filter != None and str(record.message).find(self.filter) != -1):
            self.messages.append(record.message)

def startGame(windowcaption, game, fullscreen=True, resolution=None, cfg=None, testcase=None):
    try:
        #region Initialization
        logging.info("Initiating PyGame...")

        world = game.world
        pygame.init()
        fpsClock = pygame.time.Clock()

        logging.debug("Initiating Screen...")

        if cfg.getboolean("Application", "sound"):
            logging.info("Starting Sound...")
            pygame.mixer.init()
            SCache(True)
        else:
            logging.info("Sound Disabled")
            SCache(False)
    
        ipaddress = getIPAddress()

        if resolution == None:
            resolution = pygame.display.list_modes()[0]

        windowSurface = pygame.display.set_mode(resolution, (pygame.FULLSCREEN * fullscreen) | pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption(windowcaption)

        logging.debug("Game GUI CFG...")
        # Let game initialize any GUI objects independently
        game.gui_initialize()

        colorBlack = pygame.Color(0, 0, 0)

        #shipw = ShipGUI(Ship((100, 100)))
        #shipw.ship.velocity.magnitude = 5

        #region World Registration
        bgobjects = ThreadSafeDict() # items we want always in the background
        objects = ThreadSafeDict()
        trackplayer = None
        def addorremove(obj, added):
            logging.debug("GUI: Add/Remove Obj %s (%s) [%d]", repr(obj), repr(added), thread.get_ident())
            try:
                if added:
                    # TODO: #18 - Clean-up this by auto creating wrapper on name...
                    if isinstance(obj, Ship):
                        logging.debug("GUI: Adding Ship #%d", obj.id)
                        objects[obj.id] = ShipGUI(obj, world)
                        logging.debug("GUI: Added Ship #%d", obj.id)
                    elif isinstance(obj, Nebula):
                        logging.debug("GUI: Adding Nebula #%d", obj.id)
                        bgobjects[obj.id] = NebulaGUI(obj, world)
                        logging.debug("GUI: Added Nebula #%d", obj.id)
                    elif isinstance(obj, Planet):
                        logging.debug("GUI: Adding Planet #%d", obj.id)
                        bgobjects[obj.id] = PlanetGUI(obj, world)
                        logging.debug("GUI: Added Planet #%d", obj.id)
                    elif isinstance(obj, WormHole):
                        logging.debug("GUI: Adding WormHole #%d", obj.id)
                        bgobjects[obj.id] = WormHoleGUI(obj, world)
                        logging.debug("GUI: Added WormHole #%d", obj.id)
                    elif isinstance(obj, Asteroid):
                        logging.debug("GUI: Adding Asteroid #%d", obj.id)
                        objects[obj.id] = AsteroidGUI(obj, world)
                        logging.debug("GUI: Added Asteroid #%d", obj.id)
                    elif isinstance(obj, Torpedo):
                        logging.debug("GUI: Adding Torpedo #%d", obj.id)
                        objects[obj.id] = TorpedoGUI(obj, world)
                        logging.debug("GUI: Added Torpedo #%d", obj.id)
                    elif isinstance(obj, SpaceMine):
                        logging.debug("GUI: Adding SpaceMine #%d", obj.id)
                        objects[obj.id] = SpaceMineGUI(obj, world)
                        logging.debug("GUI: Added SpaceMine #%d", obj.id)
                    else:
                        logging.debug("GUI: Adding %s #%d", repr(obj), obj.id)
                        objects[obj.id] = obj.WRAPPERCLASS(obj, world)
                        logging.debug("GUI: Added %s %d", repr(obj), obj.id)
                    #eif
                else:
                    if isinstance(obj, Ship):
                        logging.debug("GUI: Ship #%d Dying", obj.id)
                        ship = objects.get(obj.id, None)
                        if ship != None:
                            ship.dying = True
                            logging.debug("GUI: Ship #%d Set Dying", obj.id)
                    elif obj.id in objects:
                        logging.debug("GUI: Removing Object #%d", obj.id)
                        del objects[obj.id]
                        logging.debug("GUI: Removed Object #%d", obj.id)
                    elif obj.id in bgobjects:
                        logging.debug("GUI: Removing BG Object #%d", obj.id)
                        del bgobjects[obj.id]
                        logging.debug("GUI: Removed BG Object #%d", obj.id)
                    #eif
                #eif
            except:
                logging.error("GUI ERROR")
                logging.error(traceback.format_exc())
                print traceback.format_exc()
            #logging.debug("GUI: Add/Remove Done [%d]", thread.get_ident())
        #endregion

        logging.debug("Register World Listener...")
        world.registerObjectListener(addorremove)

        logging.debug("Add Objects to GUI...")
        # Create objects for all items in world
        for obj in world:
            addorremove(obj, True)
        #efor

        # Create Stars
        #stars = []
        #for i in xrange((world.width / STAR_DENSITY * world.height / STAR_DENSITY)):
        #    stars.append(Star((random.randint(4, world.width - 4), random.randint(4, world.height - 4))))

        logging.debug("Create Fonts...")
        # Start Main Loop
        font = pygame.font.Font("freesansbold.ttf", 12)
        bigfont = pygame.font.Font("freesansbold.ttf", 44)

        logging.debug("Load Textures...")
        spacetexture = Cache().getImage("Backgrounds/space")
        scalefactorx = float(world.size[0]) / resolution[0]
        scalefactory = float(world.size[1]) / resolution[1]
        offsetx = 0
        maxoffsetx = -world.width + resolution[0]
        offsety = 0
        maxoffsety = -world.height + resolution[1]

        def centerViewOnWorld(pos):
            return -pos[0] + resolution[0]/2, -pos[1] + resolution[1]/2
    
        #keyboard repeat rate
        pygame.key.set_repeat(75, 25)

        zoomout = True
        mouselock = True
        MOUSELOCK_RANGE = resolution[0] / 8
        logintercept = False
        mlh = MessageLogHandler(50)
    
        dynamiccamera = False

        mousemode = None
        prevzoom = zoomout
        showip = cfg.getboolean("Application", "showip")
        showplayerlist = cfg.getboolean("Application", "showstats")
        showroundtime = cfg.getboolean("Tournament", "tournament")
        tournamentinfo = cfg.getboolean("Tournament", "tournament")
    
        flags = {"DEBUG":False,
                 "STATS":cfg.getboolean("Application", "showstats"),
                 "NAMES":True,
                 "GAME":cfg.getboolean("Application", "showstats"),
                 "THREADS":False}
    
        logging.info("Create Main Surface...")
        #TODO: Optimize by only drawing objects in viewport...
        worldsurface = pygame.Surface((world.size[0], world.size[1]), flags=HWSURFACE)
    
        logging.debug("Game Start!")
        obj = None
    
        notexit = True

        # In test case we only care about test being done
        if testcase != None:
            notexit = False

        #endregion

        # Get spawnable items in alphabetical order
        SPAWN_TYPES = SpawnManager.ENTITY_TYPES.keys()
        SPAWN_TYPES.sort()

        while notexit or (testcase != None and not testcase.donetest):
            t = pygame.time.get_ticks() / 1000.0

            #for star in stars:
            #    star.draw(windowSurface)

            # TODO: figure out abstraction for pygame or method in order to get objwrapper to figure out if it needs
            # to draw in the screen or be no-op, ideally objwrapper just does what it does now...

            worldsurface.fill(colorBlack)
                
            #for x in xrange(offsetx, resolution[0], 512):
            #    for y in xrange(offsety, resolution[1], 512):
            #        worldsurface.blit(spacetexture, (x, y))

            # draw background items first in specific z-order
            for obj in sorted(bgobjects.values(), key=attrgetter('zorder')):
                obj.draw(worldsurface, flags)
                if obj.dead:
                    del bgobjects[obj._worldobj.id]
       
            # draw active objects
            for obj in objects:
                obj.draw(worldsurface, flags)
                if hasattr(obj._worldobj, "player") and obj._worldobj.player.sound != None:
                    #print "Trying to play sound", obj._worldobj.player.sound
                    SCache().play(obj._worldobj.player.sound)
                    obj._worldobj.player.sound = None
                if obj.dead:
                    del objects[obj._worldobj.id]
                            
            if flags["GAME"]:
                game.gui_draw_game_world_info(worldsurface, flags, trackplayer)

            #region Key/Mouse Event Handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    notexit = False
                elif (event.type == KEYDOWN and event.key == K_a) or (event.type == MOUSEBUTTONDOWN and event.button in (4, 5)):
                    if mousemode == None or not mousemode.startswith("Add"):
                        if event.type == KEYDOWN or event.button == 5:
                            mousemode = "Add" + SPAWN_TYPES[0]
                        else:
                            mousemode = "Add" + SPAWN_TYPES[-1]
                    elif event.type == KEYDOWN or event.button == 5:
                        x = SPAWN_TYPES.index(mousemode[3:])
                        if x < len(SPAWN_TYPES) - 1:
                            mousemode = "Add" + SPAWN_TYPES[x+1]
                        elif event.type == MOUSEBUTTONDOWN:
                            mousemode = "Add" + SPAWN_TYPES[0]
                        else:
                            mousemode = None
                    else:
                        x = SPAWN_TYPES.index(mousemode[3:])
                        if x > 0:
                            mousemode = "Add" + SPAWN_TYPES[x-1]
                        else:
                            mousemode = "Add" + SPAWN_TYPES[-1]
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))
                    elif event.key == K_SPACE and not game.round_get_has_started():
                        game.round_start()
                    elif event.key == K_d:
                        flags["DEBUG"] = not flags["DEBUG"]
                    elif event.key == K_i:
                        showip = not showip
                    elif event.key == K_p:
                        showplayerlist = (showplayerlist + 1) % (2 + game.tournament_is_running())
                    elif event.key == K_s:
                        flags["STATS"] = not flags["STATS"]
                    elif event.key == K_n:
                        flags["NAMES"] = not flags["NAMES"]
                    elif event.key == K_UP:
                        offsety += 16
                    elif event.key == K_DOWN:
                        offsety -= 16
                    elif event.key == K_RIGHT:
                        offsetx -= 16
                    elif event.key == K_LEFT:
                        offsetx += 16
                    elif event.key == K_g:
                        flags["GAME"] = not flags["GAME"]
                    elif event.key == K_h:
                        flags["THREADS"] = not flags["THREADS"]
                    elif event.key == K_t and game.tournament_is_running():
                        tournamentinfo = not tournamentinfo
                    elif event.key == K_z:
                        zoomout = not zoomout
                    elif event.key == K_m:
                        mouselock = not mouselock
                    elif event.key == K_PAGEUP and len(game.game_get_current_player_list()) > 0:
                        if trackplayer == None:
                            trackplayer = game.game_get_current_leader_list()[-1]
                        else:
                            lst = game.game_get_current_leader_list()
                            for x in xrange(len(lst) - 1, -1, -1):
                                if lst[x] == trackplayer:
                                    if x == 0:
                                        x = len(lst)
                                    trackplayer = lst[x-1]
                                    break
                    elif event.key == K_PAGEDOWN and len(game.game_get_current_player_list()) > 0:
                        if trackplayer == None: 
                            trackplayer = game.game_get_current_leader_list()[0]
                        else:
                            lst = game.game_get_current_leader_list()
                            for x in xrange(len(lst)):
                                if lst[x] == trackplayer:
                                    if x == len(lst) - 1:
                                        x = -1
                                    trackplayer = lst[x+1]
                                    break
                    elif event.key == K_END:
                        trackplayer = None
                        mlh.filter = None
                    elif event.key == K_y:
                        dynamiccamera = not dynamiccamera
                        if not dynamiccamera:
                            trackplayer = None
                    elif event.key == K_l:
                        logintercept = not logintercept
                        logger = logging.getLogger()
                        if logintercept:                        
                            logger.addHandler(mlh)
                        else:
                            logger.removeHandler(mlh)
                            mlh.messages.clear()
                    elif event.key == K_k:
                        if mousemode == "Destroy":
                            mousemode = None
                        else:
                            mousemode = "Destroy"
                    elif event.key == K_e:
                        if mousemode == "Explode":
                            mousemode = None
                        else:
                            mousemode = "Explode"                    
                    elif event.key == K_v:
                        if mousemode == "Move":
                            mousemode = None
                            zoomout = prevzoom
                        else:
                            mousemode = "Move"
                            prevzoom = zoomout
                            zoomout = True
                    elif event.key == K_r:
                        showroundtime = not showroundtime
                elif event.type == MOUSEBUTTONDOWN and event.button in (1, 2): #Left or Middle Click
                    if zoomout:
                        x = event.pos[0]*scalefactorx
                        y = event.pos[1]*scalefactory
                    else:
                        x, y = event.pos[0]-offsetx, event.pos[1]-offsety
                    #print zoomout, x, y

                    if mousemode == "Move" and trackplayer != None:
                        if event.button != 2:
                            mousemode = None
                        zoomout = prevzoom
                        obj = trackplayer.object
                        if obj != None:
                            obj.body.position = (x, y)
                    elif mousemode == "Destroy":
                        if event.button != 2:
                            mousemode = None
                        v = Vec2d(x, y)
                        for lst in objects, bgobjects:
                            for obj in lst:
                                if math.sqrt(obj._worldobj.body.position.get_dist_sqrd(v)) <= 32:
                                    logging.info("[GUI] Destroying Object #%d", obj._worldobj.id)
                                    if isinstance(obj, ShipGUI):
                                        obj._worldobj.killed = True
                                    world.remove(obj._worldobj)
                                    break
                    elif mousemode == "Explode":
                        if event.button != 2:
                            mousemode = None
                        world.causeExplosion((x, y), 256, 1000)
                    elif mousemode != None and  mousemode.startswith("Add"):
                        game.spawnmanager.spawn_entity(mousemode[3:], (x, y), False)
                        if event.button != 2:
                            mousemode = None
                    elif zoomout and event.button == 1:
                        # zoom in
                        zoomout = False
                        #xoffset = -(((event.pos[0] - resolution[0]/2) % 16)*16 * scalefactorx)
                        #yoffset = -(((event.pos[1] - resolution[1]/2) % 16)*16 * scalefactory)
                        offsetx, offsety = centerViewOnWorld((event.pos[0]*scalefactorx, event.pos[1]*scalefactory))
                    else:
                        # recenter on new click
                        offsetx, offsety = centerViewOnWorld((event.pos[0]*scalefactorx, event.pos[1]*scalefactory))
                elif event.type == MOUSEBUTTONDOWN and event.button == 3: #Right Click
                    mousemode = None
            #endregion 

            # Tracks a ship on screen
            if len(game.game_get_current_player_list()) == 0 or trackplayer not in game.game_get_current_leader_list():
                trackplayer = None
        
            if dynamiccamera and len(game.game_get_current_leader_list()) > 0:
                trackplayer = game.game_get_current_leader_list()[0]
            
        
            if trackplayer != None:
                obj = trackplayer.object
                if obj != None:
                    mlh.filter = "#" + repr(obj.id)
                    offsetx, offsety = centerViewOnWorld(obj.body.position)

            # Pans world with mouse
            if not mouselock:
                # TODO Edge Detect
                pos = pygame.mouse.get_pos()
                if pos[0] < MOUSELOCK_RANGE:
                    offsetx += 48
                elif pos[0] > resolution[0] - MOUSELOCK_RANGE:
                    offsetx -= 48

                if pos[1] < MOUSELOCK_RANGE:
                    offsety += 48
                elif pos[1] > resolution[1] - MOUSELOCK_RANGE:
                    offsety -= 48
            #eif        

            if offsetx > 0: offsetx = 0
            if offsety > 0: offsety = 0
            if offsetx < maxoffsetx: offsetx = maxoffsetx
            if offsety < maxoffsety: offsety = maxoffsety

            if zoomout:
                pygame.transform.scale(worldsurface, resolution, windowSurface)
            else:
                windowSurface.blit(worldsurface, (offsetx, offsety)) 

            if showip:
                ip = bigfont.render(ipaddress, False, (255, 255, 255))
                windowSurface.blit(ip, (resolution[0]/2-ip.get_width()/2,0))

            if not game.round_get_has_started():
                ip = bigfont.render("Waiting For Start - Press Space", False, (255, 255, 255))
                windowSurface.blit(ip, (resolution[0]/2-ip.get_width()/2,resolution[1]/2-ip.get_height()/2))
            
                if game.laststats != None:
                    x = 0
                    for i in game.laststats:
                        windowSurface.blit(font.render(i, False, (192, 192, 255)), (resolution[0]/2-300, resolution[1]/2 + 64 + 12*x))
                        x += 1
            
            if showplayerlist > 0:
                x = 0
                for i in game.gui_get_player_stats(all=(showplayerlist == 1)):
                    c = (192, 192, 192)
                    if trackplayer != None and trackplayer.name in i:
                        c = trackplayer.color
                    windowSurface.blit(font.render(i, False, c), (resolution[0]-300, 64 + 12*x))
                    x += 1
                if showplayerlist == 1:
                    windowSurface.blit(font.render(repr(x) + " Players Connected", False, (192, 192, 192)), (resolution[0]-300, 64 + 12 * x))
                else:
                    windowSurface.blit(font.render(repr(x) + " Players In Round", False, (192, 192, 192)), (resolution[0]-300, 64 + 12 * x))

            if showroundtime and testcase == None:
                ip = bigfont.render(str(datetime.timedelta(seconds=game.round_get_time_remaining())), False, (255, 255, 255))
                windowSurface.blit(ip, (resolution[0]/2-ip.get_width()/2,32))
            elif testcase != None:
                if testcase.flashcolor == False:
                    testcase.flashcolor = (255, 255, 255)
                ip = bigfont.render(str(datetime.timedelta(milliseconds=pygame.time.get_ticks())), False, testcase.flashcolor)
                windowSurface.blit(ip, (32,32))

                testcase.flashcolor = False
            
            if flags["DEBUG"]:
                mpos = pygame.mouse.get_pos()
                if zoomout: # TODO: Need to refactor and centralize these calculations as part of 'Camera' system
                    x = mpos[0]*scalefactorx
                    y = mpos[1]*scalefactory
                else:
                    x, y = mpos[0]-offsetx, mpos[1]-offsety

                windowSurface.blit(font.render("DEBUG MODE", False, (255, 255, 255)), (resolution[0]/2-38,32))
                windowSurface.blit(font.render("FPS: " + repr(fpsClock.get_fps()), False, (255, 255, 255)), (0,0))
                windowSurface.blit(font.render("T: " + repr(len(threading.enumerate())), False, (192, 192, 192)), (0, 12))
                windowSurface.blit(font.render("World Offset: " + repr((-offsetx, -offsety)), False, (255, 255, 255)), (0,24))
                windowSurface.blit(font.render("World Size: " + repr(world.size) + " - " + repr((int(x), int(y))), False, (255, 255, 255)), (0,36))
                windowSurface.blit(font.render("World Objects: " + repr(len(world)), False, (255, 255, 255)), (0,48))            
            
                if mouselock:
                    windowSurface.blit(font.render("MOUSELOCK: ON", False, (255, 255, 255)), (resolution[0]-114,0))
                else:
                    windowSurface.blit(font.render("MOUSELOCK: OFF", False, (255, 255, 255)), (resolution[0]-114,0))
                if "-" in windowcaption:
                    text = font.render(windowcaption.split("-")[1], False, (192, 192, 192))
                    windowSurface.blit(text, (resolution[0]-text.get_width()-2, 12))
                    text = font.render(windowcaption.split("-")[0][18:-1], False, (192, 192, 192))
                    windowSurface.blit(text, (resolution[0]-text.get_width()-2, 24))
                else:
                    text = font.render(windowcaption[18:], False, (192, 192, 192))
                    windowSurface.blit(text, (resolution[0]-text.get_width()-2, 24))

                windowSurface.blit(font.render(repr(flags), False, (255, 255, 255)), (0, resolution[1]-12))            

                if logintercept:
                    for i in xrange(len(mlh.messages)):
                        if i >= len(mlh.messages): break
                        c = 145 + i*2
                        windowSurface.blit(font.render(mlh.messages[i], False, (c, c, c)), (10, 64 + 12*i))

                if trackplayer == None:
                    windowSurface.blit(font.render("Tracking Off", False, (255, 255, 255)), (resolution[0]/2-36,resolution[1]-12))

            if trackplayer != None:
                to = trackplayer.object
                if to != None and objects.has_key(to.id):
                    # if we're tracking a ship, let's print some useful info about it.
                    #windowSurface.blit(font.render(trackplayer.name, False, trackplayer.color), (resolution[0] - 200, resolution[1] - 120))
                    windowSurface.fill((128, 128, 128), Rect(resolution[0] - 310, resolution[1] - 120, 300, 110), pygame.BLEND_ADD)
                    pygame.draw.rect(windowSurface, (192, 192, 192, 128), Rect(resolution[0] - 310, resolution[1] - 120, 300, 110), 1)
                    objects[to.id].draw(windowSurface, 
                                                        {"DEBUG":False,
                                                            "STATS":False,
                                                            "NAMES":True,
                                                            "GAME":False}, Vec2d(resolution[0] - 250, resolution[1] - 64))
                    windowSurface.blit(font.render("%d" % to.body.velocity.length, False, (255, 255, 255)), (resolution[0] - 298, resolution[1] - 86))

                    netenergy = 4
                    x = 0
                    for cmd in to.commandQueue:
                        netenergy -= cmd.energycost
                        windowSurface.blit(font.render("%.1f (%s" % (cmd.energycost, repr(cmd)[14:]), False, trackplayer.color), (resolution[0] - 300, resolution[1] - 28 - x * 12))
                        x += 1
                    x = "+"
                    if netenergy < 0:
                        x = "-"
                    #windowSurface.blit(infofont().render("Energy %d  %s%.1f" % (to.energy.value, x, netenergy), False, trackplayer.color), (resolution[0] - 190, resolution[1] - 110))

                    # Energy Bar
                    windowSurface.fill((0, 64, 0), Rect(resolution[0] - 190, resolution[1] - 114, 170, 18))
                    windowSurface.blit(pygame.transform.scale(Cache().getImage("HUD/Energy"), (166, 14)), (resolution[0] - 188, resolution[1] - 112), pygame.Rect(0, 0, 166 * to.energy.percent, 14))
                    windowSurface.blit(infofont().render("%d %s%.1f" % (to.energy.value, x, netenergy), False, (255, 255, 255)), (resolution[0] - 180, resolution[1] - 112))

                    # Shield Bar
                    windowSurface.fill((0, 0, 96), Rect(resolution[0] - 190, resolution[1] - 94, 170, 8))
                    windowSurface.blit(pygame.transform.scale(Cache().getImage("HUD/Shield"), (166, 14)), (resolution[0] - 188, resolution[1] - 93), pygame.Rect(0, 0, 166 * to.shield.percent, 6))
                    windowSurface.blit(font.render(repr(int(100 * to.shield.percent)), False, (255, 255, 255)), (resolution[0] - 178, resolution[1] - 95))

                    # Health Bar
                    windowSurface.fill((64, 0, 0), Rect(resolution[0] - 190, resolution[1] - 84, 170, 16))
                    windowSurface.blit(pygame.transform.scale(Cache().getImage("HUD/Health"), (166, 14)), (resolution[0] - 188, resolution[1] - 82), pygame.Rect(0, 0, 166 * to.health.percent, 12))
                    windowSurface.blit(infofont().render(repr(int(100 * to.health.percent)), False, (255, 255, 255)), (resolution[0] - 180, resolution[1] - 83))

                    if trackplayer.lastkilledby != None:
                        windowSurface.blit(font.render("LD: " + trackplayer.lastkilledby, False, (255, 255, 255)), (resolution[0] - 298, resolution[1] - 118))

            if flags["GAME"]:
                game.gui_draw_game_screen_info(windowSurface, flags, trackplayer)

            if tournamentinfo:
                game.gui_draw_tournament_bracket(windowSurface, flags, trackplayer)

            if trackplayer != None:
                n = font.render("Tracking: " + trackplayer.name, False, trackplayer.color)
                windowSurface.blit(n, (resolution[0]/2-n.get_width()/2,resolution[1]-12))                          

            if mousemode == "Destroy":
                ip = bigfont.render("DESTROY OBJECT BY CLICK", False, (255, 0, 0))
                windowSurface.blit(ip, (resolution[0]/2-ip.get_width()/2, resolution[1]/2-ip.get_height()/2))
            elif mousemode == "Explode":
                ip = bigfont.render("CLICK TO CAUSE EXPLOSION FORCE", False, (255, 0, 0))
                windowSurface.blit(ip, (resolution[0]/2-ip.get_width()/2, resolution[1]/2-ip.get_height()/2))
            elif mousemode != None and mousemode[:3] == "Add":
                x = SPAWN_TYPES.index(mousemode[3:])
                for i in xrange(x - 1, -1, -1):
                    c = max(0, 128 + (i - x) * 16)
                    ip = bigfont.render(SPAWN_TYPES[i], False, (c, c, c))
                    windowSurface.blit(ip, (resolution[0]/2 + 35, resolution[1]/2-24-((i - x) * -36)))

                ip = bigfont.render("Click to Add " + mousemode[3:], False, (255, 255, 0))
                windowSurface.blit(ip, (resolution[0]/2-240, resolution[1]/2-ip.get_height()/2))

                for i in xrange(x + 1, len(SPAWN_TYPES)):
                    c = max(0, 128 - (i - x - 1) * 16)
                    ip = bigfont.render(SPAWN_TYPES[i], False, (c, c, c))
                    windowSurface.blit(ip, (resolution[0]/2 + 35, resolution[1]/2+18+((i - x - 1) * 36)))

            if mousemode == "Move" and trackplayer == None:
                ip = bigfont.render("TRACK OBJECT BEFORE MOVING", False, (255, 255, 255))
                windowSurface.blit(ip, (resolution[0]/2-ip.get_width()/2, resolution[1]/2-ip.get_height()/2))
            elif mousemode == "Move":
                ip = bigfont.render("CLICK TO MOVE "+trackplayer.name, False, (255, 255, 255))
                windowSurface.blit(ip, (resolution[0]/2-ip.get_width()/2, resolution[1]/2-ip.get_height()/2))        

            if flags["THREADS"]:
                mt = 0
                st = 6
                rt = 6
                thrs = threading.enumerate()
                thrs.sort(key=lambda x: x.name, reverse=True)
                for thr in thrs:
                    s = repr(thr)
                    c = (192, 192, 192)
                    ind = 30
                    if "Receiving" in s:
                        i = rt
                        rt += 1
                        c = (192, 192, 255)
                        ind = resolution[0]/2 + 30
                    elif "Sending" in s:
                        i = st
                        st += 1
                    else:
                        i = mt
                        mt += 1
                        c = (255, 192, 192)

                    windowSurface.blit(font.render(repr(thr), False, c), (ind, 64 + 12*i))

            pygame.display.update()
            fpsClock.tick(30) # keep in sync with physics engine?

        #TODO: Add Logging???

        # close out a game 
        game.end()

        logging.info("Closing Pygame...")
        print "Closing Pygame"
        pygame.quit()
    except:
        print "EXCEPTION IN GUI"
        logging.exception("FATAL Error in GUI!!!")
        logging.error(traceback.format_exc())
        print traceback.format_exc()
        world.gameerror = True # Flag for Unit Tests

    logging.info("GUI Closed")