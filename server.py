
from socket import *
import time
import struct
import threading
import random

group_one = []
group_two = []
all_teams=[]
ip_address = gethostbyname(gethostname())
dicts_score_count = {}
server_tcp_port = 12000

#initialize tcp
try:
    multi_connections_tcp = socket();
    multi_connections_tcp.bind((ip_address, server_tcp_port))
except:
    pass

def initial_tcp():
    global multi_connections_tcp
    try:
        multi_connections_tcp = socket();
        multi_connections_tcp.bind((ip_address, server_tcp_port))
    except:
        pass

def UDP_Broadcast(start_time):
    #initialize udp
    try: 
        server_udp = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        server_udp.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)    
        while time.time()- start_time < 10:
            message = struct.pack('QQQ',0xfeedbeef ,0x2,server_tcp_port)
            server_udp.sendto(message, ('<broadcast>', 13117))
            time.sleep(1)
        server_udp.close()
    except:
        pass

def tcp_connection_reciver(start_time):
    threads = []
    while time.time() - start_time < 10:
        try:
            multi_connections_tcp.listen()
            client = multi_connections_tcp.accept()
       # maybe insert accept to the thread , to accept simultionasly multiple connections.
            thread1 = threading.Thread(target=accept_team_name,args=(client,start_time,))
            threads.append(thread1)
            thread1.start()
        except:
            pass
    # for t in threads:
    #     if t.is_alive:
    #         t.join()


def accept_team_name(client,t):
    try:
        while time.time()- t < 10:
            conn, addr = client
            all_teams.append((conn.recv(1024).decode(),client))
    except:
        pass

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
        try:
            team[1][0].sendall(msg.encode())
        except:
            pass

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
    global dicts_score_count
    dicts_score_count.clear()
    global multi_connections_tcp
    try:
        multi_connections_tcp.close()
        initial_tcp()
    except:
        pass
        
def main():
    ip_address = gethostbyname(gethostname())
    print("Server started,listening on IP address {}".format(ip_address))
    while True:
        start_time = time.time()
        waiting_for_clients = True
        game_mode = True
        #waiting for client stage
        threads =[]
        while time.time()-start_time < 10:
            if waiting_for_clients:
                try:
                    x= threading.Thread(target=UDP_Broadcast,args=(start_time,))
                    y=threading.Thread(target=tcp_connection_reciver,args=(start_time,))
                    x.start()
                    y.start()
                except:
                    pass 
                waiting_for_clients = False
        if len(all_teams) is not 0:
        #game_mode stage
            #remmmeber to close the threads
            divide_teams_to_groups()
            send_message_to_all_clients()
            start_time=time.time()
            while time.time() - start_time < 10:
                if game_mode:
                    game_mode= False
                    try:
                        game_handler(start_time)
                    except:
                        pass                        

            msg= creating_end_game_msg()
            print(msg)
            for t in all_teams:
                try:
                    t[1][0].sendall(msg.encode())
                except:
                    pass
            # now score calculating
            print("Game over, sending out offer requests...")
            # for t in threads:
            #     if t.is_alive():
            #         t.join()
            reset_info()   
        
        

def creating_end_game_msg():
    global all_teams
    global group_one
    global group_two
    score_group_one = calculating_group_one_score()
    score_group_two = calculating_group_two_score()
    msg="Game over!\n" +"Group 1 typed in "+str(score_group_one)+" characters."+" Group 2 typed in "+str(score_group_two)+" characters.\n"
    if score_group_two > score_group_one:
        msg+="Group 2 is wins!\n"
        msg+=  "Congratulations to the winners:\n"+"==\n"
        for t in group_two:
            msg+= t[0]+"\n"
    elif score_group_one > score_group_two:
        msg+="Group 1 is wins!\n"
        msg+=  "Congratulations to the winners:\n" +"==\n"
        for t in group_one:
            msg+= t[0]+"\n"
    else:
        msg+="its a Tie!\n"
        msg+=  "Congratulations to the winners:\n"+"==\n"
        for t in all_teams:
            msg+= t[0]+"\n"
    return msg


def calculating_group_one_score():
    res = 0 
    global group_one
    global dicts_score_count
    for team in group_one:
        res += dicts_score_count[team]
    return res

def calculating_group_two_score():
    res = 0 
    global group_two
    global dicts_score_count
    for team in group_two:
        res += dicts_score_count[team]
    return res


def creating_dict_counts():
    global dicts_score_count
    global all_teams
    for team in all_teams:
        dicts_score_count[team] = 0


def game_handler(start_time):
    #for each player i have to put thread and make it thread safe
    threads = []
    creating_dict_counts()
    flag = True
    global all_teams
    while time.time() - start_time < 10:
        if flag:
            flag= False
            for t in all_teams:
                try:
                    thread5=threading.Thread(target=client_score,args=(t,))
                    threads.append(thread5)
                    thread5.start()
                except:
                    pass

                
                
        # if t.is_alive:
        #     print("hey there i am alive ")


def client_score(team):
    global dicts_score_count
    while True:
        try:
            team[1][0].recv(1024)
        except:
            pass
        if team in dicts_score_count:
            dicts_score_count[team]+=1

if __name__ == "__main__":
    main()