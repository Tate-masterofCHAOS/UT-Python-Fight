import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((1600,1200))
pygame.display.set_caption("UT-Fight")
pygame_icon = pygame.image.load(r'resources\soul.png')
pygame.display.set_icon(pygame_icon)


def main():
    running = True
    while running:
        screen.fill((0,0,0))
        #Loops
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False

        
        pygame.display.flip

main()