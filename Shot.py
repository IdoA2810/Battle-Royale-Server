from Sprite import Sprite
class Shot(Sprite):
    def __init__(self, x, y, speed, direction, name, x_range, y_range, range, shooter, damage):
        Sprite.__init__(self,x,y,speed,direction,name, x_range, y_range)
        self.range = range
        self.shooter = shooter
        self.damage = damage

    def check_hit(self, player):
        if player.x - player.size <self.x<player.x + player.size and player.y - player.size <self.y<player.y + player.size:
            self.range = 0
            player.hp -= self.damage
            return True
        return False