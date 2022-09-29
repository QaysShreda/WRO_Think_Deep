
from ast import Global
import RPi.GPIO as GPIO          
from time import sleep
import time
import cv2

in1 = 36
in2 = 38
en = 40
temp1=1

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)


def dcMotor(speed,direction,p):
    temp1=1
    direction = direction
    if direction=='r':
        print("run")
        if(temp1==1):
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)     #Ask user for angle and turn servo to it
            print("forward")
            direction='z'
        else:
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            print("backward")
            x='z'

    elif direction=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        direction='z'

    elif direction=='f':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        temp1=1
        direction='z'

    elif direction=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        temp1=0
        direction='z'

    elif direction=='l':
        print("low")
        p.ChangeDutyCycle(25)
        direction='z'

    elif direction=='m':
        print("medium")
        p.ChangeDutyCycle(50)
        direction='z'

    elif direction=='h':
        print("high")
        p.ChangeDutyCycle(75)
        direction='z'
     
    
    # elif x=='e':
    #     GPIO.cleanup()
    #     print("GPIO Clean up")
        
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")


 

##### SERVO #####
GPIO.setup(3,GPIO.OUT)
servo1 = GPIO.PWM(3,50) # pin 11 for servo1, pulse 50Hz
servo1.start(0)

servo1.ChangeDutyCycle(2+(60/12))
sleep(0.5)
servo1.ChangeDutyCycle(0)


def servoSetAngle(angle):
        if angle > 90:
            angle = 90
        elif angle < 30:
            angle = 30
        servo1.ChangeDutyCycle(2+(angle/12))
        sleep(0.5)
        servo1.ChangeDutyCycle(0)

GPIO.setwarnings(False)
EchoPin = 37
TrigPin = 35
GPIO.setmode(GPIO.BOARD)
GPIO.setup(EchoPin,GPIO.IN)
GPIO.setup(TrigPin,GPIO.OUT)


def get_distance():
    GPIO.output(TrigPin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TrigPin, GPIO.LOW)
    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(EchoPin) == 0:
        StartTime = time.time()
    while GPIO.input(EchoPin) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance




p.start(100)
dcMotor(100,"r",p)
servoSetAngle(60)


startTime = time.time()
stopTime = time.time()



dcMotor(100,"s",p)
servoSetAngle(60)
GPIO.cleanup()

  


 
