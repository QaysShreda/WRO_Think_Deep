

from lib2to3.pgen2 import driver
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

     
    
    # elif x=='e':
    #     GPIO.cleanup()
    #     print("GPIO Clean up")
        
    
    else:
        print("<<<  wrong data  >>>")
      #  print    startTime = time.time()
("please enter the defined data to continue.....")



print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")  



servo_angle = 60
GPIO.setup(15,GPIO.OUT)
servo1 = GPIO.PWM(15,50) # pin 11 for servo1, pulse 50Hz

# Start PWM running, with value of 0 (pulse off)
servo1.start(0)

# Loop to allow user to set servo angle. Try/finally allows exit
# with execution of servo.stop and GPIO cleanup :)
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


p.start(100)
dcMotor(100,"r",p)
servoSetAngle(60)


# for i in range(4):
#     servoSetAngle(60)  
#     sleep(5)
#     servoSetAngle(90)
#     sleep(2)

#startTime = time.time()
#stopTime = time.time()
####################### ???? ???????????? ?????????????????? ??????????????
def take_angle():
    ang = 0
    return ang


statuse = 0  # 0 => forwared   1 => loop      2 => Collision
cc = 0
####################### main loop
g= 60
ultra_sleep = .05
loopTime = 2.5
zone = 30
safe_distance = 20
danger_distance = 15
risk = False
d_F_L = get_distance(trigPin_FL,echoPin_FL)
sleep(ultra_sleep)
print("2")
d_F_R = get_distance(trigPin_FR,echoPin_FR)
sleep(ultra_sleep)
safe_zone = (d_F_L + d_F_R) / 3
while(True):
    print("//////////////////////////////////////////////")
#   startTime = time.time()
    servoSetAngle(60)
    d_F = get_distance(trigPin_F,echoPin_F)
    sleep(ultra_sleep)
    print("1")
    d_F_L = get_distance(trigPin_FL,echoPin_FL)
    sleep(ultra_sleep)
    print("2")
    d_F_R = get_distance(trigPin_FR,echoPin_FR)
    sleep(ultra_sleep)
    print("3")
    d_L = get_distance(trigPin_L,echoPin_L)
    print("4")
    sleep(ultra_sleep)
    d_R = get_distance(trigPin_R,echoPin_R)
    print("5")
    print(f"R + L = {d_R + d_L}")

    print(f"Front = {d_F}")
    #print(f"D_F_R {d_F_R}")
    #print(f"D_L {d_L}")
    
    # Test UlraSonic DisConnect 

    if d_F == -1 or d_R == -1 or d_L == -1 or d_F_R == -1 or d_F_R == -1:
        print("PASS")
        pass
    elif d_F < 20:
        dcMotor(100,"s",p)
        break 
    elif abs(d_F_L + d_F_R) > 270 : 
        if d_F_R > d_F_L:
            servo_angle = 85
            servoSetA








    # elif abs(d_F_R - d_F_L) < 14:
    #     print("Status : FR")
    #     if servo_angle != 60:
    #         servo_angle =60
    #         servoSetAngle(servo_angle)
    # elif abs(d_L - d_F_L) > 10:
    #     print("Correction")
    #     if servo_angle != 60:
    #         servo_angle =60
    #         servoSetAngle(servo_angle)
    # elif abs(d_F_R - d_F_L) >  15:
    #     print("Diagonal")
    #     if d_F_R < d_F_L:
    #         servo_angle -= 5
    #         servoSetAngle(servo_angle)
    #     else:
    #          servo_angle += 5
    #          servoSetAngle(servo_angle)
        
    sleep(.2)




   

    key = cv2.waitKey(1)
    if key == 27:
        dcMotor(100,"s",p)
        servoSetAngle(60)
        break
    
