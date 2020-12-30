
from socket import *
import time
import struct
import threading
import random

group_one = []
group_two = []
tcp_connections = []
all_teams=["teamron","teamivri","teamdanzi","teamADi"]
ip_address = gethostbyname(gethostname())

server_tcp_port = 12000
#initialize udp 
server_udp = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
server_udp.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
server_udp.setblocking(False)

#initialize tcp
multi_connections_tcp = socket();
multi_connections_tcp.bind((ip_address, server_tcp_port));


def UDP_Broadcast():    
    start_time = time.time()
    while time.time()- start_time < 10:
        message = struct.pack('QQQ',0xfeedbeef ,0x2,server_tcp_port)
        server_udp.sendto(message, ('<broadcast>', 13117))
        time.sleep(1)

def tcp_connection_reciver():
    start_time = time.time()
    while time.time()- start_time < 10:
        multi_connections_tcp.listen()
        client = multi_connections_tcp.accept()
        tcp_connections.append(client)
        conn, addr = client
        all_teams.append(conn.recv(1024).decode())
        
def send_message_to_all_clients():
    grp1=",".join(group_one)
    grp2=",".join(group_two)
    msg ="game rules are:ron is the king group 1:" + grp1 + "  group 2 : " + grp2
    print(msg)
    for conn in tcp_connections:
        conn[0].sendall(msg.encode())

def convert_list_to_string(group):
    res = ""
    for team in group:
        res += "," + team
    return res


def divide_teams_to_groups():
    
    random.shuffle(all_teams)
    cut = int(len(all_teams)/2)
    global group_one
    group_one += all_teams[:cut]
    global group_two
    group_two += all_teams[cut:]

def reset_info():
    global all_teams
    all_teams=[]
    global tcp_connections
    tcp_connections = []
    global group_one
    group_one = []
    global group_two
    group_two = []
        
def main():
    ip_address = gethostbyname(gethostname())
    print("Server started,listening on IP address {}".format(ip_address))
    while True:
        start_time = time.time()
        waiting_for_clients = True
        game_mode = True
        #waiting for client stage
        while time.time()-start_time < 10:
            if waiting_for_clients:
                thread1 = threading.Thread(target=UDP_Broadcast,args=())
                thread1.start()
                thread2 = threading.Thread(target=tcp_connection_reciver,args=())
                thread2.start()
                waiting_for_clients = False
            else:
                waiting_for_clients = True
                waiting_for_clients = False
        #game_mode stage
        divide_teams_to_groups() 
        start_time=time.time()
        while time.time() - start_time < 10:
            if game_mode:
                print("now starting game mode")
                send_message_to_all_clients()
                game_mode= False
            else:
                game_mode= True
                game_mode= False 
        print("game mode over  begin again ")
        reset_info()

       
        

if __name__ == "__main__":
    main()