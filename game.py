import pyxel
import math

WIDTH = 256
HEIGHT = 256

map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,1,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,2,0,1,0,0,0,1],
    [1,1,1,0,0,0,0,0,1,0,1,1,1],
    [1,0,0,1,1,1,1,1,1,0,1,0,1],
    [1,0,1,1,1,0,0,0,1,0,1,0,1],
    [1,0,1,0,0,0,1,0,1,0,1,0,1],
    [1,0,1,1,1,0,1,0,1,0,1,0,1],
    [1,0,0,0,1,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1]
]

class App:
    def __init__(self):
        pyxel.init(256, 256, caption="Global Game jame")
        self.player = Player(2, 2)
        self.camera = Camera(self.player)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()

    def draw(self):
        self.camera.draw()


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dirx = -1
        self.diry = 0.5
        self.planex = 0
        self.planey = 0.66
        self.movespeed = (1/60) * 8.0
        self.rotspeed = (1/20)

    def update(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            olddirx = self.dirx
            self.dirx = self.dirx * math.cos(-self.rotspeed) - self.diry * math.sin(-self.rotspeed)
            self.diry = olddirx * math.sin(-self.rotspeed) + self.diry * math.cos(-self.rotspeed)
            oldplanex = self.planex
            self.planex = self.planex * math.cos(-self.rotspeed) - self.planey * math.sin(-self.rotspeed)
            self.planey = oldplanex * math.sin(-self.rotspeed) + self.planey * math.cos(-self.rotspeed)
        if pyxel.btn(pyxel.KEY_LEFT):
            olddirx = self.dirx
            self.dirx = self.dirx * math.cos(self.rotspeed) - self.diry * math.sin(self.rotspeed)
            self.diry = olddirx * math.sin(self.rotspeed) + self.diry * math.cos(self.rotspeed)
            oldplanex = self.planex
            self.planex = self.planex * math.cos(self.rotspeed) - self.planey * math.sin(self.rotspeed)
            self.planey = oldplanex * math.sin(self.rotspeed) + self.planey * math.cos(self.rotspeed)

        if pyxel.btn(pyxel.KEY_UP):
            if map[math.floor(self.x + self.dirx + self.movespeed)][math.floor(self.y)] == 0 :
                self.x += self.dirx * self.movespeed
            if map[math.floor(self.x)][math.floor(self.y + self.diry * self.movespeed)] == 0:
                self.y += self.diry * self.movespeed

        if pyxel.btn(pyxel.KEY_DOWN):
            if map[math.floor(self.x - self.dirx + self.movespeed)][math.floor(self.y)] == 0 :
                self.x -= self.dirx * self.movespeed
            if map[math.floor(self.x)][math.floor(self.y - self.diry * self.movespeed)] == 0:
                self.y -= self.diry * self.movespeed


class Camera:
    def __init__(self, player) -> None:
        self.player = player
        self.drawdistance = 100


    def draw(self):
        for x in range(0, WIDTH-1): 
            camerax = 2 * x /WIDTH - 1
            raydirx = self.player.dirx + self.player.planex * camerax
            raydiry = self.player.diry + self.player.planey * camerax

            mapx = math.floor(self.player.x)
            mapy = math.floor(self.player.y)

            sidedistx = 0
            sidedisty = 0

            deltadistx = abs(1/raydirx)
            deltadisty = abs(1/raydiry)
            perpwalldist = 0

            stepx = 0
            stepy = 0

            hit = 0
            side = 0

            if raydirx < 0:
                stepx = -1
                sidedistx = (self.player.x - mapx) * deltadistx
            else:
                stepx = 1
                sidedistx = (mapx + 1.0 - self.player.x) * deltadistx
            if raydiry < 0:
                stepy = -1
                sidedisty = (self.player.y - mapy) * deltadisty
            else:
                stepy = 1
                sidedisty = (mapy + 1.0 - self.player.y) * deltadisty

            while hit == 0:
                if sidedistx < sidedisty:
                    sidedistx += deltadistx
                    mapx += stepx
                    side = 0
                else:
                    sidedisty += deltadisty
                    mapy += stepy
                    side = 1
                if map[mapx][mapy] > 0:
                    hit = 1
            
            if side == 0:
                perpwalldist = (mapx - self.player.x + (1-stepx)/2)/raydirx
            else:
                perpwalldist = (mapy - self.player.y + (1-stepy)/2)/raydiry
            
            if perpwalldist < self.drawdistance:
                lineheight = HEIGHT/perpwalldist

                drawstart = -lineheight/2 + HEIGHT/2
                if drawstart <= 0:
                    drawstart = 0
                
                drawend = lineheight/2 + HEIGHT/2
                if drawend >= HEIGHT:
                    drawend = HEIGHT
                
                color = 10
                if map[mapx][mapy] == 1:
                    color = 8
                    if side == 1 :
                        color = 15
                elif map[mapx][mapy] == 2:
                    color = 3
                    if side == 1:
                        color = 11
                elif map[mapx][mapy] == 3:
                    color = 1
                    if side == 1:
                        color = 12
                elif map[mapx][mapy] == 4:
                    color = 7
                    if side == 1:
                        color = 6
                
                pyxel.line(x, 0, x, drawstart, 5)
                pyxel.line(x, drawend, x ,HEIGHT, 4)
                pyxel.line(x, drawstart-1, x, drawend, color)
                # pyxel.text(5, 5, f"Y: {self.diry}", 9)


App()