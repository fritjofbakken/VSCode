import pygame as p
from pygame.locals import *
import time
import random as r

p.init()
screen = p.display.set_mode((1400, 300))
clock = p.time.Clock()
storSmurf = p.image.load("smurf.png").convert()
storFogel = p.image.load("fogel.png").convert()
storGarga = p.image.load("garga.jpg").convert()
background = p.image.load("bakgrund.png").convert()
smurfSize = (80, 80)
gargaSize = (60, 75)
fogelSize = (80, 48)

black = (0, 0, 0)

smurf = p.transform.smoothscale(storSmurf, smurfSize)
garga = p.transform.smoothscale(storGarga, gargaSize)
fogel = p.transform.smoothscale(storFogel, fogelSize)
p.mixer.init()
p.font.init()
font = p.font.Font('C:\Windows\Fonts\comicbd.ttf', 20)
p.mixer.music.load("jump.mp3")
p.mixer.music.load("score.mp3") # Laddar in ett nytt ljud

p.mixer.Channel(1).set_volume(0.5) # Sänker volymen på score.mp3

p.display.set_caption('Smurf Run')

p.key.set_repeat(1)
speed = 300
gravity = 700



class Karaktär():
    def __init__(self, pos = p.Vector2(100, 0), vel = 0):
        self.pos = pos.xy
        self.vel = vel
        self.hitbox = Rect(self.pos.xy, smurfSize)
    def Jump(self):
        if self.vel < 0:
            self.vel += ((-(self.pos.y - 170))/40)*gravity*tick
        else:
            self.vel += 4*gravity*tick


        self.pos.y += self.vel*tick
        if self.pos.y >= 169:
            self.vel = 0
            self.pos.y = 169

        self.hitbox.topleft = self.pos.xy

        for event in p.event.get(): # Kollar på alla events och tar ut KEYDOWN events
            if event.type == p.KEYDOWN:
                if (event.key == K_SPACE or event.key == K_UP) and self.pos.y >= 169: # Kollar om specifikt space eller uppåtpilen är nedtryckt och hoppar som vanligt
                    self.vel = -700
                    #p.mixer.Channel(0).play(p.mixer.Sound("jump.mp3")) # Spelar jump.mp3 i channel 0 så jump.mp3 och score.mp3 kan spelas samtidigt
                if event.key == K_DOWN: # Om nedåtpilen är nedtryckt åker smurfen ner i marken snabbare så man kan överleva vid högre hastighet
                    self.vel = 1000

                 


class Hinder():
    def __init__(self, fogel, pos = p.Vector2(1400, -200), vel = 0):
        self.fogel = fogel
        self.pos = pos.xy
        self.vel = vel + speed
        self.alive = True
        self.hitbox = Rect(self.pos.xy, gargaSize)

    def Alive(self):
        self.vel += gravity*tick
        self.pos.y += self.vel*tick
        if self.fogel:
            self.pos.x -= speed*tick*(1 + 0.15*(speed/300))*0.9 # Gör så fogeln blir snabbare (jämfört med garga) vid större hastigheter
        else:
            self.pos.x -= speed*tick
        
        if self.pos.y >= 173 and not self.fogel:
            self.vel = 0
            self.pos.y = 173
        elif self.fogel:
            self.pos.y = 70
        
        if self.pos.x <= -100:
            self.alive = not self.alive

        self.hitbox.topleft = self.pos.xy

hinder = []
hinder.append(Hinder(True))
character = Karaktär()

frame = 0
rframe = r.randint(int(1200 - speed/2.5), 1500)/1000 # Finslipat värden
tick = 0
foreground = p.Surface((1400, 300))

score = 0
scoreAdd = font.render("+400", True, black)

while True:
    tick = clock.tick(100)/1000 

    if frame >= rframe:
        if r.randint(1, 3) == 1:
            hinder.append(Hinder(True))
        else:
            hinder.append(Hinder(False))
        frame = 0
        speed += 12
        rframe = r.randint(int(1300 - speed/2.5), 1500)/1000
        score = int(100*speed/3)
        scoreAdd.set_alpha(255) # Gör "+400"-texten synlig
        #p.mixer.Channel(1).play(p.mixer.Sound("score.mp3")) # Spelar score.mp3 i channel 1


    frame += tick

    character.Jump()
    screen.blit(background, (0, 0))
    screen.blit(smurf, character.pos.xy)

    for i in range(len(hinder) - 1):
        hinder[i].Alive()
        if hinder[i].fogel:
            screen.blit(fogel, hinder[i].pos.xy)
        else:
            screen.blit(garga, hinder[i].pos.xy)

        if (((character.hitbox.centerx - hinder[i].hitbox.centerx)**2 + (character.hitbox.centery - hinder[i].hitbox.centery)**2)**(1/2) <= 70 and not hinder[i].fogel) or (((character.hitbox.centerx - hinder[i].hitbox.centerx)**2 + (character.hitbox.centery - hinder[i].hitbox.centery)**2)**(1/2) <= 50 and hinder[i].fogel): # Fogeln har en mindre hitbox för att underlätta vid högre hastigheter
            p.quit()
        if not hinder[i].alive:
            hinder.pop(i)

    scoreText = font.render(f"{score}", True, black)
    
    screen.blit(scoreText, (700, 40))

    if (scoreAdd.get_alpha() >= 0):
        scoreAdd.set_alpha(scoreAdd.get_alpha()-3) # Fadear ut "+400"-texten
    screen.blit(scoreAdd, (800, 40))

    if (score%5000 <= 1000) and (score >= 15000): # Nu börjar spelet inte med epilepsianfall
        foreground.fill((r.randint(0, 255), r.randint(0, 255), r.randint(0, 255)))
        foreground.set_alpha(r.randint(200, 255))
        screen.blit(foreground, (0, 0))
        rframe *= 0.99 # Hinder spawnar snabbare vid epilepsianfall, den gångrar varje frame därför gångrar jag med väldigt lite

    p.display.update()

    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()