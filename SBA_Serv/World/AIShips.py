
from World.Messaging import Command
from WorldCommands import *
from WorldEntities import Ship
from Game.Players import Player

from Server import MWNL2
import time
from Server.WorldServer import MWNL_CMD_REGISTER, MWNL_CMD_REQUEST, MWNL_CMD_ENVIRONMENT, MWNL_CMD_SHIPCMD, MWNL_CMD_ERROR

class AIShip(Ship):
    NetIDs = -3 # ID Should be -3 or less, auto-assign (unused by network engine)

    def __init__(self, name, pos, game, callback, color=(64, 64, 64), image=8):
        super(AIShip, self).__init__(pos, game.world)
        game.server_register_player("* "+name+str(AIShip.NetIDs)+" *", color, image, AIShip.NetIDs, self)
        AIShip.NetIDs -= 1
        self._name = name
        self.rotationAngle = 0
        self._callback = callback

    def ship_added(self):
        """
        Called by game when ship added to world (important for tournaments)
        """
        pass

    def update(self, t):
        super(AIShip, self).update(t)

        if not self.commandQueue.isBlockingCommandOnTop():
            self._callback()


class AIShip_SetList(AIShip):
    def __init__(self, name, pos, world, cmdlist, color=(64, 64, 64), image=8):
        """
        Note cmdlist should be in list of string form, not objects directly
            pass 'self' as ship
        """
        self.cmdlist = cmdlist
        super(AIShip_SetList, self).__init__(name, pos, world, self.__callback, color, image)

    def ship_added(self):
        self.__callback() # queue up first command when added to world

    def __callback(self):
        if len(self.cmdlist) > 0:
            self.commandQueue.append(self.get_next_command())

    def get_next_command(self):
        return eval(self.cmdlist.pop(0))

    def add_command(self, cmd):
        """
        Add a command to the list, should be string.
        """
        self.cmdlist.append(cmd)


class AIShip_SetListLoop(AIShip_SetList): # Need to use string and eval to reinitialize commands for current states?    
    def __init__(self, name, pos, world, cmdlist, numtimes = 0, color=(64, 64, 64), image=8):
        self.current = 0
        self.loop = 0
        self.max_loop = numtimes
        return super(AIShip_SetListLoop, self).__init__(name, pos, world, cmdlist, color, image)

    def get_next_command(self):
        cmd = eval(self.cmdlist[self.current])
        self.current += 1
        if self.current >= len(self.cmdlist):
            self.current = 0
            self.loop += 1
            if self.max_loop > 0 and self.loop >= self.max_loop:
                self.cmdlist = []

        return cmd


class AIShip_Network_Harness:
    def __init__(self, name, callback, color=(64, 64, 64), image=8):
        self._name = name
        self._color = color
        self._image = image
        self._callback = callback
        self.id = name

    def connect(self, port=2012, host="localhost"):
        """
        Returns a client network connection to the server.

        callback will be called when the client is expected to return a command, just like the Java client.
        """
        self.__client = MWNL2.MWNL_Init(port, self._internal_callback)
        self.__client.connect(host)

        x = 0
        while not self.__client.haveID() and not self.__client.iserror() and x < 5:
            x += 1
            time.sleep(1)

        if self.__client.isconnected() and self.__client.haveID():
            logging.info("AI Client %s Connected to Server with ID %d", self._name, self.__client.getID())
            return True
        else:
            logging.error("AI %s Couldn't connect to server", self._name)
            return False

    def isconnected(self):
        return self.__client.isconnected()

    def disconnect(self):
        self.__client.close()

    def _internal_callback(self, sender, cmd):
        logging.debug("AI Ship %s Received: %s", self._name, repr(cmd))
        #print "got " + repr(cmd)
        if cmd[0] == MWNL_CMD_REQUEST:
            logging.info("MWNL Server Registration Request AI Ship %s", self._name)
            self.__client.send(MWNL_CMD_REGISTER, {"NAME": "* "+self._name+str(self.__client.getID())+" *", "COLOR": self._color, "IMAGEINDEX": self._image}, sender)
        elif cmd[0] == MWNL_CMD_ENVIRONMENT:
            #TODO: Notify if died by checking object ID? just do it in callback manually like 'old' days?
            logging.info("AI Ship %s Making callback to %s", self._name, repr(self._callback))
            response = self._callback(cmd[1])
            logging.info("AI Ship %s callback said to %s", self._name, repr(response))
            if response == None or not isinstance(response, Command): 
                self.__client.close()
            elif self.__client.isconnected():
                self.__client.send(MWNL_CMD_SHIPCMD, response.net_repr(), sender)
        elif cmd[0] == MWNL_CMD_ERROR:
            #print "ERROR:", cmd[1]
            logging.error("AI Ship %s Command Error: %s", self._name, repr(cmd[1]))
        elif cmd[0] == MWNL2.MWNL_CMD_DISCONNECT:
            #print "DISCONNECTED"
            logging.info("Disconnected AI Ship %s", self._name)
        elif cmd[0] == MWNL2.MWNL_CMD_ALREADY_CONNECTED:
            print "Multiple Connections Disallowed"
            logging.error("Multiple Connections Disallowed")
