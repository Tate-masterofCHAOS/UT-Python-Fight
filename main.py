import pygame
import random
import math
from classes import *
from pygame import mixer
from Basic_functions import *

pygame.init()

screen = pygame.display.set_mode((1600,1200))
pygame.display.set_caption("UT-Fight")
pygame_icon = pygame.image.load(r'resources\soul_red.png')
pygame.display.set_icon(pygame_icon)

player = Player_soul("Red")
battle_box_x = 300
battle_box_y = 600
battle_box_width = 1000
battle_box_height = 400
battle_box = pygame.Rect(300, 600, 1000, 400)

Fight_btn = pygame.image.load(r'resources\Fight_btn.png')   
fight = Button(320, 1070, Fight_btn, .305)
Act_btn = pygame.image.load(r'resources\Act_btn.png')   
act = Button(570, 1070, Act_btn, .42)
Item_btn = pygame.image.load(r'resources\Item_btn.png')   
item = Button(820, 1070, Item_btn, .42)
mercy_btn = pygame.image.load(r'resources\Mercy_btn.png')   
mercy = Button(1070, 1070, mercy_btn  , .42)
WHITE = (255, 255, 255)
move_area = pygame.Rect(battle_box_x+10, battle_box_y+10, battle_box_width-20, battle_box_height-20)

game_font = pygame.font.Font(r'resources\DeterminationMonoWebRegular.ttf', 50)
game_over_font = pygame.font.Font(r'resources\DeterminationMonoWebRegular.ttf', 100)
enemy_image = pygame.image.load(r'resources\327f38c6-409c-4cf8-a435-13d70c4b87f7.png')
enemy_image = pygame.transform.scale(enemy_image, (350,350))



RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (156, 0, 156)



SPEED = 1
direction = 'down'


def main():
    global direction
    running = True
    player.health = player.max_health
    player_turn = True
    direction = 'down'
    attack1 = Attack_type_A(10)
    attack2 = Attack_type_B(10)
    attack3 = Attack_type_C(10)
    attack4 = Attack_type_D(10)

    while running:
        screen.fill((0,0,0))
        pygame.draw.rect(screen, WHITE, battle_box, 10)
        max_hp_bar = pygame.Rect(700, 1015, player.max_health * 2, 40)
        current_hp_bar = pygame.Rect(700, 1015, player.health * 2, 40)
        pygame.draw.rect(screen, RED, max_hp_bar)
        pygame.draw.rect(screen, YELLOW, current_hp_bar)

        hp_display = game_font.render(f"{player.health}/{player.max_health}", True, (255, 255, 255))
        screen.blit(hp_display, (900, 1008))
        screen.blit(enemy_image, (600, 200))
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # spawn attack on keydown so perform_attack isn't called every frame
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    attack1.perform_attack()
                if event.key == pygame.K_2:
                    attack2.perform_attack()
                if event.key == pygame.K_3:
                    attack3.perform_attack()
                if event.key == pygame.K_4:
                    attack4.perform_attack()
                if event.key == pygame.K_SPACE:
                    if player.soul_mode == "Red":
                        player.soul_mode = "Orange"
                        player.player_set()
                    elif player.soul_mode == "Orange":
                        player.soul_mode = "Blue"
                        player.player_set()
                    elif player.soul_mode == "Blue":
                        player.soul_mode = "Purple"
                        player.player_set()
                    elif player.soul_mode == "Purple":
                        player.soul_mode = "Red"
                        player.player_set()

        keys = pygame.key.get_pressed()
        # reset velocities each frame
        player.changex = 0
        if player.soul_mode != "Blue":
            player.changey = 0

        if player.soul_mode == "Red":
            if keys[pygame.K_LEFT]:
                player.changex = -SPEED * 1.5
                direction = 'left'
            elif keys[pygame.K_RIGHT]:
                player.changex = SPEED * 1.5
                direction = 'right'
            if keys[pygame.K_UP]:
                player.changey = -SPEED * 1.5
                direction = 'up'
            elif keys[pygame.K_DOWN]:
                player.changey = SPEED * 1.5
                direction = 'down'

        elif player.soul_mode == "Orange":
            # continue moving in last direction unless a new key is pressed
            # set exactly one axis based on direction and clear the other axis
            if direction == 'left':
                player.changex = -SPEED
            elif direction == 'right':
                player.changex = SPEED
            elif direction == 'up':
                player.changey = -SPEED
            elif direction == 'down':
                player.changey = SPEED

            # update direction if the player presses a key (changes movement next frame)
            if keys[pygame.K_LEFT]:
                direction = 'left'
            elif keys[pygame.K_RIGHT]:
                direction = 'right'
            if keys[pygame.K_UP]:
                direction = 'up'
            elif keys[pygame.K_DOWN]:
                direction = 'down'

        #Blue soul movement: Gravity effect toward bottom of battle box
        elif player.soul_mode == "Blue":
            if keys[pygame.K_LEFT]:
                player.changex = -SPEED
                direction = 'left'
            elif keys[pygame.K_RIGHT]:
                player.changex = SPEED
                direction = 'right'
            if keys[pygame.K_UP]:
                player.changey = -SPEED
                direction = 'up'
            elif keys[pygame.K_DOWN]:
                player.changey = SPEED
                direction = 'down'

        elif player.soul_mode == "Purple":
            if keys[pygame.K_LEFT]:
                player.changex = -SPEED
                direction = 'left'
            elif keys[pygame.K_RIGHT]:
                player.changex = SPEED
                direction = 'right'
            if keys[pygame.K_UP]:
                player.changey = -SPEED
                direction = 'up'
            elif keys[pygame.K_DOWN]:
                player.changey = SPEED
                direction = 'down'
            
        if attack1.is_ended():
            attack2.perform_attack()
        elif attack2.is_ended():
            attack3.perform_attack()
        elif attack3.is_ended():
            attack3.perform_attack()
        elif attack3.is_ended():
            attack4.perform_attack()
        elif attack4.is_ended():
            attack1.perform_attack()
        else:
            attack1.perform_attack()
        player.update(move_area)
        player.player_set()

        attack1.update()
        attack2.update()
        attack3.update()
        attack4.update()
        # update and draw bullets from attacks (non-blocking)
        update_bullets(move_area, player)

        fight.draw()
        act.draw()
        item.draw()
        mercy.draw()

        if player.health <= 0:
            screen.fill((0,0,0))
            game_over_display = game_over_font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(game_over_display, (500, 200))
            game_font_display2 = game_font.render("You have been defeated...Stay Determined", True, (255, 255, 255))
            screen.blit(game_font_display2, (100, 400))
            pygame.display.flip()
            if keys[pygame.K_ESCAPE]:
                running = False
            if keys[pygame.K_RETURN]:
                #delete everything and reset
                attack1.clear()
                attack2.clear()
                attack3.clear()
                attack4.clear()
                player.health = player.max_health
                
                
                
        pygame.display.flip()
    
    pygame.quit()
        
        


main()

"""
Red
1
2
3
4
12
13
14
23
24
34
123
124
134
234
1234
total: 15
"""

"""
Orange
1
2
3
4
12
13
14
23
24
34
123
124
134
234
1234
total: 15
"""
