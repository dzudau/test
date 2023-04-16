from pygame import *
import pygame
from random import randint

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
bullet_speed =0
lost=0
score = 0
ammo = 10
font.init()
font1 = font.Font(None, 70)
font2 = font.Font(None, 70)
lose = font1.render('you lose', True, (0, 255, 0))
win = font1.render('you win', True, (0, 255, 0))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (55, 55))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        global bullet_speed
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15,)
        bullet_speed += 1
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
        

win_width = 700
win_height = 500
surface = display.set_mode((win_width, win_height))
display.set_caption('kusmas')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

game = True
finish = False
clock = time.Clock()
FPS = 60

all_sprites = pygame.sprite.Group()
ship = Player('rocket.png', 65, 400, 10)

monsters = sprite.Group()
for i in range(1,6):
    m = Enemy('ufo.png', randint(80, win_width-80), 40, randint(1,2))
    monsters.add(m)

monsters1 = sprite.Group()
for i in range(1,4):
    m2 = Enemy('asteroid.png', randint(80, win_width-80), -40, randint(1,2))
    monsters1.add(m2)

bullets = sprite.Group()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire.play()
                ship.fire()
                

    if finish != True:
        text = font2.render('МОНСТРЫ: '+ str(score),1,(255,255,255))
        
        surface.blit(background,(0,0))
        surface.blit(text, (10, 10))
        ship.update()
        bullets.update()
        monsters.update()
        monsters1.update()
        ship.reset()
        monsters.draw(surface)
        monsters1.draw(surface)
        bullets.draw(surface)

    sprites_list = sprite.groupcollide(monsters, bullets, True, True)
    for item in sprites_list:
        score = score + 1
        m = Enemy('ufo.png', randint(80, win_width-80), 40, randint(1,2))
        all_sprites.add(m)
        monsters.add(m)

    if score >= 10:
        finish = True
        surface.blit(win, (200, 200))

    display.update()
    clock.tick(FPS)