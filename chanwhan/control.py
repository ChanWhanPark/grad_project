import serial
import sys
import time
from curtsies import Input

'''                              UART                               '''
''' KEY_UP : !F   KEY_DOWN : !B     KEY_LEFT : !TL  KEY_RIGHT: !TR  '''
'''     a  : !L          d : !R            s : !S                   '''
class WheelHandler():
    ser=0
    def __init__(self):
        self.ser=serial.Serial(port='/dev/ttyUSB0',baudrate=9600)
    def Forward(self):
        self.ser.write(bytes("!F".encode('ascii')))
    def Backward(self):
        self.ser.write(bytes("!B".encode('ascii')))
    def TurnLeft(self):
        self.ser.write(bytes("!TL".encode('ascii')))
    def TurnRight(self):
        self.ser.write(bytes("!TR".encode('ascii')))
    def VanishingPointLeft(self):
        self.ser.write(bytes("!L".encode('ascii')))
    def VanishingPointRight(self):
        self.ser.write(bytes("!R".encode('ascii')))
    def Stop(self):
        self.ser.write(bytes("!S".encode('ascii')))
    def FForward(self):
        self.ser.write(bytes("!P".encode('ascii')))
    def XL(self):
        self.ser.write(bytes("!XL".encode('ascii')))
    def XR(self):
        self.ser.write(bytes("!XR".encode('ascii')))
    def ZC(self):
        self.ser.write(bytes("!ZC".encode('ascii')))
    def ZD(self):
        self.ser.write(bytes("!ZD".encode('ascii')))
    def ZE(self):
        self.ser.write(bytes("!ZE".encode('ascii')))
    def ZF(self):
        self.ser.write(bytes("!ZF".encode('ascii')))
    def Wheel_Clean(self):
        self.ser.close()


def Input_key(key,wheel):
    '''     keyboard input function     '''
    print(key)
    if k==u"h":
        wheel.TurnLeft()
    elif k==u"l":
        wheel.TurnRight()
    elif k==u"w":
        wheel.Forward()
    elif k==u"x":
        wheel.Backward()
    elif k==u'j':
        wheel.VanishingPointLeft()
    elif k==u'k':
        wheel.VanishingPointRight()
    elif k==u's':
        wheel.Stop()
    elif k==u']':
        wheel.ser.close()
        sys.exit(1)
    elif k==u'u':
        wheel.FForward()
    elif k==u'a':
        wheel.XL()
    elif k==u'd':
        wheel.XR()
    elif k==u'q':
        wheel.ZC()
    elif k==u'e':
        wheel.ZD()
    elif k==u'z':
        wheel.ZE()
    elif k==u'c':
        wheel.ZF()
    else:
        print("Press Wheel Control Key or  Exit KEY(q)")

if __name__== '__main__':
    print("EXIT KEY is q")
    start = time.time()
    wheel=WheelHandler()
    with Input(keynames="curses") as input_generator:
        for k in input_generator:
            Input_key(k,wheel)
            print(time.time()-start)
