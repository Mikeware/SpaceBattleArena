"""
Space Battle Arena is a Programming Game.

Copyright (C) 2012-2016 Michael A. Hawker and Brett Wortzman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
"""

import logging, threading
from exceptions import NotImplementedError
from Messaging import MessageQueue, Message, Command

class CommandInterface(object):
    def __init__(self):
        pass

    def requestCommand(self, environment):
        raise NotImplementedError

class CommandSystem(object):
    """
    The Command System is a special system build around a MessageQueue
    it keeps track of running commands for periods of time and continues to execute commands until their execution time is complete
    it will not process new commands while a blocking command was taken from the queue
    """
    def __init__(self, parent, size):
        self.__parent = parent
        self.__queue = MessageQueue(size)
        self.__queueSemaphore = threading.Semaphore()

    def __len__(self):
        return len(self.__queue)

    def __contains__(self, item):
        found = False
        self.__queueSemaphore.acquire()
        for cmd in self.__queue:
            if item == cmd:
                found = True
                break
        self.__queueSemaphore.release()

        return found    
        
    def containstype(self, cmdtype, force=False):
        found = None
        if not force:
            self.__queueSemaphore.acquire()
        for cmd in self.__queue:
            if isinstance(cmd, cmdtype):
                found = cmd
                break
        if not force:
            self.__queueSemaphore.release()

        return found

    def __getitem__(self, key):
        return self.__queue[key]

    def append(self, cmd):
        if isinstance(cmd, Command):
            logging.debug("Added Command to Queue: %s", repr(cmd))
            self.__queueSemaphore.acquire()
            self.__queue.append(cmd)
            self.__queueSemaphore.release()

    def update(self, t):
        self.__queueSemaphore.acquire()
        thrust = self.__parent.thrusterForce
        for i in xrange(len(self)-1, -1, -1):
            cmd = self.__queue[i]
            if cmd.initialrequiredenergy > 0 and self.__parent.energy.value < cmd.initialrequiredenergy:
                logging.info("#%d Not Enough Energy To Start: %s", self.__parent.id, repr(self.__queue[i]))
                del self.__queue[i]
            else:
                self.__parent.energy -= cmd.initialrequiredenergy
                cmd.initialrequiredenergy = 0 # spent cost
                preven = self.__parent.energy
                #TODO: This is over eager, could slice more energy on hiccup...            
                self.__parent.energy -= cmd.energycost * t
                if cmd.isExpired() or cmd.isComplete() or self.__parent.energy.value == 0:
                    logging.info("Finished Executing Command: %s", repr(self.__queue[i]))                
                    if self.__parent.energy.value == 0:
                        logging.info("#%d Out of Energy", self.__parent.id)
                    del self.__queue[i]
                    logging.info("#%d Commands in Queue: %d", self.__parent.id, len(self))
                else:           
                    nt = t     
                    # Limit Thrust, TODO: Abstract
                    if cmd.NAME == "THRST":
                        thmod = self.__parent.thrusterForce * cmd.power
                        if thmod > thrust:
                            nt = t * (thrust / thmod)
                            logging.info("#%d Limiting Thrust time from %f to %f", self.__parent.id, t, nt)
                            self.__parent.energy = preven
                        else:                        
                            thrust -= thmod
                            logging.debug("Thrust Left %f", float(thrust))
                    cmd.execute(t)                
                #eif
            #eif

        self.__queueSemaphore.release()

        """
        if len(self) == 0 or not self.isBlockingCommandOnTop():
            nmsg = self.__queue.getNextMessage()
            if nmsg != None:
                logging.info("Activating Command: %s", nmsg)
                self.__activeCommandsSemaphore.acquire()
                self.__activeCommands.append(nmsg)
                self.__activeCommandsSemaphore.release()
        """

    def isBlockingCommandOnTop(self):
        # Returns True if there's a blocking command on top of the stack
        self.__queueSemaphore.acquire()
        x = (len(self.__queue) > 0 and self.__queue[len(self.__queue)-1].blocking)
        self.__queueSemaphore.release()
        return x

    def getRadarRepr(self):
        # Returns a short form of list with just the command names
        lst = []
        self.__queueSemaphore.acquire()
        for cmd in self.__queue:
            lst.append(cmd.NAME)
        self.__queueSemaphore.release()
        return lst

    def __repr__(self):
        return "CommandSystem(" + repr(self.__queue) + ")"
