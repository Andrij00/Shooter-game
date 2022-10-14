from pygame import *
from random import randint

mixer.init()
mixer.music.load("space.mp3")
mixer.music.play()

fire_sound=mixer.Sound("fire.ogg")

img_back="galaxy.jpg"
img_rocket="rocket.png"
font.init()
font1 = font.SysFont("Arial",80)
win=font1.render("You win",True,(0,255,0))
lose =font1.render("You lose",True,(255,255,255))
font2 = font.SysFont("ARIAL",40)

score = 0 #скільки збито нло
goal = 10 #ціль гри - знищити 10 нло
lost = 0 #скільки пропустили нло
max_lost = 3 
life=3

class GameSprite(sprite.Sprite) :
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed) :
        sprite.Sprite.__init__(self) #super() . _init_()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset (self) :
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost-1
class Enemy1(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y<0:
            self.kill()
        
bullets=sprite.Group()
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy("ufo.png",randint(70,620),-40,70,50,randint(1,6))
    monsters.add(monster)
asteroids= sprite.Group()
for i in range(1,3):
    asteroid= Enemy1("asteroid.png",randint(80,620),-40,50,50,randint(1,3))
    asteroids.add(asteroid)

win_width = 700
win_height = 500
display.set_caption("Shooter")
window=display.set_mode((win_width,win_height))
background = transform.scale(image.load(img_back),(win_width,win_height))

ship=Player(img_rocket,5,400,60,80,12)
run=True
finish = False
rel_time = False#перезярядка
num_fire = 0 #кількість пострілів

from time import time as timer

while run:
    for e in event.get() :
        if e. type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire<5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()    
                    ship.fire()
                if num_fire >= 5 and rel_time ==False:
                    rel_time = True
                    last_time = timer()
    if not finish:
        window.blit(background,(0, 0))
        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        ship.reset()
        bullets.draw(window)

        if rel_time==True:
            now_time =timer()
            if now_time -last_time<3:
                reload = font2.render("Wait...reload",1,(150,0,0))
                window.blit(reload, (260,460))
            else:
                num_fire=0
                rel_time=False
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score =  score + 1
            monster = Enemy("ufo.png",randint(80,620),-40,80,50,randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship,monsters,False)or sprite.spritecollide(ship,asteroids,False):
            sprite.spritecollide(ship,monsters,True)
            sprite.spritecollide(ship,asteroids,True)
            life = life -1
        if life == 0 or lost>= max_lost:
            finish = True
            window.blit(lose, (200,200))    
        if score>=goal:
            finish = True
            window.blit(win,(200,200))

        if life == 3:
            color_life = (0, 150, 0)
        if life == 2:
            color_life = (100, 50, 0)
        if life == 1:
            color_life = (150, 0, 0)
        
        text_life = font1.render("life"+str(life), 1, color_life)
        window.blit(text_life, (550, 10))
        text_lose = font2.render("Пропушено: "+str(lost), 1, (255, 255, 255))
        window.blit (text_lose, (10,50))

        display.update()
    else:
        score = 0
        lost = 0
        num_fire=0
        life = 3
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(1,6):
            monster=Enemy(img_enemy,randint(80,520),-40,80,50,randint(1,5))
            monsters.add(monster)
        for i in range(1,3):
            ateroid=Enemy1("asteroid.png",randint(80,520),-40, 80, se, randint(1,5))
            asteroids.add(asteroid)
    time.delay(50)