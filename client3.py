from socket import *
import struct
import time 
import msvcrt

def Looking_For_Server():
    client_udp = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP) #UDP socket intiallize
    client_udp.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    client_udp.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    client_udp.bind(("", 13117))
    looking_server=True
    while looking_server: #Entering looking for server mode
        data, addr = client_udp.recvfrom(1024)
        client_udp.close() #closing the udp connection after getting a reply
        (ip, port) = addr
        content = struct.unpack('QQQ',data)  #Unpacking the message
        print("Received offer from {} attempting to connect...".format(ip))
        looking_server = False
    return content,ip

def TCP_Connection(content,ip):
    connecting_to_tcp_server = True 
    while connecting_to_tcp_server: #Starting the TCP Connection
        with socket(AF_INET, SOCK_STREAM) as s:
            s.connect((ip, content[2]))
            s.sendall('Fingers Of Doom'.encode()) #Sending Team name
            data = s.recv(1024).decode()
            print(data)
            start_time = time.time()
            while time.time()-start_time < 10:
                if msvcrt.kbhit():
                    s.sendall(msvcrt.getch())
            connecting_to_tcp_server=False
            data = s.recv(1024).decode()
            print(data)
            s.close()
            print("Server disconnected, listening for offer requests...")
    
def main():
# Enable broadcasting mode
    print("client started, listening for offer requests...")
    while True:
        content,ip=Looking_For_Server()
        TCP_Connection(content,ip)

    

if __name__ == "__main__":
    main()

     
