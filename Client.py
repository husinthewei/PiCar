import socket
import time 
import select
import RPi.GPIO as GPIO

#UDP_IP = "10.170.67.252" (school)
UDP_IP = "192.168.1.10"
UDP_PORT = 3141
MESSAGE = "Hi"

A1 = 7
A2 = 8

A3 = 23
A4 = 24
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(A1,GPIO.OUT)
GPIO.setup(A2,GPIO.OUT)
GPIO.setup(A3,GPIO.OUT)
GPIO.setup(A4,GPIO.OUT)

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
        #print "received message:", data   
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
        right()
    if(msg[3:4] == "1"):
        left()
        
while(True):
    msg = UDPCom()
    print "received message:", msg
    analyzeIn(msg) 
    time.sleep(0.10) 