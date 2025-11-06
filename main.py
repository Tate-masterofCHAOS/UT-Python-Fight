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
battle_box = pygame.Rect(300, 600, 1000, 400)
Fight_btn = pygame.image.load(r'resources\Fight_btn.png')   
fight = Button(310, 1050, Fight_btn, .305)
Act_btn = pygame.image.load(r'resources\Act_btn.png')   
act = Button(560, 1050, Act_btn, .42)
Item_btn = pygame.image.load(r'resources\Item_btn.png')   
item = Button(810, 1050, Item_btn, .42)
mercy_btn = pygame.image.load(r'resources\Mercy_btn.png')   
mercy = Button(1060, 1050, mercy_btn  , .42)
WHITE = (255, 255, 255)
move_area = pygame.Rect(300+10, 600+10, 1000-20, 400-20)

speed = 4

def main():
    running = True
    while running:
        screen.fill((0,0,0))
        pygame.draw.rect(screen, WHITE, battle_box, 10)
        #Loops
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False



        keys = pygame.key.get_pressed()
        # reset velocities each frame
        player.changex = 0
        player.changey = 0
        if keys[pygame.K_LEFT]:
            player.changex = -speed
        elif keys[pygame.K_RIGHT]:
            player.changex = speed
        if keys[pygame.K_UP]:
            player.changey = -speed
        elif keys[pygame.K_DOWN]:
            player.changey = speed

        player.update(move_area)
        player.player_set()
        fight.draw()
        act.draw()
        item.draw()
        mercy.draw()
        pygame.display.flip()
        
        
        

        
        pygame.display.flip()

main()











#https://www.google.com/search?q=how+to+make+a+rectangle+with+an+object+inside+that+cant+get+out+the+rectangle+pygame&rlz=1CAJIKU_enUS1187&oq=how+to+make+a+rectangle+with+an+object+inside+that+cant+get+out+the+rectangle+pygame&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCTIwODM3ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8&safe=active&ssui=on
#Code to clamp soul inside recangle