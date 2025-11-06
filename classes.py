
import pygame

pygame.init()

screen = pygame.display.set_mode((1600,1200))
pygame.display.set_caption("UT-Fight")
pygame_icon = pygame.image.load(r'resources\soul.png')
pygame.display.set_icon(pygame_icon)


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


class Attack:
    def __init__(self, length):
        self.length = length

    def perform_attack(self):
        pass

class Enemy:
    def __init__(self, health):
        self.health = health

    def move(self):
        pass

class Player:
    def __init__(self, change=0):
        img = pygame.image.load(r'resources/soul.png')
        self.img = pygame.transform.scale(img, (64, 64))  # Scale the image to fit the screen 
        self.x = 800-32
        self.y = 600-32
        self.change = change
        self.score = 0

    def player_set(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.change
        self.y += self.change

#Take button class from space invaders