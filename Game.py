from Shot import Shot
import time
from Character import Character
import DBHandler

HEIGHT = 1080
WIDTH = 1920
MAX_HEIGHT = 3*HEIGHT
MAX_WIDTH = 3*WIDTH
class Game:
    def __init__(self):
        self.ShotList = []
        self.started = False
        self.full = False
        self.wait = 20
        self.players = {}
        self.amount = 0
        self.starting_amount = 0
        self.ended = False
        self.removed_list = []

    def add_player(self, user, cac):
        num = 1
        reload = 1
        ult_reload = 10
        cac_information = DBHandler.GetCharacter(cac)
        shot = cac_information[1]
        ult = cac_information[2]
        shot_damage = cac_information[3]
        ult_damage = cac_information[4]
        while num in self.players:
            num += 1
        if num==1:
            self.players[num] = Character(100,50,10,"DOWN", cac, WIDTH, HEIGHT, reload,ult_reload, num, user, shot, ult, shot_damage, ult_damage)
        elif num==2:
            self.players[num] = Character(WIDTH+100,50,10,"DOWN", cac, WIDTH*2, HEIGHT, reload,ult_reload, num, user, shot, ult, shot_damage, ult_damage)
        elif num==3:
            self.players[num] = Character(WIDTH*2+100,50,10,"DOWN", cac, WIDTH*3, HEIGHT, reload,ult_reload, num, user, shot, ult, shot_damage, ult_damage)
        elif num==4:
            self.players[num] = Character(100,HEIGHT+50,10,"DOWN", cac, WIDTH, HEIGHT*2, reload,ult_reload, num, user, shot, ult, shot_damage, ult_damage)
        elif num==5:
            self.players[num] = Character(WIDTH+100,HEIGHT+50,10,"DOWN", cac, WIDTH*2, HEIGHT*2, reload,ult_reload, num, user, shot, ult, shot_damage, ult_damage)
        elif num==6:
            self.players[num] = Character(WIDTH*2+100,HEIGHT+50,10,"DOWN", cac, WIDTH*3, HEIGHT*2, reload,ult_reload, num, user, shot, ult, shot_damage, ult_damage)
        elif num==7:
            self.players[num] = Character(100,HEIGHT*2+50,10,"DOWN", cac, WIDTH, HEIGHT*3, reload,ult_reload, num, user, shot, ult, shot_damage, ult_damage)
        elif num==8:
            self.players[num] = Character(WIDTH+100,HEIGHT*2+50,10,"DOWN", cac, WIDTH*2, HEIGHT*3, reload,ult_reload, num, user, shot, ult, shot_damage, ult_damage)
        self.amount += 1
        self.starting_amount+=1
        if self.amount == 8:
            self.full = True
        return num


    def command(self, num, command):
        CHANGED = False
        player = self.players[num]
        if player.Alive:
            if command == "RIGHT" or command == "LEFT" or command == "UP" or command == "DOWN":
                player.set_direction(command)
                player.step_number = 1
                player.moving = True
                ''' player.Move()
                if player.x>=player.x_range:
                    player.x_range += WIDTH
                    CHANGED = True
                elif player.x<player.x_range-WIDTH:
                    player.x_range -= WIDTH
                    CHANGED = True
                if player.y >= player.y_range:
                    player.y_range += HEIGHT
                    CHANGED = True
                elif player.y < player.y_range - HEIGHT:
                    player.y_range -= HEIGHT
                    CHANGED = True'''
            elif command == "RELEASED":
                player.moving = False
                player.step_number = 1
            elif command ==  "SHOOT":
                if time.time()-player.last_shot_time>=player.reload:
                    shot = False
                    player.shoot()
                    shot_range = 100
                    shot_direction = player.direction
                    if shot_direction == "RIGHT" and player.x<MAX_WIDTH-100:
                        shot_x = player.x + 100
                        shot_y = player.y
                        shot = True
                    elif shot_direction == "LEFT" and player.x>=50:
                        shot_x = player.x - 100
                        shot_y = player.y
                        shot = True
                    elif shot_direction == "UP" and player.y>=50:
                        shot_x = player.x
                        shot_y = player.y - 100
                        shot = True
                    elif shot_direction == "DOWN" and player.y<MAX_HEIGHT+100:
                        shot_x = player.x
                        shot_y = player.y + 100
                        shot = True
                    if shot:
                        self.ShotList.append(Shot(shot_x, shot_y, 20,  shot_direction, player.shot ,player.x_range, player.y_range, shot_range, num,player.shot_damage))
            elif command ==  "ULT":
                if time.time()-player.last_ult_time>=player.ult_reload:
                    shot = False
                    player.shoot_ult()
                    shot_range = 100
                    shot_direction = player.direction
                    if shot_direction == "RIGHT" and player.x<MAX_WIDTH-100:
                        shot_x = player.x + 100
                        shot_y = player.y
                        shot = True
                    elif shot_direction == "LEFT" and player.x>=50:
                        shot_x = player.x - 100
                        shot_y = player.y
                        shot = True
                    elif shot_direction == "UP" and player.y>=50:
                        shot_x = player.x
                        shot_y = player.y - 100
                        shot = True
                    elif shot_direction == "DOWN" and player.y<MAX_HEIGHT+100:
                        shot_x = player.x
                        shot_y = player.y + 100
                        shot = True
                    if shot:
                        self.ShotList.append(Shot(shot_x, shot_y, 20,  shot_direction, player.ult,player.x_range, player.y_range, shot_range, num, player.ult_damage))
        return CHANGED

    def get_player(self, num):
        return self.players[num]

    def move_shots(self):
        for shot in self.ShotList:
            moved = shot.Move()
            if shot.x>=shot.x_range:
                shot.x_range += WIDTH
            elif shot.x<shot.x_range-WIDTH:
                shot.x_range -= WIDTH
            if shot.y >= shot.y_range:
                shot.y_range += HEIGHT
            elif shot.y < shot.y_range - HEIGHT:
                shot.y_range -= HEIGHT
            shot.range -= 1
            for player in self.players.values():
                if player.Alive:
                    hit =  shot.check_hit(player)
                    if hit:
                        self.players[shot.shooter].score += 100
                        if player.hp<=0:
                            player.place = self.amount
                            player.Alive = False


            if not moved or shot.range==0:
                #self.players[shot.shooter].shot = False
                self.ShotList.remove(shot)


    def remove_player(self, num):
        if num in self.players:
            if self.started:
                self.removed_list.append(num)
            del self.players[num]
            self.amount -= 1
            if self.amount == 0:
                self.ShotList = []
                self.started = False
                self.full = False
                self.wait = 20
                self.players = {}
                self.amount = 0
                self.starting_amount = 0
                self.ended = False
                self.removed_list = []
            elif not self.started:
                self.starting_amount -= 1

            elif self.amount == 1:
                for player in self.players.values():
                    if player.Alive:
                        player.place = 1
                self.ended = True


