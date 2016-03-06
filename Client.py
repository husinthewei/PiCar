import socket
import time 
#UDP_IP = "10.170.67.252"
UDP_IP = "192.168.1.11"
UDP_PORT = 3141
MESSAGE = "Hi"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE
sock = socket.socket(socket.AF_INET, # Internet
socket.SOCK_DGRAM) # UDP
i=0
while(i<1000):
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", data    
    time.sleep(0.5)

    i+=1