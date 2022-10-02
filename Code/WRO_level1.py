

from lib2to3.pgen2 import driver
from locale import D_FMT
from turtle import window_width
import RPi.GPIO as GPIO          
import time
import math

from time import sleep
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



dc_direction = "f"
def dcMotor(speed,direction,p):
    temp1=1
    direction = direction
    if direction=='r':
        print("run")
        if(temp1==1):
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)     #Ask user for angle and turn servo to it
            print("forward")
            dc_direction = "f"
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
        dc_direction = "s"
        direction='z'

    elif direction=='f':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        temp1=1
        dc_direction = "f"
        direction='z'

    elif direction=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        temp1=0
        direction='z'
        dc_direction = "b"
    else:
        print("<<<  wrong data  >>>")


servo_angle = 60
GPIO.setup(15,GPIO.OUT)
servo1 = GPIO.PWM(15,50) # pin 11 for servo1, pulse 50Hz


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




###### UltraSonic *********
GPIO.setwarnings(False)
trigPin_FR = 21
echoPin_FR = 23

trigPin_FL = 31
echoPin_FL = 33

trigPin_F = 35
echoPin_F = 37

trigPin_R = 26
echoPin_R = 32

trigPin_L = 11
echoPin_L = 13



GPIO.setup(trigPin_F,GPIO.OUT)
GPIO.setup(echoPin_F,GPIO.IN)

GPIO.setup(trigPin_FL,GPIO.OUT)
GPIO.setup(echoPin_FL,GPIO.IN)

GPIO.setup(trigPin_FR,GPIO.OUT)
GPIO.setup(echoPin_FR,GPIO.IN)

GPIO.setup(trigPin_R,GPIO.OUT)
GPIO.setup(echoPin_R,GPIO.IN)

GPIO.setup(trigPin_L,GPIO.OUT)
GPIO.setup(echoPin_L,GPIO.IN)





def get_distance(TRIG,ECHO):
    try:
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        while GPIO.input(ECHO) == 0:
            pulseStart = time.time()
        while GPIO.input(ECHO) == 1:
            pulseEnd = time.time()
        pulseDuration = pulseEnd - pulseStart
        distance = pulseDuration * 17150
        distance = round(distance, 2)
        return distance
    except:
        return -1




dc_speed = 80
p.start(dc_speed)
dcMotor(dc_speed,"r",p)
servoSetAngle(60)

statuse = 0  # 0 => forwared   1 => loop      2 => Collision
cw = -1
####################### main loop
ultra_sleep = .08
d_L = get_distance(trigPin_L,echoPin_L)

sleep(ultra_sleep)
d_R = get_distance(trigPin_R,echoPin_R)


loop_times = 0
danger_distance = 20
middle_width = 15
road_width = 100
if d_R + d_L + 15 > 80:
    road_width = 100
    middle_width = 20
else:
    road_width = 60
    middle_width = 20
loop_angle = 25

middle_angle = 8
print(road_width)
while(True):
    print("===========================")
    print(" ")
    print(road_width)
    print("")
    d_F_L = get_distance(trigPin_FL,echoPin_FL)
    print(1)
    sleep(ultra_sleep)
    d_F = get_distance(trigPin_F,echoPin_F)
    sleep(ultra_sleep)
    print(2)
    d_F_R = get_distance(trigPin_FR,echoPin_FR)
    sleep(ultra_sleep)
    print(3)
    d_L = get_distance(trigPin_L,echoPin_L)
    sleep(ultra_sleep)
    print(4)
    d_R = get_distance(trigPin_R,echoPin_R)
    sleep(ultra_sleep)
    print(5)


    if d_F == -1 or d_R == -1 or d_L == -1 or d_F_R == -1 or d_F_R == -1:
        #print("PASS")
        pass

    # Loop Action 
    elif (statuse == 1) : 
        if dc_speed != 60:
            dc_speed = 60
            dcMotor(60,"r",p)
        print("Loop Action  => ************")
        # Set Turn Angle
        if cw == 1:
            if d_F < danger_distance:
                dcMotor(80,"s",p)
                if servo_angle != 60:
                    servo_angle = 60 
                    servoSetAngle(servo_angle)
                dcMotor(60,"b",p)
                sleep(1.8)
                dcMotor(60,"f",p)            
            else:
                if(servo_angle != 60 +loop_angle):
                    servo_angle = 60 + loop_angle
                    servoSetAngle(servo_angle)
        
        
        else:   # CCW 
            if d_F< danger_distance:
                dcMotor(80,"s",p)
                if servo_angle != 60:
                    servo_angle = 60 
                    servoSetAngle(servo_angle)
                dcMotor(60,"b",p)
                sleep(1.8)
                dcMotor(60,"f",p)
            else :
                if servo_angle != 60 - loop_angle: 
                    servo_angle = 60 - loop_angle
                    servoSetAngle(servo_angle)
        
        #End of Turn 
        if d_F > 160 and d_F_R + d_F_L < road_width -10:
            if loop_times == 12:
                if servo_angle != 60:
                    servo_angle = 60
                    servoSetAngle(servo_angle)
                sleep(1.5)
                break             
            if servo_angle != 60:
                servoSetAngle(60)
            statuse = 0   # Change Status to Forwared




    # Forwared Action
    elif statuse == 0:
        # Test LOOP  (Check LOOP)
        if d_F_L + d_F_R > 260 :
            # Test LOOP  (Check LOOP)
            if d_F_L + d_F_R > 260:
                loop_times +=1
                # Road Width
                if d_F > 65:
                    road_width = 100
                    loop_angle = 25
                    middle_width = 20
                    if dc_speed != 70:
                        dcMotor(dc_speed,"r",p)
                    
                else:
                    road_width = 60
                    loop_angle = 30
                    middle_width = 15 
                    if dc_speed != 60:
                        dcMotor(dc_speed,"r",p)
            # Check CW
            if cw == -1:
                if d_F_R > d_F_L:
                    cw = 1
                else:
                    cw = 2
            statuse = 1
        
        
        # Test Forwared Risk 
        elif d_F < danger_distance :
            print("risk")
            if d_F < danger_distance:
                dcMotor(60,"s",p)
                if servo_angle != 60:
                    servo_angle = 60 
                    servoSetAngle(servo_angle)
                dcMotor(60,"b",p)
                sleep(1.2)
                dcMotor(60,"f",p)      
        
        # Test Diagonal 
        # Midle Chick   Near Wall
        elif (abs(d_R - d_L) > middle_width or abs(d_F_R - d_F_L) > middle_width):   #( dynamic Number )
            print("not in the middle")
            if d_F_R >  d_F_L :
                if servo_angle != 60 + middle_angle:
                    servo_angle = 60 + middle_angle
                    servoSetAngle(servo_angle)
            else:
                if servo_angle != 60 - middle_angle:
                    servo_angle = 60 - middle_angle
                    servoSetAngle(servo_angle)

        
        #Angle (Diagonal only in Middle )
        elif abs(d_F_L - d_L) > 2 and cw != 2: 
            print("slope fix")
            if d_F_L > d_L:
                if servo_angle!= 50:
                    servo_angle = 50
                    servoSetAngle(servo_angle)
            else:
                if servo_angle != 70:
                    servo_angle = 70
                    servoSetAngle(servo_angle)
        elif  abs(d_F_R  - d_R) > 2 and cw != 1 and (d_F < 100 or d_F > 200):
                if d_F_R > d_R:
                    if servo_angle!= 70:
                        servo_angle = 70
                        servoSetAngle(servo_angle)
                else:
                    if servo_angle != 50:
                        servo_angle = 50
                        servoSetAngle(servo_angle)               
        else:
            if servo_angle != 60:
                servo_angle = 60
                servoSetAngle(servo_angle)
                
    sleep(.08)
dcMotor(80,"s",p)
servoSetAngle(60)