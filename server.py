
from socket import *
import time
import struct


def UDP_Broadcast():
    server = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    server.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    print("Server started,listening on IP address {}".format(gethostbyname(gethostname())) )
    server.settimeout(0.2)
    message = struct.pack('QQQ',0xfeedbeef ,0x2,13000)
    while True:
        server.sendto(message, ('<broadcast>', 13117))
        time.sleep(1)
        
def main():
    UDP_Broadcast()

if __name__ == "__main__":
    main()