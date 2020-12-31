
from socket import *
import time
import struct
import threading
import random
"""[global variables]
    summary: server that teams register to him and then split them to 2 groups and then calculate each group clicks on keyboard
varibales:
    [group_one]: [for group number one - list of tuples that contains (teams name,(connection with client , port of client) ]
    [group_two]: [for group number two - list of tuples that contains (teams name,(connection with client , port of client) ]
    [all_teams]: [for all the teams in the game - list of tuples that contains (teams name,(connection with client , port of client) ]
    [dicts_score_count]: [dict of counters for all the click made by all the teams]
    [multi_connections_tcp]: [socket that define the tcp connection]
    [server_tcp_port]: [contains the tcp socket port]
    [ip address]: [contains the server ip ]
    [time_limit]: [contains the time limit for each stage of the server ]
"""
group_one = []
group_two = []
all_teams=[]
ip_address = gethostbyname(gethostname())
dicts_score_count = {}
time_limit = 10
server_tcp_port = 12000
#initialize tcp
try:
    multi_connections_tcp = socket();
    multi_connections_tcp.bind((ip_address, server_tcp_port))
except:
    pass

def initial_tcp():
    """[initial the tcp socket we use this function when the game is ending and we are getting ready to another game]
    """
    global multi_connections_tcp
    try:
        multi_connections_tcp = socket();
        multi_connections_tcp.bind((ip_address, server_tcp_port))
    except:
        pass

def UDP_Broadcast(start_time):
    """[initial the broadcast message and the udp server and closing the socket after reach to the time limit]

    Args:
        start_time ([time]): [contains the start time of the first stage of the server]
    Varibales:
        [server_udp]: [ccontains the udp socket  ]
        [message]: [contains the message  with the pack like the instuctions ]

    """
    #initialize udp
    global time_limit
    try: 
        server_udp = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        server_udp.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)    
        while time.time()- start_time < time_limit:
            message = struct.pack('QQQ',0xfeedbeef ,0x2,server_tcp_port)
            server_udp.sendto(message, ('<broadcast>', 13117))
            time.sleep(1)
        server_udp.close()
    except:
        pass

def tcp_connection_reciver(start_time):
    """[summary]
    this function getting connection requests from clients and then establish the connection 
    after that 
    for each client she`s openining thread and waiting to recive a message - the message that contains the team name

    Args:
         start_time ([time]): [contains the start time of the first stage of the server]
    Varibales:
        [threads]: [contains all the threads that was created  ]
        [client_thread]: [contains the thread that created and then start it  ]
    """
    global time_limit
    threads = []
    while time.time() - start_time < time_limit:
        try:
            multi_connections_tcp.listen()
            client = multi_connections_tcp.accept()
       # maybe insert accept to the thread , to accept simultionasly multiple connections.
            client_thread = threading.Thread(target=accept_team_name,args=(client,start_time,))
            threads.append(client_thread)
            client_thread.start()
        except:
            pass
    # for t in threads:
    #     if t.is_alive:
    #         t.join()


def accept_team_name(client,timer):
    """[summary]
        this function  get client and timer  and then wait for message from the client
    Args:
        client ([type]): [tuple that contant the client connection and address]
        timer ([type]): [get the time to live of this thread ]
    Varibales:
        [conn]: [getting the connection  ]
        [addr]: [contains the thread that created and then start it  ]
    """
    global time_limit
    try:
        while time.time()- timer < time_limit:
            conn, addr = client
            all_teams.append((conn.recv(1024).decode(),client))
    except:
        pass

def send_message_to_all_clients():
    """[summary]
    this function generate the message of the begining of the game. and then send it  to all of the teams
    Varibales:
        [msg]: [message content   ]
    """
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

def divide_teams_to_groups():
    """[summary]
    this function making random shufle to all of the teams  and then cut the list to a half.
    half of the team go to group one 
    and the rest of them to group two.
    Varibales:
        [cut]: [contains all the threads that was created  ]
        
    """
    global all_teams
    random.shuffle(all_teams)
    cut = int(len(all_teams)/2)
    global group_one
    group_one += all_teams[:cut]
    global group_two
    group_two += all_teams[cut:]

def reset_info():
    """[summary]
    this function reset all the info of the games that over.
    and setting all global variables to be ready for another round.
    """
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
    """[summary]
    this is the main function of the script
    there is infinite while that running 
    in this while there is 2 whiles that run with time limit that representing  each mode  like  the advice of the instructions
    waiting for client stage - collecting connection and teams name
    game mode stage - randomize the teams and split them to two groups and then starting the game 
    Varibales:
        [start_time]: [the begin of the server time  ]
        [waiting_for_clients]: [indicate if we are in the waiting for clients mode  ]
        [game_mode]: [indicate if we are in the waiting for game mode  ]
        [threadtcp]: [tcp server in thread]
        [threadudp]: [broadcast  server in thread ]
        [msg]: [contains the result of the games that has to be print to the screen and send to the clients  ]
    """
    global time_limit
    ip_address = gethostbyname(gethostname())
    print("Server started,listening on IP address {}".format(ip_address))
    while True:
        start_time = time.time()
        waiting_for_clients = True
        game_mode = True
        #waiting for client stage
        while time.time()-start_time < time_limit:
            if waiting_for_clients:
                try:
                    udpthread= threading.Thread(target=UDP_Broadcast,args=(start_time,))
                    tcpthread=threading.Thread(target=tcp_connection_reciver,args=(start_time,))
                    udpthread.start()
                    tcpthread.start()
                except:
                    pass 
                waiting_for_clients = False
        if len(all_teams) is not 0:
        #game_mode stage
            #remmmeber to close the threads
            divide_teams_to_groups()
            send_message_to_all_clients()
            start_time=time.time()
            while time.time() - start_time < time_limit:
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
            reset_info()   
        
        

def creating_end_game_msg():
    """[summary]
    making the end game message.
    getting the score of each group and then building the end_game message
    this function decide who is the winner or if this is atie and then everyone wins 
Varibales:
        [score_group_one]: [calculated score of group one   ]
        [score_group_two]: [calculated score of group two ]
    Returns:
        [string]: [end game message ]
    """
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
    """[summary]
    calculate the score for group one 
    Returns:
        [int]: [calculated score of group one ]
    """
    res = 0 
    global group_one
    global dicts_score_count
    for team in group_one:
        res += dicts_score_count[team]
    return res

def calculating_group_two_score():
    """[summary]
    calculate the score for group two
    Returns:
    [int]: [calculated score of group two ]
    """
    global group_two
    global dicts_score_count
    res = 0 
    for team in group_two:
        res += dicts_score_count[team]
    return res


def creating_dict_counts():
    """[summary]
    initial the counters dict  with key= team and zero= initial value
    """
    global dicts_score_count
    global all_teams
    for team in all_teams:
        dicts_score_count[team] = 0


def game_handler(start_time):
    #for each player i have to put thread and make it thread safe
    """[summary]
    this function collecting simultionasly  clicks of all the teams that clicking and save it to the counter dict
    not splited to group by now

    Args:
        start_time ([type]): [description]
        Varibales:
        [first_run]: [if that the first run of the while  ]
        [threads]: [collecting all of the threads this function  created]
        [client_thread]: [thread for each client(team)]

    """
    global time_limit
    threads = []
    creating_dict_counts()
    first_run = True
    global all_teams
    while time.time() - start_time < time_limit:
        if first_run:
            first_run= False
            for t in all_teams:
                try:
                    client_thread=threading.Thread(target=client_score,args=(t,))
                    threads.append(client_thread)
                    client_thread.start()
                except:
                    pass

def client_score(team):
    """[summary]
    this function get the tuple and waiting for messages from the client once message has recived she update the counter 
    in the dict counter and waiting to another message 

    Args:
        team ([type]): [tuple that contain team name and connection and address of the client ]
    """
    global dicts_score_count
    while True:
        try:
            team[1][0].recv(1024)
            if team in dicts_score_count:
                dicts_score_count[team]+=1
        except:
            pass

if __name__ == "__main__":
    main()