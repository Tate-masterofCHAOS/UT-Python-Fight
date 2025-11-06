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

player = Player(800-32, 600-32)
battle_box = pygame.Rect(300, 200, 1000, 800)

def main():
    running = True
    while running:
        screen.fill((0,0,0))
        #Loops
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False

        player.player_set()
        screen.blit(pygame.Surface(battle_box.size), battle_box.topleft)

        
        player.update(keys, battle_box.get_rect())

        
        pygame.display.flip

main()











#https://www.google.com/search?q=how+to+make+a+rectangle+with+an+object+inside+that+cant+get+out+the+rectangle+pygame&rlz=1CAJIKU_enUS1187&oq=how+to+make+a+rectangle+with+an+object+inside+that+cant+get+out+the+rectangle+pygame&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCTIwODM3ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8&safe=active&ssui=on
#Code to clamp soul inside recangle