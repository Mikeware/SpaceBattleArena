
from collections import deque
import time

class MessageQueue(deque):
    """
    represents a queue of messages
    Will automatically destroy messages in the queue if they are older than their TimeToLive value
    """
    def __init__(self, bufferSize=16):
        super(MessageQueue, self).__init__([], bufferSize)

    """
    def __setitem__(self, key, value):
        if not isinstance(value, Message):
            return
        elif len(self) == self.bufferSize:
            super(MessageQueue, self).popleft()
        return super(MessageQueue, self).__setitem__(key, value)
    """

    def getNextMessage(self):
        item = None
        expired = False
        while len(self) > 0:
            item = super(MessageQueue, self).popleft()
            expired = item.isExpired()
            if not expired:
                break
        
        return None if expired else item

    def popleft(self):
        return self.getNextMessage()

    def append(self, value):
        if not isinstance(value, Message):
            return
        elif len(self) == self.maxlen:
            self.popleft()
        return super(MessageQueue, self).append(value)

class Message(object):
    """
    describes a game message
    All in game messages are 5 letters long
    """

    def __init__(self, msg, ttl=-1):
        """creates a message that will live until processed or when ttl is hit (ttl in sec)"""
        if isinstance(msg, str):
            self.message = msg[:5]
        else:
            self.message = "NULL0"
        self.timeToLive = ttl
        if self.timeToLive != -1:
            self.__endTime = time.time() + ttl        

    def isExpired(self):
        """
        Returns True when the message has expired
        """
        if self.timeToLive == -1: return False
        return time.time() > self.__endTime

    def __repr__(self):
        return "Message(" + self.message + ", " + repr(self.timeToLive) + ")"

    def __str__(self):
        return self.message

class Command(Message):
    """
    Special type of message
    """
    def __init__(self, obj, msg, ttl=4, block=False, required=0):
        super(Command, self).__init__(msg, ttl)
        self._obj = obj
        self.blocking = block
        self.energycost = 0
        self.initialrequiredenergy = required

    def isComplete(self):
        return False

    def execute(self, t):
        pass

    def __repr__(self):
        return "Command(#" + str(self._obj.id) + ", " + self.message + ", " + repr(self.timeToLive) + ", " + repr(self.blocking) + ", " + repr(self.initialrequiredenergy) + ")"

class OneTimeCommand(Command):
    def __init__(self, obj, msg, executefirst=False, ttl=4, required=0):
        super(OneTimeCommand, self).__init__(obj, msg, ttl, block=True, required=required)
        self.__pre_execute = executefirst
        self.__executed = False
        self.__done = False

    def isComplete(self):
        return self.__done and self.__executed

    def isExpired(self):
        self.__done = super(OneTimeCommand, self).isExpired()
        # execute when expiring if tail end
        if self.__done and not self.__executed:
            self.__executed = True
            self.onetime()

    def execute(self, t):
        # check if execute now if front end
        if not self.__executed and self.__pre_execute:
            self.__executed = True
            self.onetime()

        self.isExpired()
        
    def onetime(self):
        pass

if __name__ == "__main__":
    m = MessageQueue()
    for i in range(5):
        m.append(Message(repr(i)+"TEST1", 6))
        st = time.time()
        while time.time() < st + 1:
            pass

    st = time.time()
    while time.time() < st + 3:
        pass

    print m
    print m.getNextMessage()
    print m
