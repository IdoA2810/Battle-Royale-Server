#Object_SIZE = 50
HEIGHT = 1080
WIDTH = 1920
MAX_HEIGHT = 3*HEIGHT
MAX_WIDTH = 3*WIDTH

class Sprite:
    def __init__(self, x, y, speed, direction, name, x_range, y_range):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed  = speed
        self.real_location = (x,y)
        self.name = name
        self.ready = False
        self.x_range = x_range
        self.y_range = y_range
        self.size = 50


    def set_real_location(self,x,y):
        self.real_location = (x,y)

    def get_image_index(self):
        return self.image_index
    def get_real_location(self):
        return self.real_location
    def get_pos(self):
        return self.x, self.y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_v(self):
        return self.speed

    def set_direction(self, direction):
        self.direction = direction

    def get_direction(self):
        return self.direction

    def LeftWall(self):
        return self.x == 0

    def RightWall(self, WIDTH):
        return self.x + self.size == WIDTH

    def TopWall(self):
        return self.y == 0

    def BottomWall(self, HEIGHT):
        return self.y + self.size == HEIGHT

    def PlayerFrom(self, Direction, OtherPlayer):
        if Direction == "RIGHT" and self.x + 50 == OtherPlayer.get_x() and self.y == OtherPlayer.get_y():
            return True
        if Direction == "LEFT" and self.x == OtherPlayer.get_x() + 50 and self.y == OtherPlayer.get_y():
            return True
        if Direction == "UP" and self.y == OtherPlayer.get_y() + 50 and self.x == OtherPlayer.get_x():
            return True
        if Direction == "DOWN" and self.y + 50 == OtherPlayer.get_y() and self.x == OtherPlayer.get_x():
            return True
        return False
    def Move(self):
        if self.direction == "LEFT":
            if self.x - self.speed >=0:
                self.x = self.x - self.speed
                return True
        elif self.direction == "RIGHT":
            if self.x + self.speed <= MAX_WIDTH - self.size*2:
                self.x = self.x + self.speed
                return True
        elif self.direction == "UP":
            if self.y - self.speed > 0:
                self.y = self.y - self.speed
                return True
        elif self.direction == "DOWN":
            if self.y + self.speed <= MAX_HEIGHT - self.size*2:
                self.y = self.y + self.speed
                return True
        return False

