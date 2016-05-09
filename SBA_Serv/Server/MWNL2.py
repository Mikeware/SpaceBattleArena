import socket
import time
import thread, threading, atexit, logging, json

# Mikeware Network Lib
#----------------------
# A Client/Host Networking Library, Allowing For Easy Creation of Network Games
# Copyright 2005-2012 Mikeware

# TODO: Give Connection ID number and pass back, check that IDs match to prevent spoofing...

MWNL_TIMEOUT = 1
MWNL_CMD_ASSIGN_ID = "MWNL2_ASSIGNMENT"
MWNL_CMD_ALREADY_CONNECTED = "MWNL2_AC"
MWNL_CMD_CLIENT_CONNECTED = "MWNL2_CLIENT_CONNECTED"
MWNL_CMD_DISCONNECT = "MWNL2_DISCONNECT"
MWNL_CMD_PING = "MWNL2_PING"
MWNL_CMD_PONG = "MWNL2_PONG"
MWNL_BLOCKSIZE = 1450

def getIPAddress():
    return socket.gethostbyname(socket.gethostname())

# The Main Network Class That Establishes the Network Connections, Maintains them, and handles all connections
class MWNL_Init:
    IDCounter = 0
    
    # Called To Initialize Class and Socket
    def __init__(self, port, callback):
        self.__connections = {}
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__port = port
        self.__blocksize = MWNL_BLOCKSIZE
        self.__host = 0
        self.__callback = callback
        self.__incomingdata = ""
        self.__id = -1
        self.__allowallremoteconnections = True

        self.__acceptNewClients = 0
        self.__connalive = 0
        self.__threadsalive = 0
        
        atexit.register(self.__close)
    #END __init__
    
    # Are we the host?
    def ishost(self):
        return self.__host
    #END ishost

    def isconnected(self):
        return (self.__id >= 0)

    def iserror(self):
        return (self.__id == -2)

    def haveID(self):
        return (self.__id <> -1)
    #END haveID
    
    def getID(self):
        return self.__id
    #END getID

    def getIDStr(self):
        return str(self.__id)
    #END IF
    
    def numClients(self):
        return len(self.__connections.values())
    #END numConnections
    
    def getClientIDs(self):
        return self.__connections.keys()
    #END getClientIDs

    # Takes Dictionary with Keys = Current IDs and Values = New IDs
    def remapIDs(self, newIDdict):
        # Rearrange Host's Dictionary & Sends New IDS to Clients
        
        # First Off Send Client's New IDs
        for curID in newIDdict.keys():
            logging.info("Sending " + str(curID) + " new ID of " + str(newIDdict[curID]))
            self.send(MWNL_CMD_ASSIGN_ID, newIDdict[curID], curID)
        #END FOR

        # Have Original Copy Of Connections
        olddict = self.__connections.copy()

        # Rearrange Connections In Place
        for curID in newIDdict.keys():
            self.__connections[newIDdict[curID]] = olddict[curID]
            self.__connections[newIDdict[curID]]._setID(newIDdict[curID])
        #END FOR

        # Delete Copy
        del olddict
    #END remapIDs

    # Called To Start Being a Host
    def host(self, allowmultipleremoteconnections=True):
        self.__host = 1
        self.__id = 0
        self.__allowallremoteconnections = allowmultipleremoteconnections
        
        # Active Connection
        self.__connalive = 1

        # Continually Listen For Clients
        self.acceptNewClients()
    #END host

    def acceptNewClients(self, value=1):
        if self.ishost():
            if self.__acceptNewClients == value:
                return 0
            #END IF
            
            if self.__acceptNewClients == 1:
                logging.info("Not accepting new clients")
                self.__acceptNewClients = 0
                
                # Close if no clients
                if self.numClients() == 0:
                    logging.info("No more clients, closing")
                    self.close()
                #END IF
            else:
                logging.info("Accepting New Clients")
                self.__acceptNewClients = 1

                threading.Thread(None, self.__THREAD__getClients, "MWNL2_getClients").start()
            #END IF
                
            return 1
        else:
            return 0
        #END IF
    #END acceptNewClients

    # Connects to Remote Host
    def connect(self, host, tries = 10):
        connected = 0

        logging.info("Connecting to %s:%d...", host, self.__port)
        for t in range(tries):
            try:
                self.__socket.connect((host, self.__port))
                connected = 1
                break
            except:
                logging.error("Failed to Connect to %s:%d...", host, self.__port)
                time.sleep(1)
            #END TRY/EXCEPT
        #END FOR

        if connected:
            logging.info("Successfully Connected")

            # Active Connection
            self.__connalive = 1
            
            self.__connections[self.__id] = MWNL_Connection((self.__socket, ("localhost", self.__port)), self.__id, self.__gotTag)
        #END IF

        return connected
    #END connect
    
    def close(self, specificconnection=0, senddis=1):
        if specificconnection == 0:
            threading.Thread(None, self.__THREAD__close, "Close All Clients Thread", (senddis,)).start()
        else:
            self.__disconnectClient(specificconnection)
        #eif
    #END close
    
    # Closes Network Connections
    def __close(self, senddis=1):
        # Send Network Message, If Client Died
        if self.__id >= 0:
            logging.info("Sending Disconnect Message")
            if senddis == 1:
                self.broadcast(MWNL_CMD_DISCONNECT)      

            # Inform Calling Process of Disconnect (And Do What They Want First)
            # Want To Block Here So They Can Do Something?
            self.__callback(0, [MWNL_CMD_DISCONNECT])
        #if self.haveID():            
        #    if self.ishost():
        #        logging.info("Broadcasting Disconnect")
        #        self.broadcast(MWNL_CMD_DISCONNECT)
        #    else:
        #        logging.info("Notifying Server, Disconnected")
        #        self.send(MWNL_CMD_DISCONNECT)
        #    #eif
        #END IF
        
        if self.__id != -2:
            # Close All Connections
            for conn in self.__connections.values():
                conn.close()
            #END FOR

            self.__killThreads()

            logging.info("Closing Main Socket")
            #self.__socket.shutdown(socket.SHUT_RDWR)
            self.__socket.close()
        
            # Close
            self.__id = -2

            # Destroy Object
            del self
    #END IF

    # Used To Prevent Blocking On Client
    def __THREAD__close(self, senddis):
        #if self.haveID():
        self.__close(senddis)
        #eif
    #END IF

    # Used To Prevent Blocking On Client
    def __makeCallback(self, sender, cmd):
        threading.Thread(None, self.__callback, "Client Callback %d %s" % (sender, repr(cmd)), (sender, cmd)).start()
    #END __makeCallback

    # Connection Was Removed (Not Necessarily Closed)
    def __killThreads(self):
        if self.__connalive == 1:
            logging.info("Killing Main Threads...")

            logging.info(str(self.__threadsalive) + " Thread(s) Alive")

            # Kill Listend Thread
            self.__connalive = 0
            
            # Wait For Thread To Die
            while self.__threadsalive > 0:
                pass
            #END WHILE
        #END IF
    #END __killThreads__

    # Broadcasts a command to everyone connected to the server
    def broadcast(self, command, data = None):
        self.send(command, data, None)
    #end broadcast
    
    # Sends a Command with extra data object, optionally to a specific client
    # if on the server, will broadcast if no sendto
    # if on the client, defaults to send to server only
    def send(self, command, data = None, sendto = 0):        
        logging.debug("Enter Send: %d %s", self.__id, repr(self.haveID()))
        while not self.haveID():
            pass
        #wend

        logging.debug("Sending Command %s to %s", command, repr(sendto))

        info = (self.__id, sendto)

        # Host
        if self.ishost():
            if sendto != None and sendto > 0:
                logging.debug("Sending to specific connection: %d", sendto)
                if sendto in self.__connections:
                    # Send To Specific Connection
                    logging.debug("Sent to connection")
                    self.__connections[sendto].send(info, command, data)
                else:
                    logging.error("Couldn't find connection in %s", repr(self.__connections))
                #eif
            else:
                # Broadcast Message
                for conn in self.__connections.values():
                    logging.debug("Broadcasting to " + repr(conn.getAddress()))
                    conn.send(info, command, data)
                #END FOR
            #END IF
        # Client
        elif self.__connections.has_key(self.__id):
            logging.debug("Sending message to host")
            # Send To Host
            self.__connections[self.__id].send(info, command, data)
        #END IF
        logging.debug("Exit Send")
    #END __send

    # THREADS
    # Just Adds New Clients To Connection List
    def __THREAD__getClients(self):
        self.__threadsalive += 1
        
        logging.info("Waiting For Clients...")

        acquire = 0
        while acquire == 0 and self.__connalive:
            try:
                self.__socket.bind(('', self.__port))
                acquire = 1
            except:
                logging.info("Port Closed, Waiting...")
                time.sleep(MWNL_TIMEOUT * 10)
            #END TRY/EXCEPT
        #END WHILE
        
        # Queue 3 Connections, Should Be Enough With Our Thread
        self.__socket.listen(3)

        while self.__connalive and self.__acceptNewClients:
            if self.__connalive == 0:
                logging.info("Should Die!")
            #END IF
                
            # Wait For New Connection
            try:
                self.__socket.settimeout(MWNL_TIMEOUT)
                newconn = self.__socket.accept()
                self.__socket.settimeout(None)
                if newconn[0] <> None:
                    logging.info("New Connection From: %s", repr(newconn[1]))
                    
                    # Temp Assign Connection ID
                    MWNL_Init.IDCounter += 1
                    newID = MWNL_Init.IDCounter
                                        
                    if not self.__allowallremoteconnections:
                        # check if connection already exists
                        found = False
                        for conn in self.__connections.values():
                            if conn.getAddress()[0] == newconn[1][0]: # (ip, port)
                                logging.warning("Client Already Connected")
                                # temp add so we can send via regular methods
                                self.__connections[newID] = MWNL_Connection(newconn, newID, self.__gotTag)
                                self.send(MWNL_CMD_ALREADY_CONNECTED, sendto=newID)
                                self.__disconnectClient(newID)
                                found = True
                                break     
                            #eif
                        #next conn

                        # skip past the sending of ID assignment
                        if found:
                            continue
                    #eif
                    
                    self.__connections[newID] = MWNL_Connection(newconn, newID, self.__gotTag)
                    logging.info("conn: %s", repr(self.__connections[newID]))
                    self.send(MWNL_CMD_ASSIGN_ID, newID, newID)
                    self.__callback(newID, [MWNL_CMD_CLIENT_CONNECTED])
                #END IF
            except:
                # will get error here on timeout
                pass
                #logging.error(traceback.format_exc())
                #print traceback.format_exc()
            #END TRY/EXCEPT
        #END WHILE

        # Close Socket
        self.__socket.close()

        self.__threadsalive -= 1

        logging.info("Stopped Waiting For Clients...")
    #END __THREAD__getClients
    
    # Callback from Client Threads When Complete Tag Received
    def __gotTag(self, datalist):              
        # Do We Have Anything?
        if datalist <> None and isinstance(datalist, list) and len(datalist) >= 2 and len(datalist[0]) == 2:
            logging.debug("Got Data: %s", repr(datalist[2:]))

            # Break into Readable Vars
            sender = datalist[0][0]
            receiver = datalist[0][1]
            cmd = datalist[1]
            data = None
            if len(datalist) > 2:
                data = datalist[2]
            #eif

            if self.ishost() and sender not in self.__connections:
                logging.error("Received message from invalid client id: %d", sender)
                return
            #eif

            if cmd == MWNL_CMD_PING:
                logging.info("pinged...ponging")
                self.send(MWNL_CMD_PONG, sendto=sender)
                print "PING!!!"
            elif cmd == MWNL_CMD_PONG:
                logging.info("received pong")
                print "PONG!!!"
            elif cmd == MWNL_CMD_DISCONNECT:
                # If Host, Client Died
                if self.ishost():
                    # TODO: Check that we already disconnected this client or not!
                    logging.info("Host Deleting Client Entry: %d", sender)
                    self.__disconnectClient(sender)

                    # No New Clients Acceptable, and No Clients Left
                    # Assume Termination, Will Have To ReInit if want to continue
                    if self.__acceptNewClients == 0 and len(self.__connections) == 0:
                        self.close()
                    #END IF

                    # notify server that client disconnected
                    self.__makeCallback(sender, [MWNL_CMD_DISCONNECT])
                # If Client, Host Died
                else:
                    logging.info("Client Closing")
                    self.close(0)
                #ENDIF
            elif cmd == MWNL_CMD_ALREADY_CONNECTED and not self.ishost():
                logging.info("Closing Client Already Connected")
                self.close(0)
            elif cmd == MWNL_CMD_ASSIGN_ID:
                logging.info("Received New ID: %s", repr(data))
                newID = int(data)
                    
                # Make Sure On Client
                if not self.ishost():
                    # Swap Socket To New ID
                    if newID <> self.__id:
                        self.__connections[newID] = self.__connections[self.__id]
                        del self.__connections[self.__id]
                        #print "newdic = " + repr(self.__connections)

                        self.__id = newID
                    else:
                        #print "Same ID!"
                        logging.error("Same ID Assigned??")
                    #END IF
                #END IF
            elif data == None:
                self.__makeCallback(sender, [cmd])
            else:
                self.__makeCallback(sender, [cmd, data])
            #END IF
        else:
            logging.error("Receive Data Error!")
        #END IF
    #END __gotTag

    def __disconnectClient(self, id):
        if self.__connections.has_key(id):
            logging.info("Trying to Disconnect Client %d", id)
            try:
                threading.Thread(None, self.__connections[id].close, "Close Specific Connection %d" % id).start()
                logging.info("Closing Threads...")
                del self.__connections[id]
                logging.info("newdic = %s", repr(self.__connections))
            except:
                logging.error("DIS: No Connection @%d", id)
            #END TRY/EXCEPT
        else:
            logging.warning("Client %d already disconnected", id)
        #eif            
    #END __disconnectClient
#END MWNL

# MWNL_Connection
#-----------------
# A Wrapper Class for a basic Socket Connection that handles sending, receiving, and processing of data
class MWNL_Connection:
    def __init__(self, conn, id, callback):
        self.__socket = conn[0]
        self.__address = conn[1]
        self.__id = id
        
        self.__blocksize = MWNL_BLOCKSIZE
        
        self.__incomingdata = ""
        self.__outgoingdata = ""
        
        # Used To Kill Threads
        self.__connalive = 1
        self.__threadsalive = 0
        
        # Used To Prevent Corruption of Data
        self.__inlock = threading.Condition()
        self.__outlock = threading.Condition()

        self.__callback = callback
        
        # Start Thread For This Connection
        threading.Thread(None, self.__THREAD__listen, "Client Receiving Thread %d" % id).start()
        threading.Thread(None, self.__THREAD__send, "Client Sending Thread %d" % id).start()
        threading.Thread(None, self.__THREAD__getNextTag, "Client Processing Thread %d" % id).start()
    #END __init__
    
    # Connection Was Removed (Not Necessarily Closed)
    def __killThreads(self):
        logging.info(repr(self.__address) + "Killing Threads...")
    
        # Kill Listend Thread
        self.__connalive = 0
        
        # Wait For Thread To Die
        while self.__threadsalive > 0:
            pass
        #END WHILE
    #END __killThreads
    
    def getAddress(self):
        return self.__address
    #END getAddress

    def _setID(self, id):
        self.__id == id
    
    # Closes Socket
    def close(self):
        logging.info("%s Closing Connection", repr(self.__address))
        
        # Let it Finish Sending All Data Before Closing Connection
        while self.__threadsalive > 0 and self.isSendingData():
            pass
        #END WHILE

        # Kill Threads
        self.__killThreads()

        # Close Socket
        #self.__socket.shutdown(socket.SHUT_RDWR)
        self.__socket.close()

        # Destroy Object
        del self
    #END close

    # Sends out through socket in (blocksize) increments
    def send(self, info, command, data):
        #print repr(self.__address) + "send start"
        #print "adding = " + data
        self.__outlock.acquire()
        
        #print repr(self.__address) + "outdata+ " + data

        #format outgoing data

        sendstr = ""
        if data != None:
            sendstr = json.dumps(info, separators=(',',':')) + ',' + json.dumps(command, separators=(',',':')) + ',' + json.dumps(data, separators=(',',':'))
        else:
            sendstr = json.dumps(info, separators=(',',':')) + ',' + json.dumps(command, separators=(',',':'))
        #eif

        sendstr = str(len(sendstr)) + sendstr
        
        logging.debug("Appending to Outgoing Data %d bytes", len(sendstr))

        self.__outgoingdata += sendstr
        
        self.__outlock.notify()
        self.__outlock.release()
        
        #print repr(self.__address) + "send end"
    #END send
    
    # Gets Next Complete Tag or Returns Nothing
    def __THREAD__getNextTag(self):
        self.__threadsalive += 1
        
        logging.info("%s Started Processing Incoming Data", repr(self.__address))
    
        atedata = 0
        
        while self.__connalive:
            retval = ""
    
            #print repr(self.__address) + "gnt start"
            
            self.__inlock.acquire()
            
            while ((len(self.__incomingdata) == 0) or (len(self.__incomingdata) < atedata)) and self.__connalive:
                self.__inlock.wait(MWNL_TIMEOUT)
            #END WHILE
            
            if self.__connalive:
                #print repr(self.__address) + "gnt run"

                logging.debug("Processing Incoming Data")
                
                i = self.__incomingdata.find("[")
                if i != -1:
                    #logging.debug("Found json data at " + repr(i))
                    #TODO: chop after all data received?
                    #logging.debug("Message Info Before: " + self.__incomingdata)
                    lofs = self.__incomingdata[:i]                    

                    # Do we have complete data
                    tlen = len(lofs) + int(lofs)
                    if len(self.__incomingdata) >= tlen:
                        #logging.debug("Processing json data found")
                        retval = self.__incomingdata[:tlen]
                        self.__incomingdata = self.__incomingdata[tlen:]

                        retval = json.loads("[" + retval[i:] + "]")
                    else:
                        logging.debug("Need more json data, need %d bytes", tlen)
                        atedata = tlen
                    #eif

                    #logging.debug("Message Info After: " + self.__incomingdata)
                else:
                    logging.error("%s Receive Error: %s", self.__address, self.__incomingdata)
                    atedata = 0
                #END IF
                
                # If We Have A Complete Tag, Process It
                if retval <> "":
                    atedata = 0

                    logging.debug("Making callback for command: %s", retval)

                    self.__callback(retval)
                #END IF
            #END IF
            
            #print repr(self.__address) + "gnt release"
            
            # Release After Completion Of Tag
            self.__inlock.release()
        #END WHILE
        
        self.__threadsalive -= 1
        
        logging.info("%s Stopped Processing Incoming Data", self.__address)
        
        thread.exit()
    #END IF

    def isSendingData(self):
        return (len(self.__outgoingdata) > 0)
    #END isSendingData
    
    # Listens For Incoming Data On Connection
    def __THREAD__listen(self):
        self.__threadsalive += 1        
        logging.info(repr(self.__address) + "Listening...")

        while self.__connalive:
            try:
                self.__socket.settimeout(MWNL_TIMEOUT)
                blk = self.__socket.recv(self.__blocksize)
                self.__socket.settimeout(None)

                if blk <> "":
                    #print repr(self.__address) + "listen start"
                    #print "recv = " + blk
                    self.__inlock.acquire()

                    #print repr(self.__address) + "indata+ " + blk
                    
                    logging.debug("Received " + repr(len(blk)) + " bytes")

                    self.__incomingdata += blk
                    
                    self.__inlock.notify()
                    self.__inlock.release()
                    
                    #print repr(self.__address) + "listen end"
                    
                    #print "icd = " + self.__incomingdata
                #END IF
            except:
                pass
            #END TRY/EXCEPT
        #END WHILE
        
        logging.info(repr(self.__address) + "Stopped Listening...")
        
        self.__threadsalive -= 1
        
        thread.exit()
    #END __THREAD__listen

    # Sends Data in Buffer
    def __THREAD__send(self):
        self.__threadsalive += 1
        logging.info(repr(self.__address) + "Ready To Send...")

        while self.__connalive:
            #print repr(self.__address) + "consend start"
            self.__outlock.acquire()
            
            while len(self.__outgoingdata) == 0 and self.__connalive:
                self.__outlock.wait(MWNL_TIMEOUT)
            #END WHILE
        
            try:
                if self.__connalive:
                    sending = ""
                    while len(self.__outgoingdata) > self.__blocksize:
                        sending = self.__outgoingdata[:self.__blocksize]
                        self.__outgoingdata = self.__outgoingdata[self.__blocksize:]
                        #print "ogdb = " + self.__outgoingdata
                    
                        #print "sendingb = " + sending
                        logging.debug("Sending Chunk " + repr(len(sending)) + " bytes")
                        self.__socket.send(sending)
                    #END WHILE
                    
                    if self.__connalive and len(self.__outgoingdata) > 0:
                        #print "sending = " + self.__outgoingdata
                        logging.debug("Sending " + repr(len(self.__outgoingdata)) + " bytes")
                        self.__socket.send(self.__outgoingdata) #Error if socket closed?
                        self.__outgoingdata = ""
    
                        #print "ogd = " + self.__outgoingdata
                    #END IF
                
                    #print repr(self.__address) + "outnow = " + self.__outgoingdata    
                #END IF
            except:
                self.__connalive = False
                logging.error("Error Sending Data - Remote Host Forced Closure?")
                self.__callback([(self.__id, 0), MWNL_CMD_DISCONNECT])
            
            self.__outlock.release()
                
            #print repr(self.__address) + "consend end"
        #END WHILE

        logging.info(repr(self.__address) + "Stopped Sending...")

        self.__threadsalive -= 1

        thread.exit()
    #END __THREAD__send
#END MWNL_Connection