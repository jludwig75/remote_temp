import serial
import time
import threading
import signal
import sys


class ConsoleReader(threading.Thread):
    def __init__(self, ser):
        threading.Thread.__init__(self)
        self.ser = ser
        self.stop_thread = False

    def run(self):
        while not self.stop_thread:
            line = self.ser.read(size=64)
            if len(line) > 0:
                print line,

    def stop(self):
        self.stop_thread = True
        self.join()


def HandleCommands(ser):
    while True:
        cmd = raw_input().strip()
        cmd = cmd.replace('\\x1A', chr(26))
        ser.write(cmd + '\r')


def signal_handler(signal, frame):
   print('Ctrl+C Exiting...')
   global ser
   global readerThread
   readerThread.stop()
   ser.close()
   sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

ser=serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
print dir(ser)
ser.open()
readerThread = ConsoleReader(ser)
readerThread.start()
ser.write('\r\r\r\r\r\r\r\r\r')
ser.write('AT\r')
ser.write('ATE0\r')
ser.write('AT+CMEE=2\r')
HandleCommands(ser)
readerThread.stop()
ser.close()
