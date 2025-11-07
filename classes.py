
import pygame
from pygame import mixer
import random
import time

pygame.init()

screen = pygame.display.set_mode((1600,1200))
pygame.display.set_caption("UT-Fight")
pygame_icon = pygame.image.load(r'resources\soul.png')
pygame.display.set_icon(pygame_icon)

#Parent class for bullet(projectiles)
class Bullet:
    def __init__(self, sprite, scale, x_pos, y_pos, x_change, y_change):
        self.sprite = sprite
        self.scale = scale
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_change = x_change
        self.y_change = y_change
    
    def move(self):
        pass

    def create(self):
        pass

    def hit(self):
        pass

#Child class for a specific type of bullet
class Bullet_type_A(Bullet):
    def __init__(self, sprite, scale, x_pos, y_pos, x_change, y_change):
        super().__init__(sprite, scale, x_pos, y_pos, x_change, y_change)
        self.sprite = pygame.image.load(r'resources/attack_1_frame_1.png')
        self.transformed_sprite = pygame.transform.scale(sprite, scale)
        self.x_pos = random.randint(300, 1300)
        self.y_pos = random.srandint(100, 500)
        self.x_change = 0
        self.y_change = 5
        self.rect = self.sprite.get_rect(topleft=(self.x_pos, self.y_pos))

    def move(self):
        self.x_pos += self.x_change
        self.y_pos += self.y_change
        if self.sprite == pygame.image.load(r'resources/attack_1_frame_1.png'):
            time.sleep(0.5)
            self.sprite = pygame.image.load(r'resources/attack_1_frame_2.png')
        else:
            time.sleep(0.5)
            self.sprite = pygame.image.load(r'resources/attack_1_frame_1.png')
    
    def create(self):
        screen.blit(self.sprite, (self.x_pos, self.y_pos))
    
    def hit(self, player):
        if self.rect.colliderect(player.rect, self.x_pos, self.y_pos, self.sprite.get_width(), self.sprite.get_height()):
            player.health -= random.randint(1, 10)  # Decrease player's health by 1 through ten on hit
        


#Parent class for attacks
class Attack:
    def __init__(self, length):
        self.length = length

    def perform_attack(self):
        pass

#Child class for a specific type of attack
class Attack_type_A(Attack):
    def __init__(self, length):
        super().__init__(length)
        self.length = length

    def perform_attack(self):
        start_time = time.time()
        while time.time() - start_time < self.length:
            # Logic for performing the attack
            for i in range(random.randint(1, 10)):
                bullet = Bullet_type_A(None, (50, 50), 0, 0, 0, 0)
                bullet.move()
                bullet.create()
                time.sleep(.3)  # Simulate time between bullet spawns
        

#Parent class for enemies
class Enemy:
    def __init__(self, health):
        self.health = health
        self.max_health = health
        self.attacks = []

#Class for the player, specifically the soul that appears during fights
class Player_soul:
    def __init__(self, x=800-32, y=600-32, changex=0, changey=0):
        img = pygame.image.load(r'resources/soul.png')
        self.img = pygame.transform.scale(img, (64, 64))  # Scale the image to fit the screen 
        self.x = x
        self.y = y
        self.changex = changex
        self.changey = changey
        self.rect = self.img.get_rect(topleft=(x, y))
        self.health = 92
        self.max_health = 92

    def update(self, boundary_rect):
            self.x += self.changex
            self.y += self.changey
            self.rect.topleft = (self.x, self.y)

            self.rect.clamp_ip(boundary_rect)

            # ensure position variables match the clamped rect
            self.x, self.y = self.rect.topleft

    def player_set(self):
        screen.blit(self.img, (self.x, self.y))

#Class for buttons
class Button:
    def __init__(self, x, y, img, scale):
        self.x = x
        self.y = y
        self.img = img
        width = img.get_width()
        height = img.get_height()
        self.img = pygame.transform.scale(img, (int(width * scale), int(height * scale)))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                action = True
                print("Clicked")
            else:
                action = False
                self.clicked = False
                
        screen.blit(self.img, (self.x, self.y))