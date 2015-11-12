import socket
 
UDP_IP = "10.170.67.252"
UDP_PORT = 3141
sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM) 
sock.bind((UDP_IP, UDP_PORT))
while True:
    data, addr = sock.recvfrom(1024) 
    print "received message:", data