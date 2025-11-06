
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
    def __init__(self, x, y, change=0):
        img = pygame.image.load(r'resources/soul.png')
        self.img = pygame.transform.scale(img, (64, 64))  # Scale the image to fit the screen 
        self.x = x
        self.y = y
        self.speed = 5

    def update(self, keys, boundary_rect):
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
            if keys[pygame.K_UP]:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed

            self.rect.clamp_ip(boundary_rect)

    def player_set(self):
        screen.blit(self.img, (self.x, self.y))

#Take button class from space invaders