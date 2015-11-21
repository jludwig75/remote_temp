import serial
import time

def SendSMS(message):
   #send SMS about the action
   ser=serial.Serial('/dev/ttyAMA0',9600,timeout=1)
   ser.open()

   ser.write("at\r")
   time.sleep(0.3)
   line=ser.read(size=64)
   print line

   ser.write("AT+CMGF=1\r")
   time.sleep(0.1)
   #line=ser.read(size=64)
   #print line

   ser.write('AT+CMGS="+18013600861"\r')
   time.sleep(0.2)
   ser.write(message)
   time.sleep(0.5)
   ser.write(chr(26))
   time.sleep(0.5)
 
   line=ser.read(size=64)
   print line

   ser.close()
   return


SendSMS("Hi. This is a test.")
