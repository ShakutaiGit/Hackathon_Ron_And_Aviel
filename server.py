
from socket import *
import time
import struct
import threading
import random


group_one = []
group_two = []
group_one_score = []
group_two_score = []
scores = []
group_one_counter = 0
group_two_counter = 0 
all_teams=[]
ip_address = gethostbyname(gethostname())

server_tcp_port = 12000
#initialize udp 
server_udp = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
server_udp.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

#initialize tcp
multi_connections_tcp = socket();
multi_connections_tcp.bind((ip_address, server_tcp_port))


def UDP_Broadcast(start_time):    
    while time.time()- start_time < 10:
        message = struct.pack('QQQ',0xfeedbeef ,0x2,server_tcp_port)
        server_udp.sendto(message, ('<broadcast>', 13117))
        time.sleep(1)

def tcp_connection_reciver(start_time):
    while time.time()- start_time < 10:
        multi_connections_tcp.listen()
        client = multi_connections_tcp.accept()
       # maybe insert accept to the thread , to accept simultionasly multiple connections.
        thread1 = threading.Thread(target=accept_team_name,args=(client,start_time,))
        thread1.start()


def accept_team_name(client,t):
    while time.time()- t < 10:
        conn, addr = client
        all_teams.append((conn.recv(1024).decode(),client))

def send_message_to_all_clients():
    msg = "Welcome to Clash of fingers.\n"
    msg += "Group 1:\n"+"==\n"
    for g in group_one:
        msg+= g[0]+"\n"
    msg += "Group 2:\n"+"==\n"
    for g in group_two:
        msg+= g[0]+"\n"
    msg+="\n"+"Start pressing keys on your keyboard as fast as you can!!"
    print(msg)
    for team in all_teams:
        team[1][0].sendall(msg.encode())

def convert_list_to_string(group):
    res = ""
    for team in group:
        res += "," + team
    return res


def divide_teams_to_groups():
    global all_teams
    random.shuffle(all_teams)
    cut = int(len(all_teams)/2)
    global group_one
    group_one += all_teams[:cut]
    global group_two
    group_two += all_teams[cut:]

def reset_info():
    global all_teams
    all_teams=[]
    global group_one
    group_one = []
    global group_two
    group_two = []
    global group_one_counter 
    group_one_counter = 0
    global group_two_counter
    group_two_counter = 0
        
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
                thread1 = threading.Thread(target=UDP_Broadcast,args=(start_time,))
                thread1.start()
                thread2 = threading.Thread(target=tcp_connection_reciver,args=(start_time,))
                thread2.start()
                waiting_for_clients = False
        if len(all_teams) is not 0:
        #game_mode stage
            divide_teams_to_groups()
            send_message_to_all_clients()
            start_time=time.time()
            while time.time() - start_time < 10:
                if game_mode:
                    game_mode= False
                    game_handler(start_time)
            msg="Game over!"
            print(group_one_score)
            # now score calculating 

                
        print("game mode over  begin again ")
        reset_info()

def game_handler(start_time):
    #for each player i have to put thread and make it thread safe
    
    x = threading.Thread(target=score_handler_group,args=(True,))
    y = threading.Thread(target=score_handler_group,args=(False,))
    x.start()
    y.start()
         
         
def score_handler_group(group_type):
    threads = []
    group=[]
    global group_one
    global group_two
    if group_type:
        group = group_one
    else:
        group = group_two
    for index,team in enumerate(group,0):
        threads[index] = threading.Thread(client_score,(team,index,group_type))
        threads[index].start()


def client_score(team,index):
    if group_type:
        global group_one_score
        group_one_score[index]=0
    else:
        global group_two_score
        group_two_score[index]=0
    while True:
        team[1][0].recv(1024)
        if group_type:
            group_one_score[index]+=1
        else:
            group_two_score[index]+=1
     

        

if __name__ == "__main__":
    main()