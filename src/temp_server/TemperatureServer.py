'''
Created on Nov 11, 2015

@author: jludwig
'''
import socket
import json
import threading
import time
import os
from remotetempcommon import *

class Server(threading.Thread):

    def __init__(self, listenPort, databaseFileName, log = False):
        threading.Thread.__init__(self)
        self.listenPort = listenPort 
        self.databaseFileName = databaseFileName
        self.inputBuffer = ''
        self.dataBaseFile = None
        self.stop = False
        self.threaded = False
        self.conn = None
        self.socket = None
        self.log = log
        os.environ['TZ'] = 'US/Mountain'
        time.tzset()
    
    def run(self):
        #print 'Server started'
        with open(self.databaseFileName, 'a+') as self.dataBaseFile:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('', self.listenPort))
            self.socket.listen(2)
            while not self.stop:
                print 'Waiting for client connection...'
                self.conn, addr = self.socket.accept()
                print 'Accepted client connection'
                while not self.stop:
                    print 'Waiting for client data...'
                    data = self.conn.recv(1024)
                    if not data:
                        print 'Client disconnected'
                        break   # client disconnected
                    if self.accumulateInput(data):
                        self.conn.shutdown(socket.SHUT_RDWR)
                        self.conn.close()
                        break
            #print "Server shutting down"

    def startServer(self):
        self.start()
        self.threaded = True
    
    def stopServer(self):
        #print 'Telling server to stop'
        self.stop = True
        if self.conn:
            #print 'Closing client connection'
            self.conn.shutdown(socket.SHUT_RDWR)
            self.conn.close()
            self.conn = None
        if self.socket:
            #print 'Closing listening socket'
            self.socket.close()
            self.socket = None
            # Now connect to the socket to kick it.
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", self.listenPort))
        if self.threaded:
            #print 'Waiting for server thread to stop...'
            self.join()
        
    def accumulateInput(self, input):
        self.inputBuffer += input
        return self.processInputBuffer()
    
    def processInputBuffer(self):
        while True:
            start = self.inputBuffer.find('{')
            if start == -1:
                self.inputBuffer = ''
                break
            if start != 0:
                self.inputBuffer = self.inputBuffer[start:]
                start = 0
            end = self.inputBuffer.find('}')
            if end == -1:
                break
            end += 1
            self.recordTemp(self.inputBuffer[0:end])
            self.inputBuffer = self.inputBuffer[end:]
            return True
        return False
        
    def recordTemp(self, data):
        #print data
        data = json.loads(data)
        st = '%s,%d,%d,%d,%d\n' % (time.strftime(TIME_FORMAT_STRING, time.localtime()), data['temp'], data['bat'], data['signal'], data['berror'])
        if self.log:
            print 'Received data %s at %s' % (st.strip(), time.ctime())
        self.dataBaseFile.write(st)
        self.dataBaseFile.flush()
        
