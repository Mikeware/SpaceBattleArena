
from WorldCommands import *
from WorldEntities import Ship
from Game.Players import Player

class AIShip(Ship):
    NetIDs = -3

    def __init__(self, name, pos, world, callback):
        super(AIShip, self).__init__(pos, world)
        self.player = Player("* "+name+str(AIShip.NetIDs)+" *", (64, 64, 64), 8, AIShip.NetIDs, self) # ID Should be -3 or less, auto-assign
        AIShip.NetIDs -= 1
        self.rotationAngle = 0
        self._callback = callback

    def update(self, t):
        super(AIShip, self).update(t)

        if not self.commandQueue.isBlockingCommandOnTop():
            self._callback()

class AIShip_SetList(AIShip):
    def __init__(self, name, pos, world, cmdlist):
        """
        Note cmdlist should be in list of string form, not objects directly
            pass 'self' as ship
        """
        self.cmdlist = cmdlist
        super(AIShip_SetList, self).__init__(name, pos, world, self.__callback)
        self.__callback() # queue up first command        

    def __callback(self):
        if len(self.cmdlist) > 0:
            self.commandQueue.append(self.get_next_command())

    def get_next_command(self):
        return eval(self.cmdlist.pop(0))

class AIShip_SetListLoop(AIShip_SetList): # Need to use string and eval to reinitialize commands for current states?    
    def __init__(self, name, pos, world, cmdlist, numtimes = 0):
        self.current = 0
        self.loops = numtimes
        return super(AIShip_SetListLoop, self).__init__(name, pos, world, cmdlist)

    def get_next_command(self):
        cmd = eval(self.cmdlist[self.current])
        self.current += 1
        if self.current >= len(self.cmdlist):
            self.current = 0
            self.loops -= 1
            if self.loops == 0:
                self.cmdlist = []

        return cmd