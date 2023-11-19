Object_SIZE = 50
import time
from Sprite import Sprite
class Character(Sprite):
    def __init__(self, x, y, speed, direction, name, x_range, y_range, reload,ult_reload, num, user, shot, ult, shot_damage, ult_damage):
        Sprite.__init__(self,x,y,speed,direction,name, x_range, y_range)
        self.Alive = True
        self.ready = False
        self.reload = reload
        self.last_shot_time = 0
        self.last_ult_time = 0
        self.ult_reload = ult_reload
        self.num = num
        self.hp = 100
        self.score = 0
        self.place = None
        self.user = user
        self.moving = False
        self.step_number = 1
        self.shot = shot
        self.ult = ult
        self.shot_damage = shot_damage
        self.ult_damage = ult_damage


    def shoot(self):
        self.last_shot_time = time.time()

    def shoot_ult(self):
        self.last_ult_time = time.time()


