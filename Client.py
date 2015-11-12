import socket
import time 
UDP_IP = "10.170.67.252"
UDP_PORT = 3141
MESSAGE = "Hi"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE
sock = socket.socket(socket.AF_INET, # Internet
socket.SOCK_DGRAM) # UDP
i=0
while(i<10):
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    time.sleep(1)
    i+=1