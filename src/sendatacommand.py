import serial
import time


def millis():
    return int(round(time.time() * 1000))

def sendATCommand(ser, command, expectedResponse, timeout, delayForInput):
    time.sleep(0.1)
    
    # Clear the input buffer
    print 'Clearing input buffer'
    while ser.inWaiting() > 0:
        ser.read(size=1)
    
    print command
    ser.write(command + '\r')
    previous = millis()
    response = ''
    while True:
        if ser.inWaiting() > 0:
            c = ser.read(size=1)
            #print c,
            response += c
            i = response.find(expectedResponse)
            if i != -1:
                time.sleep(delayForInput)
                break
        if (millis() - previous) > timeout:
            break
    if ser.inWaiting() > 0:
        response += ser.read(size=ser.inWaiting())
    return response.strip()

data = '{"temp":11,"bat":4123,"signal":19,"berror":0}'


ser=serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
ser.open()
ser.write('\r\r\r\r\r\r\r\r\r')
print sendATCommand(ser, 'AT', 'OK', 5000, 0.1)
print sendATCommand(ser, 'ATE0', 'OK', 5000, 0.1)
print sendATCommand(ser, 'AT+CMEE=2', 'OK', 5000, 0.1)
#AT+CSQ
#AT+CREG?
print sendATCommand(ser, 'AT+CIPSTATUS', '', 5000, 0.1)
print sendATCommand(ser, 'AT+CGATT?', '+CGATT:', 5000, 0.1)
print sendATCommand(ser, 'AT+CIPSTATUS', '', 5000, 0.1)
print sendATCommand(ser, 'AT+CSTT="att.mvno"', 'OK', 5000, 0.1)
print sendATCommand(ser, 'AT+CIPSTATUS', '', 5000, 0.1)
#time.sleep(0.5)
print sendATCommand(ser, 'AT+CIICR', 'OK', 5000, 0.1)
print sendATCommand(ser, 'AT+CIPSTATUS', '', 5000, 0.1)
#time.sleep(0.5)
print sendATCommand(ser, 'AT+CIFSR', '', 5000, 0.1)
print sendATCommand(ser, 'AT+CIPSTATUS', '', 5000, 0.1)
#time.sleep(0.5)
print sendATCommand(ser, 'AT+CIPSTART="TCP","54.214.48.0","8888"', 'CONNECT OK', 5000, 0.1)
print sendATCommand(ser, 'AT+CIPSTATUS', '', 5000, 0.1)
#time.sleep(0.5)
for i in range(1):
    print sendATCommand(ser, 'AT+CIPSEND=%d' % len(data), '>', 5000, 0.1)
    print sendATCommand(ser, data, 'SEND OK', 5000, 0.1)
print sendATCommand(ser, 'AT+CIPSTATUS', '', 5000, 0.1)
print sendATCommand(ser, 'AT+CIPCLOSE', 'CLOSE OK', 5000, 0.1)
print sendATCommand(ser, 'AT+CIPSTATUS', '', 5000, 0.1)
print sendATCommand(ser, 'AT+CIPSHUT', 'SHUT OK', 5000, 0.1)
print sendATCommand(ser, 'AT+CIPSTATUS', '', 5000, 0.1)
ser.close()
