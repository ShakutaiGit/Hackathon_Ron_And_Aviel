from socket import *
import struct
import time 
import msvcrt

def Looking_For_Server():
    """This function represents the state of connecting to a UDP socket and getting the TCP port

    Returns:
        [ip]: [ip of tcp server]
        [tcp_port]: [port of tcp server]
    """
    try:
        # Enable broadcasting mode
        broadcast_port=13117
        client_udp = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP) #UDP socket intiallize
        client_udp.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        client_udp.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        client_udp.bind(("", broadcast_port))
        looking_for_server=True
        while looking_for_server: #Entering looking for server mode
            data, addr = client_udp.recvfrom(1024)
            client_udp.close() #closing the udp connection after getting a reply
            (ip, port) = addr
            message = struct.unpack('QQQ',data)  #Unpacking the message
            print("Received offer from {} attempting to connect...".format(ip))
            tcp_port=message[2]
            looking_for_server = False
        return tcp_port,ip
    except:
        pass

def TCP_Connection(tcp_port,ip):
    """This function connects to the TCP server and sends keyboard hits back to him

    Args:
        tcp_port (int): [port of the TCP server]
        ip (int): [ip of the TCP server]
    """
    try:
        connecting_to_tcp_server = True 
        while connecting_to_tcp_server: #Starting the TCP Connection
            with socket(AF_INET, SOCK_STREAM) as s:
                s.connect((ip, tcp_port)) 
                s.sendall('Fingers Of Doom'.encode()) #Sending Team name
                data = s.recv(1024).decode()
                time_limit=10
                print(data)
                start_time = time.time()
                while time.time()-start_time < time_limit: # getting the keyboard clicks and sends this to the server
                    if msvcrt.kbhit():
                        s.sendall(msvcrt.getch())
                connecting_to_tcp_server=False
                data = s.recv(1024).decode()
                print(data)
                s.close()
            print("Server disconnected, listening for offer requests...")
    except:
        pass
def main():
    print("client started, listening for offer requests...")
    while True:
        tcp_port,ip=Looking_For_Server()
        TCP_Connection(tcp_port,ip)

    

if __name__ == "__main__":
    main()

     
