"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2015 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

import Server.MWNL2, logging, random, time, traceback
from World.WorldEntities import Ship
from World.WorldCommands import ConvertNetworkMessageToCommand, RadarCommand
from NetworkCommands import *

class WorldServer(object):
    """description of class"""

    # TODO take configuration for port, max images
    def __init__(self, port, game):
        print "Server Started at IP: " + Server.MWNL2.getIPAddress()
        self.__port = port
        self.__maximages = game.cfg.getint("Server", "maximages")
        self.__net = Server.MWNL2.MWNL_Init(port, self.__serverCallback)
        self.__net.host(game.cfg.getboolean("Server", "multipleconnections"))
        self.__game = game
        if game.cfg.has_option("Server", "disablecommands"):
            self.__badcmds = game.cfg.get("Server", "disablecommands").split(",")
        else:
            self.__badcmds = None
        #eif
        game.server = self        
        logging.info("Started Server (%s), Waiting for Clients", Server.MWNL2.getIPAddress())    
        
    def sendErrorMessage(self, shipcmd, errmsg, sender):
        logging.error("ERRMSG: " + repr(shipcmd) + errmsg)
        if len(shipcmd) > 1:
            self.__net.send(MWNL_CMD_ERROR, {"COMMAND":shipcmd[0],"PARAMETERS":shipcmd[1],"MESSAGE":errmsg}, sender)
        else:
            self.__net.send(MWNL_CMD_ERROR, {"COMMAND":shipcmd[0],"PARAMETERS":{},"MESSAGE":errmsg}, sender)
        #eif
    #e sendErrorMessage

    def sendEnvironment(self, ship, netid):
        self.__net.send(MWNL_CMD_ENVIRONMENT, self.__game.world.getEnvironment(ship), netid)

    def sendDisconnect(self, netid):        
        # disconnect client...
        self.__net.send(Server.MWNL2.MWNL_CMD_DISCONNECT, sendto=netid)
        # make sure it's closed?
        self.__net.close(netid)
        
    # Called when Main Ends to clean-up threads
    def disconnectAll(self):
        self.__net.close()

    def __serverCallback(self, sender, cmd):
        try:
            #logging.debug("Got Info from " + repr(sender) + " " + repr(cmd))        
            if cmd[0] == Server.MWNL2.MWNL_CMD_CLIENT_CONNECTED:
                p = {"IMAGELENGTH": self.__maximages, "WORLDWIDTH": self.__game.world.width, "WORLDHEIGHT": self.__game.world.height}
                p.update(self.__game.getInitialInfoParameters())
                self.__net.send(MWNL_CMD_REQUEST, p, sender)
            elif cmd[0] == Server.MWNL2.MWNL_CMD_DISCONNECT:
                self.__game.playerDisconnected(sender)
            elif cmd[0] == MWNL_CMD_REGISTER:
                data = cmd[1]
                if isinstance(data["NAME"], unicode):
                    teamname = data["NAME"][:20]
                else:
                    teamname = "NOT A STRING " + str(random.randint(0, 999999))
                #eif

                if len(teamname.strip()) <= 0:
                    teamname = "BLANK STRING " + str(random.randint(0, 999999))
                #eif
                
                if self.__game.hasPlayer(teamname):
                    self.sendErrorMessage(cmd, "Player already playing game.", sender)
                else:
                    c = []
                    if isinstance(data["COLOR"], list) and len(data["COLOR"]) == 3 and map(type, data["COLOR"]) == [int] * 3:
                        isgreater128 = False                        
                        for i in data["COLOR"]:
                            if i < 0:
                                c.append(0)
                            elif i > 255:
                                isgreater128 = True
                                c.append(255)
                            else:
                                if i >= 128:
                                    isgreater128 = True
                                c.append(i)
                            #eif
                        if not isgreater128:
                            c = [255, 255, 255]                        
                    else:
                        c = (random.randint(128, 255),random.randint(128, 255),random.randint(128, 255))
                    #eif

                    ii = 0
                    if isinstance(data["IMAGEINDEX"], int) and data["IMAGEINDEX"] >= 0 and data["IMAGEINDEX"] < self.__maximages:
                        ii = data["IMAGEINDEX"]
                    #eif

                    logging.debug("Trying to Register Player: " + teamname + " with color " + repr(c) + " and image " + repr(ii))
                    
                    if not self.__game.registerPlayer(teamname, c, ii, sender):
                        self.sendErrorMessage(cmd, "Game already started or does not allow reentry.", sender)
                #eif
            elif cmd[0] == MWNL_CMD_SHIPCMD:
                # TODO: Deal with case where we get a command after a disconnect???
                ship = self.__game.getPlayerByNetId(sender).object
                self.__game.getPlayerByNetId(sender).waiting = False
                # TODO: propogate this down below more too?
                if ship == None: 
                    return
            
                scmd = None
                if len(cmd[1]) == 2:
                    scmd = ConvertNetworkMessageToCommand(ship, cmd[1][0], cmd[1][1])
                elif len(cmd[1]) == 1:
                    scmd = ConvertNetworkMessageToCommand(ship, cmd[1][0], {})

                if scmd == None or isinstance(scmd, str):
                    logging.error("Bad Command #%d: %s", ship.id, repr(scmd))
                    self.sendErrorMessage(cmd[1], "Invalid Ship Command: " + repr(scmd), sender)
                    scmd = None
                elif self.__badcmds != None and scmd.__class__.__name__ in self.__badcmds:
                    self.sendErrorMessage(cmd[1], "Ship Command Has Been Disabled: " + repr(scmd), sender)
                    scmd = None
                else:
                    logging.info("Processing Ship #%d Command %s", ship.id, repr(scmd))
                    logging.info("Ship Queue Before #%d %s", ship.id, repr(ship.commandQueue))
                    if ship.commandQueue.isBlockingCommandOnTop():
                        logging.error("CHEAT: %d, %s", ship.id, repr(ship.commandQueue))
                        print "CHEAT ", ship.id                        
                        self.sendErrorMessage(cmd[1], "CHEAT: Can't Place Command When Blocked" + repr(scmd), sender)
                        scmd = None
                    else:
                        #logging.error("%s", repr(ship.commandQueue))                       
                        ship.commandQueue.append(scmd)
                        #ship.commandQueue.update(0)

                        logging.info("Ship Queue After #%d %s", ship.id, repr(ship.commandQueue))

                        # block server response on a blocking command...
                        #if scmd.blocking
                        #   while not (scmd.isExpired() or scmd.isComplete()):
                        #TODO Releasing Here?
                        while ship.commandQueue.isBlockingCommandOnTop():
                            time.sleep(0.02) #TODO: Centralize step

                        #logging.error("%s", repr(ship.commandQueue))                            
                        logging.info("Releasing #%d From Server Command: %s", ship.id, repr(scmd))
                    #eif
                #eif

                radar = 0
                target = -1
                if isinstance(scmd, RadarCommand):
                    radar = scmd.level
                    target = scmd.target
                #eif

                #print "Command: " + repr(cmd[1])

                if not ship.destroyed:
                    logging.info("Send Environment to #%d (net %d)", ship.id, sender)
                    self.__game.getPlayerByNetId(sender).waiting = True
                    self.__net.send(MWNL_CMD_ENVIRONMENT, self.__game.world.getEnvironment(ship, radar, target), sender)
                else:
                    logging.debug("Ship #%d Destroyed, won't send environment", ship.id)
                #eif
            #eif
        except:
            logging.error(traceback.format_exc())
            print traceback.format_exc()
    #e__serverCallback
#eclass
