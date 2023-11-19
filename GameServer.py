import socket
import time
import threading
import SizeOfSize
from Game import Game
import DBHandler
delay = 0.025
Game_list= []
Connected_Users = []
HEIGHT = 1080
WIDTH = 1920
#MOVED = True
locker = threading.Lock()
class ClientThread(threading.Thread):

    def __init__(self, ip, port, conn, tid):
        threading.Thread.__init__(self)
        print ("New thread started for "+ip+":"+str(port))
        self.ip = ip
        self.port = port
        self.conn = conn
        self.stid = str(tid)  # threading.current_thread().ident
        self.client_name = "unknown"
        self.Pnum = 0
        self.game = None
        self.CHANGED = True
        self.Screen_Width = 0
        self.Screen_Height = 0
        self.username = None
        self.cac = "KID"



    def run(self):
        #global MOVED
        global HEIGHT
        global WIDTH
        global WIDTH
        global HEIGHT
        cac_list = DBHandler.GetCharactersNames()
        self.conn.setblocking(1)
        data = SizeOfSize.recv_by_size(self.conn)
        print ("Received: " + data)
        connected = False
        while not connected:
            while self.Screen_Height == 0 or self.Screen_Width == 0:
                data = SizeOfSize.recv_by_size(self.conn)
                print ("Received: " + data)
                if data == "":
                    break
                if data.split("_")[0] == "SIZE":
                    self.Screen_Width = int(data.split("_")[1])
                    self.Screen_Height = int(data.split("_")[2])

            print ("WIDTH: " + str(self.Screen_Width))
            print ("HEIGHT: " + str(self.Screen_Height))

            data = SizeOfSize.recv_by_size(self.conn)
            print ("Received: " + data)
            if data == "":
                break

            if data.split("_")[0] == "LOGIN":
                if len(data.split("_"))==3:
                    result = DBHandler.Login(data.split("_")[1], data.split("_")[2])
                    if data.split("_")[1] in Connected_Users:
                        data = "ERROR_User already connected"
                        self.conn.send(data + "\n")
                    elif result == True:
                        self.username = data.split("_")[1]
                        locker.acquire()
                        Connected_Users.append(self.username)
                        locker.release()
                        self.conn.send("OK" + "\n")
                        connected = True
                    elif result == False:
                        data =  "ERROR_Username or password incorrect"
                        self.conn.send(data + "\n")
                else:
                    data = "ERROR_Username or password incorrect"
                    self.conn.send(data + "\n")
            elif data.split("_")[0] == "SIGN":
                all_fields = True
                if len(data.split("_"))==4:
                    for field in data.split("_"):
                        if len(field) == 0:
                            all_fields = False
                            break
                    if data.split("_")[2]==data.split("_")[3] and all_fields:
                        result = DBHandler.AddUser(data.split("_")[1], data.split("_")[2])
                        if result == "OK":
                            self.username = data.split("_")[1]
                            locker.acquire()
                            Connected_Users.append(self.username)
                            locker.release()
                            self.conn.send("OK" + "\n")
                            connected = True
                        elif result == "TAKEN":
                            data = "ERROR_Username already taken"
                            self.conn.send(data + "\n")
                        else:
                            data = "ERROR_Something went wrong"
                            self.conn.send(data + "\n")
                    elif not all_fields:
                        data = "ERROR_Please fill all fields"
                        self.conn.send(data + "\n")

                    else:
                        data = "ERROR_The password confirmation does not match"
                        self.conn.send(data + "\n")

                elif len(data.split("_"))<4:
                    data = "ERROR_Please fill all fields"
                    self.conn.send(data + "\n")
                else:
                    data = "ERROR_Please make sure your username and password do not include underscores"
                    self.conn.send(data + "\n")

                print ("Sent: " + data)
        if connected:
            print ("Connected")
            while True:
                found = False
                while not found:
                    self.conn.setblocking(1)
                    enter = False
                    while not enter:
                        data = SizeOfSize.recv_by_size(self.conn)
                        print ("Received: " + data)
                        if data == "":
                            break
                        elif data == "ENTER":
                            enter = True
                        elif data == "SELECT":
                            data = ""
                            cac_list = DBHandler.GetCharactersNames()
                            for cac in cac_list:
                                data+=cac+"_"
                            data = data[:-1]
                            self.conn.send(data + "\n")
                        elif data.split("_")[0] == "CHOOSE":
                            if data.split("_")[1] in cac_list:
                                self.cac = data.split("_")[1]

                    if data == "":
                        break
                    print ("ENTERED")

                    '''while height==0 and width==0:
                        data = self.conn.recv(1024)
                        if data.split("_")[0] == "HEIGHT":
                            height = int(data.split("_")[1])
                        if data.split("_")[2] == "WIDTH":
                            width = int(data.split("_")[3])'''


                    for g in Game_list:
                        if not g.started and not g.full:
                            locker.acquire()
                            self.Pnum = g.add_player(self.username, self.cac)
                            locker.release()
                            self.game = g
                            found = True
                            break
                    if not found:
                        self.game = Game()
                        locker.acquire()
                        Game_list.append(self.game)
                        self.Pnum = self.game.add_player(self.username, self.cac)
                        locker.release()
                        found = True
                    try:
                        self.conn.settimeout(1)
                        while found and not self.game.started:
                            data = "WAIT_" + str(self.game.wait) + "_" + str(self.game.amount) + "/8"
                            self.conn.send(data + "\n")
                            try:
                                data = SizeOfSize.recv_by_size(self.conn)
                                if data == "RETURN":
                                    locker.acquire()
                                    self.game.remove_player(self.Pnum)
                                    locker.release()
                                    found = False
                                    self.game = None
                            except socket.timeout:
                                pass
                            #print "Sent: " + data
                    except socket.error:
                        locker.acquire()
                        self.game.remove_player(self.Pnum)
                        locker.release()

                if self.game is None:
                    break

                try:
                    self.conn.setblocking(1)
                    self.conn.send("STARTED" + "\n")
                    print ("Sent Started")
                    thread1 = threading.Thread(target=self.get_command)
                    thread1.start()
                    thread2 = threading.Thread(target=self.move_character)
                    thread2.start()
                    factor_x = float(self.Screen_Width)/WIDTH
                    factor_y = float(self.Screen_Height)/HEIGHT
                    data = "FACTORS_" + str(factor_x) + "_" + str(factor_y)
                    self.conn.send(data + "\n")
                    print ("Sent " + data)
                    #MOVED = True

                    while self.Pnum in self.game.players and self.game.players[self.Pnum].Alive and not self.game.ended:
                        curr_time = time.time()
                        data = "AMOUNT_" + str(self.game.amount)
                        self.conn.send(data + "\n")
                        data = "POINTS_" + str(self.game.players[self.Pnum].score)
                        self.conn.send(data + "\n")
                        if self.CHANGED:
                            player = self.game.players[self.Pnum]
                            if player.x_range == WIDTH and player.y_range == HEIGHT:
                                background = "1,1"
                            elif player.x_range == 2*WIDTH and player.y_range == HEIGHT:
                                background = "1,2"
                            elif player.x_range == 3 * WIDTH and player.y_range == HEIGHT:
                                background = "1,3"
                            elif player.x_range == WIDTH and player.y_range == 2*HEIGHT:
                                background = "2,1"
                            elif player.x_range == 2 * WIDTH and player.y_range == 2*HEIGHT:
                                background = "2,2"
                            elif player.x_range == 3 * WIDTH and player.y_range == 2*HEIGHT:
                                background = "2,3"
                            elif player.x_range == WIDTH and player.y_range == 3 * HEIGHT:
                                background = "3,1"
                            elif player.x_range == 2 * WIDTH and player.y_range == 3 * HEIGHT:
                                background = "3,2"
                            else:
                                background = "3,3"
                            data = "BACK_" + background
                            self.conn.send(data + "\n")
                            print ("Sent: " + data)
                            self.CHANGED = False

                        #if MOVED:
                        player = self.game.players[self.Pnum]
                        for sprite in self.game.ShotList:
                            if sprite.x_range == player.x_range and sprite.y_range == player.y_range:
                                x = sprite.x
                                y = sprite.y
                                while x>=WIDTH:
                                    x-=WIDTH
                                while y>=HEIGHT:
                                    y-=HEIGHT
                                x = int(x * factor_x)
                                y = int(y * factor_y)
                                data = "SHOT_" + sprite.name + "_" + sprite.direction +"_" + str(x) + "_" + str(y)
                                self.conn.send(data+"\n")
                                #print "sent: " + data
                        for sprite in self.game.players.values():
                            if sprite.x_range == player.x_range and sprite.y_range == player.y_range:
                                x = sprite.x
                                y = sprite.y
                                while x>=WIDTH:
                                    x-=WIDTH
                                while y>=HEIGHT:
                                    y-=HEIGHT
                                x = int(x * factor_x)
                                y = int(y * factor_y)
                                data = "CAC_" + sprite.name + "_" + sprite.direction + "_" + str(x) + "_" + str(y) + "_" + \
                                       str(sprite.hp) + "_" +str(sprite.num) + "_" + sprite.user +"_" + str(sprite.moving) + "_" + str(sprite.step_number)
                            else:
                                data = "DEL_" + str(sprite.num)
                            self.conn.send(data + "\n")
                            #print "sent " + data
                        for player in self.game.removed_list:
                            data = "DEL_" + str(player)
                            self.conn.send(data + "\n")
                        while time.time() - curr_time < delay:
                            pass

                    if self.Pnum in self.game.players:
                        self.conn.send("END"+"\n")
                        score = self.game.players[self.Pnum].score + (self.game.starting_amount - self.game.players[self.Pnum].place)*1000
                        DBHandler.AddScore(self.username,score)
                        total_score = DBHandler.GetScore(self.username)
                        data = "SCORE_" + str(self.game.players[self.Pnum].place)+ "_" + str(score) + "_" + str(total_score)
                        self.conn.send(data + "\n")
                        print ("Sent: " + data)
                        locker.acquire()
                        self.game.remove_player(self.Pnum)
                        locker.release()
                    else:
                        break

                except socket.error:
                    locker.acquire()
                    self.game.remove_player(self.Pnum)
                    locker.release()
                    break




                    #MOVED = False
                #while time.time() - curr_time < delay:
                 #   pass
               # print "Finished one"
            locker.acquire()
            Connected_Users.remove(self.username)
            locker.release()
        self.conn.close()

    def move_character(self):
        while self.Pnum in self.game.players:
            try:
                player = self.game.get_player(self.Pnum)
                if player.moving:
                    curr_time = time.time()
                    if not player.Move():
                        player.moving = False
                    else:
                        if player.step_number==4:
                            player.step_number=1
                        else:
                            player.step_number += 1
                    if player.x>=player.x_range:
                        player.x_range += WIDTH
                        self.CHANGED = True
                    elif player.x<player.x_range-WIDTH:
                        player.x_range -= WIDTH
                        self.CHANGED = True
                    if player.y >= player.y_range:
                        player.y_range += HEIGHT
                        self.CHANGED = True
                    elif player.y < player.y_range - HEIGHT:
                        player.y_range -= HEIGHT
                        self.CHANGED = True
                    while time.time() - curr_time < delay:
                        pass
            except KeyError:
                break

    def get_command(self):
        # sock.settimeout(delay)
        #global MOVED
        data = "nothing"
        try:
            while data != "" and self.Pnum in self.game.players:
                # try:
                self.conn.settimeout(delay)
                curr_time = time.time()
                try:
                    data = SizeOfSize.recv_by_size(self.conn)
                    #print "Received: " + data
                    if data == "":
                        locker.acquire()
                        self.game.remove_player(self.Pnum)
                        locker.release()
                        break
                    else:
                        self.CHANGED = self.game.command(self.Pnum, data)
                    #MOVED = True
                    while time.time() - curr_time < delay:
                        pass
                except socket.timeout:
                    pass
        except socket.error:
            pass
        #self.game.remove_player(self.Pnum)
        #MOVED = True
        # except socket.timeout:
        #    pass


def games_starter():
    while True:
        curr_time = time.time()
        for game in Game_list:
            if game.amount == 8 and not game.started:
                game.started = True
                thread2 = threading.Thread(target=move_shots, args=(game,))
                thread2.start()
            elif not game.started and game.amount>1:
                game.wait -= 1
            if game.wait == 0 and not game.started:
                game.started = True
                thread2 = threading.Thread(target=move_shots, args=(game,))
                thread2.start()
        while time.time() - curr_time < 1:
            pass



def move_shots(game):
    #global MOVED
    while game.started:
        curr_time = time.time()
        if len(game.ShotList)>0:
            game.move_shots()
            #MOVED = True
        while time.time() - curr_time < delay:
            pass
def main():
    global client_socket
    srv_sock = socket.socket()
    ip = "0.0.0.0"
    port = 12345
    srv_sock.bind((ip, port))
    srv_sock.listen(10)
    threads = []
    tid = 0
    srv_sock.settimeout(600)
    thread = threading.Thread(target=games_starter)
    thread.start()
    while True:
        try:
            (conn, (ip, port)) = srv_sock.accept()
            print ("new client\n")
            tid += 1

            new_thread = ClientThread(ip, port, conn, tid)
            new_thread.start()
            threads.append(new_thread)

        except socket.timeout:
            break

    srv_sock.close()
    for new_thread in threads:  # iterates over the threads
        new_thread.join()       # waits until the thread has finished wor
if __name__ == '__main__':
    main()