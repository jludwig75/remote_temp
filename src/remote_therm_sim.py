import sys
import socket
import random
import time
from temp_server.TemperatureServer import Server
import os


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 7000
MIN_TEMP = -20
MAX_TEMP = 40
MIN_VOLTAGE = 3700
MAX_VOLTAGE = 4250
MIN_SIGNAL = 0
MAX_SIGNAL = 99
MIN_ERR = 0
MAX_ERR = 99
DATA_FILE_NAME = 'data.txt'

GARBAGE = 'sfhhgk sfdh8934 54  hgSDF GHSFDT%$QWV^%#&BN %^&*N$&*N%&B$%V #XCQ$:";vb54;<<>>,/'


class RemoteTempServerTest:
    def __init__(self):
        self.statusStringsGenerated = 0
        self.outputString = ''

    def sendGarbage(self):
        l = random.randint(0, len(GARBAGE))
        if l > 0:
            start = random.randint(0, len(GARBAGE) - l)
            self.socket.sendall(GARBAGE[start:start + l])
    
    def sendString(self, st, avgNumParts):
        avgPartLen = len(st) / avgNumParts
        while len(st) > 0:
            l = random.randint(1, avgPartLen)
            self.socket.sendall(st[0:l])
            st = st[l:]
            time.sleep(0.001)
    
    def generateStatusString(self):
        t = random.randint(MIN_TEMP,MAX_TEMP)
        v = random.randint(MIN_VOLTAGE, MAX_VOLTAGE)
        s = random.randint(MIN_SIGNAL, MAX_SIGNAL)
        e = random.randint(MIN_ERR, MAX_ERR)
        st = '{"temp":%d,"bat":%d,"signal":%d,"berror":%d}' % (t, v, s, e)
        self.outputString += '%d,%d,%d,%d\n' % (t, v, s, e)
        self.statusStringsGenerated += 1
        return st
    
    def nonFragmentedSingleRecord(self):
        self.socket.sendall(self.generateStatusString())
    
    def fragmentedSingleRecord(self):
        st = self.generateStatusString()
        self.sendString(st, 4)
    
    def highlyFragmentedSingleRecord(self):
        st = self.generateStatusString()
        self.sendString(st, 11)
    
    def nonFragmentedMultipleRecords(self):
        st = ''
        for i in range(3):
            st += self.generateStatusString()
        self.socket.sendall(st)
    
    def fragmentedMultipleRecords(self):
        st = ''
        for i in range(3):
            st += self.generateStatusString()
        self.sendString(st, 4)
    
    def highlyFragmentedMultipleRecords(self):
        st = ''
        for i in range(3):
            st += self.generateStatusString()
        self.sendString(st, 23)
    
    def runTestIteration(self):
        print 'Running test iteration: Reporting temperature and voltage.'
        self.sendGarbage()
        self.nonFragmentedSingleRecord()
        self.sendGarbage()
        self.fragmentedSingleRecord()
        self.sendGarbage()
        self.highlyFragmentedSingleRecord()
        self.sendGarbage()
        
        self.sendGarbage()
        self.sendGarbage()
        
        self.sendGarbage()
        self.nonFragmentedMultipleRecords()
        self.sendGarbage()
        self.fragmentedMultipleRecords()
        self.sendGarbage()
        self.highlyFragmentedMultipleRecords()
        self.sendGarbage()
        
    def runTests(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((SERVER_HOST, SERVER_PORT))
        
        for i in range(10):
            self.runTestIteration()
    
        self.socket.close()
    
    def verifyOutput(self):
        with open(DATA_FILE_NAME, 'r') as file:
            data = file.read()
            if data == self.outputString:
                print 'PASS: Output matches'
                return 0
            else:
                print 'FAIL: Output does not match'
                print 'Expected output:\n%s' % self.outputString
                print 'Actual output:\n%s' % data
                return -1
    
def Main(progName, args):
    testServer = '--test-server' in args or '-t' in args
    
    print testServer

    if testServer:        
        os.unlink(DATA_FILE_NAME)
        server = Server(SERVER_PORT, DATA_FILE_NAME)
        
    test = RemoteTempServerTest()
    
    if testServer:
        server.start()
    
    test.runTests()
    time.sleep(0.25)

    if testServer:
        server.stopServer()
        return test.verifyOutput()
    
    return 0

 
if __name__ == '__main__':
    sys.exit(Main(sys.argv[0], sys.argv[1:]))