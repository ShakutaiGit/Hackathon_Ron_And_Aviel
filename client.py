from socket import *
import struct
import time 
import msvcrt

client_udp = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP) # UDP

# Enable port reusage so we will be able to run multiple client_udps and servers on single (host, port). 
# Do not use socket.SO_REUSEADDR except you using linux(kernel<3.9): goto https://stackoverflow.com/questions/14388706/how-do-so-reuseaddr-and-so-reuseport-differ for more information.
# For linux hosts all sockets that want to share the same address and port combination must belong to processes that share the same effective user ID!
# So, on linux(kernel>=3.9) you have to run multiple servers and client_udps under one user to share the same (host, port).
# Thanks to @stevenreddie
# client_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

# Enable broadcasting mode
client_udp.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
print("client started, listening for offer requests...")
client_udp.bind(("", 13117))
while True:
    looking_server = True 
    connecting_to_tcp_server = True 
    game_mode = True  
    while looking_server:
        # Thanks @seym45 for a fix
        data, addr = client_udp.recvfrom(1024)
        client_udp.close()
        (ip, port) = addr
        content = struct.unpack('QQQ',data)
        print("Received offer from {} attempting to connect...".format(ip))# we have to check how we get the server ip 
        looking_server = False
    print("now  trying to connect the tcp server ")
    while connecting_to_tcp_server:
        with socket(AF_INET, SOCK_STREAM) as s:
            s.connect((ip, content[2]))
            s.sendall('Team A'.encode())
            data = s.recv(1024)
            print(data)
            while True:
                s.sendall(msvcrt.getch())
                connecting_to_tcp_server = False 
    while game_mode:
        x=0

         
     
