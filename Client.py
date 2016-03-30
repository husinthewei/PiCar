import socket
import time 
import select
import RPi.GPIO as GPIO

#UDP_IP = "10.170.67.252" (school IP)
UDP_IP = "192.168.1.4"
UDP_PORT = 3141
MESSAGE = "REQ"

A1 = 7 #left gate1 (H-bridge)
A2 = 8 #left gate2 (H-bridge)

A3 = 23 #right gate1 (H-bridge)
A4 = 24 #right gate2 (H-bridge)

#Front: e=17 t=21
#Back: e=10 t=9
EchoFront = 17 #for utlrasonic sensors
TrigFront = 27
EchoBack = 10
TrigBack = 9

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(A1,GPIO.OUT)
GPIO.setup(A2,GPIO.OUT)
GPIO.setup(A3,GPIO.OUT)
GPIO.setup(A4,GPIO.OUT)

GPIO.setup(TrigFront,GPIO.OUT)
GPIO.setup(EchoFront,GPIO.IN)
GPIO.setup(TrigBack,GPIO.OUT)
GPIO.setup(EchoBack,GPIO.IN)

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE
sock = socket.socket(socket.AF_INET, # Internet
socket.SOCK_DGRAM) # UDP
i=0
sock.setblocking(0)


def forward():
    GPIO.output(A1,GPIO.HIGH)
    GPIO.output(A2,GPIO.LOW)
    GPIO.output(A3,GPIO.HIGH)
    GPIO.output(A4,GPIO.LOW)

def back():
    GPIO.output(A1,GPIO.LOW)
    GPIO.output(A2,GPIO.HIGH)
    GPIO.output(A3,GPIO.LOW)
    GPIO.output(A4,GPIO.HIGH)

def left():
    GPIO.output(A1,GPIO.HIGH)
    GPIO.output(A2,GPIO.LOW)
    GPIO.output(A3,GPIO.LOW)
    GPIO.output(A4,GPIO.HIGH)
def right():
    GPIO.output(A1,GPIO.LOW)
    GPIO.output(A2,GPIO.HIGH)
    GPIO.output(A3,GPIO.HIGH)
    GPIO.output(A4,GPIO.LOW)
    
def stop():
    GPIO.output(A1,GPIO.LOW)
    GPIO.output(A2,GPIO.LOW)
    GPIO.output(A3,GPIO.LOW)
    GPIO.output(A4,GPIO.LOW)
    
def UDPCom():
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    ready = select.select([sock], [], [], 2)
    if ready[0]: 
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        return data
    else:
        return "nothing received"   

def analyzeIn(msg):
    msg = str(msg)
    if (msg[0:1] == "1"):
        forward()
    if(msg[1:2] == "1"):
        back()
    if(msg[0:1] == "0" and msg[1:2] == "0"):
        stop()
        
    if(msg[2:3] == "1"):
        left()
    if(msg[3:4] == "1"):
        right()
        
def getDistance(echo, trig):
    GPIO.output(trig, True)     #triggering signal
    time.sleep(0.00001)
    GPIO.output(trig, False)
    signaloff = 0; signalon = 0;
    
    i = 0;
    while GPIO.input(echo) == 0 and i <300:     #If more than 300 readings (lost signal), cancel
          signaloff = time.time()                
          i+=1
    i=0;
    while GPIO.input(echo) == 1 and i <300:    # measuring return signal
          signalon = time.time()
          i+=1
    timepassed = signalon - signaloff    #difference in time
    distance = timepassed * 17000 #in cm  
    return distance

def doDistanceFeature():
    a = getDistance(EchoFront, TrigFront)    #reading sensor
    b = getDistance(EchoBack, TrigBack)      #reading sensor
    if(b < 20):         #if object is closer than 20 front or back, move away
        back()
    if(a < 20):        
        forward()
    if(a < 20 and b < 20 and  b < a):      #if one side is closer than the other while they are both "dangerous" 
        back()                              #move away from the closer side
    if(a < 20 and b < 20 and  a < b):      
        forward()    
        
while(True):             #main loop. Cycles every 0.1 seconds
    msg = UDPCom()       #gets the message. Has a 2 second timeout.
    print "received message:", msg
    analyzeIn(msg)       #Interprets message to move if necessary
    doDistanceFeature()  #Using ultrasonic sensor to prevent "crashes"
    time.sleep(0.1) 