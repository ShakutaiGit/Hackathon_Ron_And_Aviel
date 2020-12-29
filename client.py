from socket import *

def connect_to_server():
    print("in client function")
    serverPort=2010
    serverName= '192.168.14.6' #the IP you want to connect to
    clientSocket = socket(AF_INET,SOCK_DGRAM)
    message = b"HEY Tomer its ron and we connect server to client"
    clientSocket.sendto(message,(serverName,serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2055)
    print(modifiedMessage)
    clientSocket.close()


def main():
    print("client begin")
    connect_to_server()

if __name__ == "__main__":
    main()
