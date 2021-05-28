import RPi.GPIO as GPIO
from time import sleep

STOP = 0
FORWARD = 1
BACKWORD = 2

CH1 = 0
CH2 = 1

OUTPUT = 1
INPUT = 0

HIGH = 1
LOW = 0

class drive():
    def __init__(self,ENA = 8, INA = 10, INB = 12):
        GPIO.setmode(GPIO.BOARD)
        self.ENA = ENA
        self.INA = INA
        self.INB = INB
        GPIO.setup(ENA, GPIO.OUT)
        GPIO.setup(INA, GPIO.OUT)
        GPIO.setup(INB, GPIO.OUT)
        self.pwm = GPIO.PWM(ENA, 100)
        self.pwm.start(0)


    def setMotorControl(self,pwm, INA, INB, speed, stat):
        pwm.ChangeDutyCycle(speed)

        if stat == FORWARD:
            GPIO.output(INA, HIGH)
            GPIO.output(INB, LOW)
            print("FORWARD")

        elif stat == BACKWORD:
            GPIO.output(INA, LOW)
            GPIO.output(INB, HIGH)
            print("BACKWARD")

        elif stat == STOP:
            GPIO.output(INA, LOW)
            GPIO.output(INB, LOW)
            print("STOP")
        print('init end')

    def go(self,speed =10):
        self.setMotorControl(self.pwm, self.INA, self.INB, speed, FORWARD)
        print("forward")
    def stop(self,speed =80):
        self.setMotorControl(self.pwm, self.INA, self.INB, speed, STOP)
        print("stop")
    def back(self,speed = 80):
        self.setMotorControl(self.pwm, self.INA, self.INB, speed, BACKWORD)
        print("backward")

