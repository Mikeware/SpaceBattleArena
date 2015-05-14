"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2015 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

import pygame, sys, random, logging, math, datetime
from collections import deque
from pygame.locals import *
from operator import attrgetter

from World.WorldMap import GameWorld

from ObjWrappers.ShipWrapper import ShipGUI
from ObjWrappers.NebulaWrapper import NebulaGUI
from ObjWrappers.PlanetWrapper import PlanetGUI
from ObjWrappers.AsteroidWrapper import AsteroidGUI
from ObjWrappers.WeaponWrappers import TorpedoGUI
from Game.KingOfTheBubble import Bubble, KingOfTheBubbleGame
from GraphicsCache import Cache
from World.WorldEntities import Ship, Planet, Asteroid, Torpedo, BlackHole, Nebula
from Server.MWNL2 import getIPAddress
from pymunk import Vec2d
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

def startGame(windowcaption, game, fullscreen=True, resolution=None, showstats=False, sound=False, testcase=None):    
    #region Initialization
    logging.info("Initiating PyGame...")

    world = game.world
    pygame.init()
    fpsClock = pygame.time.Clock()

    logging.debug("Initiating Screen...")

    if sound:
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
    shipids = []
    trackshipid = None
    def addorremove(obj, added):
        logging.debug("GUI: Add/Remove Obj %s (%s) [%d]", repr(obj), repr(added), thread.get_ident())
        try:
            if added:
                # TODO: #18 - Clean-up this by auto creating wrapper on name...
                if isinstance(obj, Ship):
                    logging.debug("GUI: Adding Ship #%d", obj.id)
                    objects[obj.id] = ShipGUI(obj, world)
                    shipids.append(obj.id)
                    logging.debug("GUI: Added Ship #%d", obj.id)
                elif isinstance(obj, Nebula):
                    logging.debug("GUI: Adding Nebula #%d", obj.id)
                    bgobjects[obj.id] = NebulaGUI(obj, world)
                    logging.debug("GUI: Added Nebula #%d", obj.id)
                elif isinstance(obj, Planet):
                    logging.debug("GUI: Adding Planet #%d", obj.id)
                    bgobjects[obj.id] = PlanetGUI(obj, world)
                    logging.debug("GUI: Added Planet #%d", obj.id)
                elif isinstance(obj, Asteroid):
                    logging.debug("GUI: Adding Asteroid #%d", obj.id)
                    objects[obj.id] = AsteroidGUI(obj, world)
                    logging.debug("GUI: Added Asteroid #%d", obj.id)
                elif isinstance(obj, Torpedo):
                    logging.debug("GUI: Adding Torpedo #%d", obj.id)
                    objects[obj.id] = TorpedoGUI(obj, world)
                    logging.debug("GUI: Added Torpedo #%d", obj.id)
                else:
                    logging.debug("GUI: Adding %s #%d", repr(obj), obj.id)
                    objects[obj.id] = obj.WRAPPERCLASS(obj, world)
                    logging.debug("GUI: Added %s %%d", repr(obj), obj.id)
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
    showip = showstats
    showplayerlist = showstats
    showroundtime = game.cfg.getboolean("Tournament", "tournament")
    tournamentinfo = game.cfg.getboolean("Tournament", "tournament")
    
    flags = {"DEBUG":False,
             "STATS":showstats,
             "NAMES":True,
             "GAME":showstats}
    
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
                if isinstance(obj, ShipGUI):
                    shipids.remove(obj._worldobj.id)
                            
        if flags["GAME"]:
            game.gui_draw_game_world_info(worldsurface, flags)

        #region Key/Mouse Event Handling
        for event in pygame.event.get():
            if event.type == QUIT:
                notexit = False
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
                elif event.key == K_t and game.tournament_is_running():
                    tournamentinfo = not tournamentinfo
                elif event.key == K_z:
                    zoomout = not zoomout
                elif event.key == K_m:
                    mouselock = not mouselock
                elif event.key == K_PAGEUP and len(shipids) > 0:
                    if trackshipid == None: 
                        trackshipid = shipids[0]
                    else:
                        trackshipid = shipids[shipids.index(trackshipid) - 1]
                elif event.key == K_PAGEDOWN and len(shipids) > 0:
                    if trackshipid == None: 
                        trackshipid = shipids[-1]
                    else:
                        trackshipid = shipids[(shipids.index(trackshipid) + 1) % len(shipids)]
                elif event.key == K_END:
                    trackshipid = None
                    mlh.filter = None
                elif event.key == K_y:
                    dynamiccamera = not dynamiccamera
                    if not dynamiccamera:
                        trackshipid = None
                elif event.key == K_l:
                    logintercept = not logintercept
                    logger = logging.getLogger()
                    if logintercept:                        
                        logger.addHandler(mlh)
                    else:
                        logger.removeHandler(mlh)
                        mlh.messages.clear()
                elif event.key == K_a:
                    if mousemode not in ("AddAsteroid", "AddPlanet", "AddBlackHole", "AddNebula", "AddBubble"):
                        mousemode = "AddAsteroid"
                    elif mousemode == "AddAsteroid":
                        mousemode = "AddPlanet"
                    elif mousemode == "AddPlanet":
                        mousemode = "AddBlackHole"
                    elif mousemode == "AddBlackHole":
                        mousemode = "AddNebula"
                    elif mousemode == "AddNebula" and isinstance(game, KingOfTheBubbleGame):
                        mousemode = "AddBubble"
                    else:
                        mousemode = None
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
            elif event.type == MOUSEBUTTONDOWN:                
                if zoomout:
                    x = event.pos[0]*scalefactorx
                    y = event.pos[1]*scalefactory
                else:
                    x, y = event.pos[0]-offsetx, event.pos[1]-offsety
                #print zoomout, x, y

                if mousemode == "Move" and trackshipid != None:
                    mousemode = None
                    zoomout = prevzoom
                    objects[trackshipid]._worldobj.body.position = (x, y)
                elif mousemode == "Destroy":
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
                    mousemode = None                
                    world.causeExplosion((x, y), 256, 1000)
                elif mousemode == "AddAsteroid":
                    mousemode = None
                    world.append(Asteroid((x, y)))
                elif mousemode == "AddPlanet":
                    mousemode = None
                    world.append(Planet((x, y)))
                elif mousemode == "AddBlackHole":
                    mousemode = None
                    world.append(BlackHole((x, y)))
                elif mousemode == "AddNebula":
                    mousemode = None
                    world.append(Nebula((x, y), (512, 128)))
                elif mousemode == "AddBubble":
                    mousemode = None
                    game.addBubbles(world, 1, pos=(x, y))
                elif zoomout and event.button == 1:
                    # zoom in
                    zoomout = False
                    #xoffset = -(((event.pos[0] - resolution[0]/2) % 16)*16 * scalefactorx)
                    #yoffset = -(((event.pos[1] - resolution[1]/2) % 16)*16 * scalefactory)
                    offsetx, offsety = centerViewOnWorld((event.pos[0]*scalefactorx, event.pos[1]*scalefactory))
                else:
                    # recenter on new click
                    offsetx, offsety = centerViewOnWorld((event.pos[0]*scalefactorx, event.pos[1]*scalefactory))
                    
        #endregion 

        # Tracks a ship on screen
        if len(shipids) == 0 or trackshipid not in objects: 
            trackshipid = None
        
        if dynamiccamera:
            trackshipid = game.game_get_current_leader_list()[0].id
            
        if trackshipid != None:
            mlh.filter = "#" + repr(trackshipid)
            offsetx, offsety = centerViewOnWorld(objects[trackshipid]._worldobj.body.position)

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

        if flags["DEBUG"] or showip:
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
                windowSurface.blit(font.render(i, False, (192, 192, 192)), (resolution[0]-300, 64 + 12*x))
                x += 1
            if showplayerlist == 1:
                windowSurface.blit(font.render(repr(x) + " Players Connected", False, (192, 192, 192)), (resolution[0]-300, 64 + 12 * x))
            else:
                windowSurface.blit(font.render(repr(x) + " Players In Round", False, (192, 192, 192)), (resolution[0]-300, 64 + 12 * x))

        if showroundtime:
            ip = bigfont.render(str(datetime.timedelta(seconds=game.round_get_time_remaining())), False, (255, 255, 255))
            windowSurface.blit(ip, (resolution[0]/2-ip.get_width()/2,32))
            
        if flags["DEBUG"]:
            mpos = pygame.mouse.get_pos()
            if zoomout: # TODO: Need to refactor and centralize these calculations as part of 'Camera' system
                x = mpos[0]*scalefactorx
                y = mpos[1]*scalefactory
            else:
                x, y = mpos[0]-offsetx, mpos[1]-offsety

            windowSurface.blit(font.render("DEBUG MODE", False, (255, 255, 255)), (resolution[0]/2-38,32))
            windowSurface.blit(font.render("FPS: " + repr(fpsClock.get_fps()), False, (255, 255, 255)), (0,0))            
            windowSurface.blit(font.render("World Offset: " + repr((-offsetx, -offsety)), False, (255, 255, 255)), (0,24))
            windowSurface.blit(font.render("World Size: " + repr(world.size) + " - " + repr((int(x), int(y))), False, (255, 255, 255)), (0,36))
            windowSurface.blit(font.render("World Objects: " + repr(len(world)), False, (255, 255, 255)), (0,48))
            
            if mouselock:
                windowSurface.blit(font.render("MOUSELOCK: ON", False, (255, 255, 255)), (resolution[0]-104,0))
            else:
                windowSurface.blit(font.render("MOUSELOCK: OFF", False, (255, 255, 255)), (resolution[0]-104,0))
            windowSurface.blit(font.render(repr(flags), False, (255, 255, 255)), (0, resolution[1]-12))            

            if logintercept:
                for i in xrange(len(mlh.messages)):
                    if i >= len(mlh.messages): break
                    c = 145 + i*2
                    windowSurface.blit(font.render(mlh.messages[i], False, (c, c, c)), (10, 64 + 12*i))

            if trackshipid == None:
                windowSurface.blit(font.render("Tracking Off", False, (255, 255, 255)), (resolution[0]/2-36,resolution[1]-12))

        if flags["GAME"]:
            game.gui_draw_game_screen_info(windowSurface, flags)

        if tournamentinfo:
            game.gui_draw_tournament_bracket(windowSurface, flags)

        if trackshipid != None:
            n = font.render("Tracking: " + objects[trackshipid]._worldobj.player.name, False, objects[trackshipid]._worldobj.player.color)
            windowSurface.blit(n, (resolution[0]/2-n.get_width()/2,resolution[1]-12))                          

        if mousemode == "Destroy":
            ip = bigfont.render("DESTROY OBJECT BY CLICK", False, (255, 0, 0))
            windowSurface.blit(ip, (resolution[0]/2-ip.get_width()/2, resolution[1]/2-ip.get_height()/2))
        elif mousemode == "Explode":
            ip = bigfont.render("CLICK TO CAUSE EXPLOSION FORCE", False, (255, 0, 0))
            windowSurface.blit(ip, (resolution[0]/2-ip.get_width()/2, resolution[1]/2-ip.get_height()/2))
        elif mousemode != None and mousemode[:3] == "Add":
            ip = bigfont.render("Click to Add " + mousemode[3:], False, (255, 255, 0))
            windowSurface.blit(ip, (resolution[0]/2-ip.get_width()/2, resolution[1]/2-ip.get_height()/2))        

        if mousemode == "Move" and trackshipid == None:
            ip = bigfont.render("TRACK OBJECT BEFORE MOVING", False, (255, 255, 255))
            windowSurface.blit(ip, (resolution[0]/2-ip.get_width()/2, resolution[1]/2-ip.get_height()/2))
        elif mousemode == "Move":
            ip = bigfont.render("CLICK TO MOVE "+objects[trackshipid]._worldobj.player.name, False, (255, 255, 255))
            windowSurface.blit(ip, (resolution[0]/2-ip.get_width()/2, resolution[1]/2-ip.get_height()/2))        

        pygame.display.update()
        fpsClock.tick(30) # keep in sync with physics engine?

    #TODO: Add Logging???

    # close out a game 
    logging.info("Ending Game")
    game._tournament = True # force it to not restart timers again
    game.round_over()

    logging.info("Ending World")
    print "Ending World"
    game.world.endGameLoop()
    logging.info("Closing Pygame...")
    print "Closing Pygame"
    pygame.quit()
