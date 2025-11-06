import pygame
import random
import math
from classes import *
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((1600,1200))
pygame.display.set_caption("UT-Fight")
pygame_icon = pygame.image.load(r'resources\soul.png')
pygame.display.set_icon(pygame_icon)

player = Player()

def main():
    running = True
    while running:
        screen.fill((0,0,0))
        #Loops
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_LEFT]:
                    player.change = -0.3
                if keys[pygame.K_RIGHT]:
                    player.change = 0.3

        player.player_set

        
        pygame.display.flip

main()