'''
Created on Nov 11, 2015

@author: jludwig
'''
import socket
import json
import threading

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
    
    def run(self):
        #print 'Server started'
        with open(self.databaseFileName, 'a') as self.dataBaseFile:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(('', self.listenPort))
            self.socket.listen(2)
            while not self.stop:
                self.conn, addr = self.socket.accept()
                while not self.stop:
                    data = self.conn.recv(1024)
                    if not data:
                        break   # client disconnected
                    self.accumulateInput(data)
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
        self.processInputBuffer()
    
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
        
    def recordTemp(self, data):
        #print data
        data = json.loads(data)
        st = '%d,%d,%d,%d\n' % (data['temp'], data['bat'], data['signal'], data['berror'])
        if self.log:
            print 'Received data %s' % st,
        self.dataBaseFile.write(st)
        self.dataBaseFile.flush()
        