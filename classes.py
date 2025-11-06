
import pygame
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((1600,1200))
pygame.display.set_caption("UT-Fight")
pygame_icon = pygame.image.load(r'resources\soul.png')
pygame.display.set_icon(pygame_icon)

def select_sound():
    pygame.mixer.Sound(r'resources\select.wav').play()

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

class Bullet_type_A(Bullet):
    def __init__(self, sprite, scale, x_pos, y_pos, x_change, y_change):
        super().__init__(sprite, scale, x_pos, y_pos, x_change, y_change)

    def move(self):
        self.x_pos += self.x_change
        self.y_pos += self.y_change
    
    def create(self):
        screen.blit(self.sprite, (self.x_pos, self.y_pos))
    
    def hit(self):
        pass


class Attack:
    def __init__(self, length):
        self.length = length

    def perform_attack(self):
        pass

class Attack_type_A(Attack):
    def __init__(self, length):
        super().__init__(length)

    def perform_attack(self):
        pass


class Enemy:
    def __init__(self, health):
        self.health = health

    def move(self):
        pass

class Player:
    def __init__(self, x, y, changex=0, changey=0):
        img = pygame.image.load(r'resources/soul.png')
        self.img = pygame.transform.scale(img, (64, 64))  # Scale the image to fit the screen 
        self.x = x
        self.y = y
        self.changex = changex
        self.changey = changey
        self.rect = self.img.get_rect(topleft=(x, y))

    def update(self, boundary_rect):
            self.x += self.changex
            self.y += self.changey
            self.rect.topleft = (self.x, self.y)

            self.rect.clamp_ip(boundary_rect)

            # ensure position variables match the clamped rect
            self.x, self.y = self.rect.topleft

    def player_set(self):
        screen.blit(self.img, (self.x, self.y))

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