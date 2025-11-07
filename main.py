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

player = Player_soul()
battle_box_x = 300
battle_box_y = 600
battle_box_width = 1000
battle_box_height = 400
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
move_area = pygame.Rect(battle_box_x+10, battle_box_y+10, battle_box_width-20, battle_box_height-20)

attack1 = Attack_type_A(10)

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
        if keys[pygame.K_1]:
            attack1.perform_attack()


        player.update(move_area)
        player.player_set()
        fight.draw()
        act.draw()
        item.draw()
        mercy.draw()
        pygame.display.flip()
        
        
        

        
        pygame.display.flip()

main()











