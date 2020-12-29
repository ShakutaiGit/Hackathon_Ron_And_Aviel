from socket import *

def pyUDPServer():
    print( "begin the server" )
    serverPort = 2010
    severSocket = socket(AF_INET,SOCK_DGRAM)
    severSocket.bind(('',serverPort))
    print( "The server is ready to receive" )
    while 1:
        print( "wait for message" )
        messsage, clientAddress = severSocket.recvfrom(2010)
        print ("message: " + str(messsage, 'utf-8') ) # need to be translated back to str from bytes
        modifiedMessage = messsage.upper() # a func on the message
        print (modifiedMessage)
        severSocket.sendto(modifiedMessage,clientAddress)
        pass

def main():
    print("Hello World! this is the server!!")
    pyUDPServer()

if __name__ == "__main__":
    main()
