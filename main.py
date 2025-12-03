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
player2 = Player_soul("Red")
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




RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (156, 0, 156)



SPEED = 1
direction = 'down'
direction2 = "down"


def main():
    global direction
    enemy_image = pygame.image.load(r'resources\327f38c6-409c-4cf8-a435-13d70c4b87f7.png')
    enemy_image = pygame.transform.scale(enemy_image, (350,350))
    running = True
    player.health = player.max_health
    player_turn = True
    direction = 'down'
    attack0 = Attack_type_NULL(8.3)
    attack1 = Attack_type_A(8.2)
    attack2 = Attack_type_B(8.1)
    attack3 = Attack_type_C(7.9)
    attack4 = Attack_type_D(8.3)

    attack5 = Attack_type_E(8.15)
    attack6 = Attack_type_F(8.45)
    attack7 = Attack_type_G(8.15)
    attack8 = Attack_type_H(8.15)
    attack9 = Attack_type_I(8.3)
    attack10 = Attack_type_J(9.5)

    attack11 = Attack_type_K(13.5)
    attack12 = Attack_type_L(8.3)
    attack13 = Attack_type_M(8.3)
    attack14 = Attack_type_O(7.9)

    attack15 = Attack_type_N(8.2)

    attack_wait = Attack_type_NULL(15.3)
    attack_wait_2 = Attack_type_NULL(0)
    attack_wait_3 = Attack_type_NULL(0)

    attack16 = Attack_type_A(8)
    attack17 = Attack_type_B(8)
    attack18 = Attack_type_C(6)
    attack19 = Attack_type_D(4)

    attack20 = Attack_type_E(8)
    attack21 = Attack_type_F(8.5)
    attack22 = Attack_type_G(10)
    attack23 = Attack_type_H(10)
    attack24 = Attack_type_I(10)
    attack25 = Attack_type_J(10)

    attack26 = Attack_type_K(10)
    attack27 = Attack_type_L(10)
    attack28 = Attack_type_M(10)
    attack29 = Attack_type_O(10)

    attack30 = Attack_type_N(10)
    attacks = [attack1, attack2, attack3, attack4]
    started = {"attack0": False, "attack1": False, "attack2": False, "attack3": False, "attack4": False, "attack5": False, "attack6": False, "attack7": False, "attack8": False, "attack9": False, "attack10": False, "attack11": False, "attack12": False, "attack13": False, "attack14": False, "attack15": False, "attack_wait": False, "attack_wait_2": True, "attack_wait_3": True, "attack16": False, "attack17": False, "attack18": False, "attack19": False, "attack20": False, "attack21": False, "attack22": False, "attack23": False, "attack24": False, "attack25": False, "attack26": False, "attack27": False, "attack28": False, "attack29": False, "attack30": False}
    current_attack = "attack0"

    
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
                if event.key == pygame.K_SPACE:
                    if player.soul_mode == "Red":
                        player.soul_mode = "Red_M"
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
        elif player.soul_mode == "Red_M":
            player2.soul_mode = "Cyan_M"
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
            if player2.soul_mode == "Cyan_M":
                if keys[pygame.K_a]:
                    player2.changex = -SPEED * 1.5
                elif keys[pygame.K_d]:
                    player2.changex = SPEED * 1.5
                elif keys[pygame.K_w]:
                    player2.changey = -SPEED * 1.5
                elif keys[pygame.K_s]:
                    player2.changey = SPEED * 1.5
                else:
                    player2.changey =0  # gravity effect
                    player2.changex =0  # air resistance
            

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


        if current_attack == "attack0":
            if not started["attack0"]:
                play_bgm_battle()
                attack0.perform_attack()
                started["attack0"] = True   
                
        elif current_attack == "attack1":
            if not started["attack1"]:
                attack1.perform_attack()
                started["attack1"] = True
        elif current_attack == "attack2":
            if not started["attack2"]:
                attack2.perform_attack()
                started["attack2"] = True
        elif current_attack == "attack3":
            if not started["attack3"]:
                attack3.perform_attack()
                started["attack3"] = True
        elif current_attack == "attack4":
            if not started["attack4"]:
                attack4.perform_attack()
                started["attack4"] = True
        elif current_attack == "attack5":
            if not started["attack5"]:
                attack5.perform_attack()
                started["attack5"] = True
        elif current_attack == "attack6":
            if not started["attack6"]:
                attack6.perform_attack()
                started["attack6"] = True
        elif current_attack == "attack7":
            if not started["attack7"]:
                attack7.perform_attack()
                started["attack7"] = True
        elif current_attack == "attack8":
            if not started["attack8"]:
                attack8.perform_attack()
                started["attack8"] = True
        elif current_attack == "attack9":
            if not started["attack9"]:
                attack9.perform_attack()
                started["attack9"] = True
        elif current_attack == "attack10":
            if not started["attack10"]:
                attack10.perform_attack()
                started["attack10"] = True
        elif current_attack == "attack11":
            if not started["attack11"]:
                attack11.perform_attack()
                started["attack11"] = True
        elif current_attack == "attack12":
            if not started["attack12"]:
                attack12.perform_attack()
                started["attack12"] = True
        elif current_attack == "attack13":
            if not started["attack13"]:
                attack13.perform_attack()
                started["attack13"] = True
        elif current_attack == "attack14":
            if not started["attack14"]:
                attack14.perform_attack()
                started["attack14"] = True
        elif current_attack == "attack15":
            if not started["attack15"]:
                attack15.perform_attack()
                started["attack15"] = True
        elif current_attack == "attack_wait":
            if not started["attack_wait"]:
                attack_wait.perform_attack()
                started["attack_wait"] = True
        elif current_attack == "attack_wait_2":
            if not started["attack_wait_2"]:
                mixer.music.stop()
                play_bgm_battle2()
                attack_wait_2.perform_attack()
                started["attack_wait_2"] = True
        elif current_attack == "attack_wait_3":
            if not started["attack_wait_3"]:
                player.soul_mode = "Orange"
                enemy_image = pygame.image.load(r'resources\ff644481-c0b2-40d9-84a1-d47a51d3bcf4.png')
                enemy_image = pygame.transform.scale(enemy_image, (350,350))
                player.health = player.max_health
                attack_wait_3.perform_attack()
                started["attack_wait_3"] = True
        elif current_attack == "attack16":
            if not started["attack16"]:
                attack16.perform_attack()
                started["attack16"] = True
        elif current_attack == "attack17":
            if not started["attack17"]:
                player.soul_mode = "Orange"
                attack17.perform_attack()
                started["attack17"] = True
        elif current_attack == "attack18":
            if not started["attack18"]:
                player.soul_mode = "Orange"
                attack18.perform_attack()
                started["attack18"] = True
        elif current_attack == "attack19":
            if not started["attack19"]:
                player.soul_mode = "Orange"
                attack19.perform_attack()
                started["attack19"] = True
        elif current_attack == "attack20":
            if not started["attack20"]:
                player.soul_mode = "Orange"
                attack20.perform_attack()
                started["attack20"] = True
        elif current_attack == "attack21":
            if not started["attack21"]:
                player.soul_mode = "Orange"
                attack21.perform_attack()
                started["attack21"] = True
        elif current_attack == "attack22":
            if not started["attack22"]:
                player.soul_mode = "Orange"
                attack22.perform_attack()
                started["attack22"] = True
        elif current_attack == "attack23":
            if not started["attack23"]:
                player.soul_mode = "Orange"
                attack23.perform_attack()
                started["attack23"] = True
        elif current_attack == "attack24":
            if not started["attack24"]:
                player.soul_mode = "Orange"
                attack24.perform_attack()
                started["attack24"] = True
        elif current_attack == "attack25":
            if not started["attack25"]:
                player.soul_mode = "Orange"
                attack25.perform_attack()
                started["attack25"] = True
        elif current_attack == "attack26":
            if not started["attack26"]:
                player.soul_mode = "Orange"
                attack26.perform_attack()
                started["attack26"] = True
        elif current_attack == "attack27":
            if not started["attack27"]:
                player.soul_mode = "Orange"
                attack27.perform_attack()
                started["attack27"] = True
        elif current_attack == "attack28":
            if not started["attack28"]:
                player.soul_mode = "Orange"
                attack28.perform_attack()
                started["attack28"] = True
        elif current_attack == "attack29":
            if not started["attack29"]:
                player.soul_mode = "Orange"
                attack29.perform_attack()
                started["attack29"] = True
        elif current_attack == "attack30":
            if not started["attack30"]:
                player.soul_mode = "Orange"
                attack30.perform_attack()
                started["attack30"] = True


        player.update(move_area)
        player.player_set()
        if player2.soul_mode == "Cyan_M":
            player2.update(move_area)
            player2.player_set()
        

        cur = None
        if current_attack == "attack0":
            cur = attack0
        elif current_attack == "attack1":
            cur = attack1
        elif current_attack == "attack2":
            cur = attack2
        elif current_attack == "attack3":
            cur = attack3
        elif current_attack == "attack4":
            cur = attack4
        elif current_attack == "attack5":
            cur = attack5
        elif current_attack == "attack6":
            cur = attack6
        elif current_attack == "attack7":
            cur = attack7
        elif current_attack == "attack8":
            cur = attack8
        elif current_attack == "attack9":
            cur = attack9
        elif current_attack == "attack10":
            cur = attack10
        elif current_attack == "attack11":
            cur = attack11
        elif current_attack == "attack12":
            cur = attack12
        elif current_attack == "attack13":
            cur = attack13
        elif current_attack == "attack14":
            cur = attack14
        elif current_attack == "attack15":
            cur = attack15
        elif current_attack == "attack_wait":
            cur = attack_wait
        elif current_attack == "attack_wait_2":
            cur = attack_wait_2
        elif current_attack == "attack_wait_3":
            cur = attack_wait_3
        elif current_attack == "attack16":
            cur = attack16
        elif current_attack == "attack17":
            cur = attack17
        elif current_attack == "attack18":
            cur = attack18
        elif current_attack == "attack19":
            cur = attack19
        elif current_attack == "attack20":
            cur = attack20
        elif current_attack == "attack21":
            cur = attack21
        elif current_attack == "attack22":
            cur = attack22
        elif current_attack == "attack23":
            cur = attack23
        elif current_attack == "attack24":
            cur = attack24
        elif current_attack == "attack25":
            cur = attack25
        elif current_attack == "attack26":
            cur = attack26
        elif current_attack == "attack27":
            cur = attack27
        elif current_attack == "attack28":
            cur = attack28
        elif current_attack == "attack29":
            cur = attack29
        elif current_attack == "attack30":
            cur = attack30

        if cur is not None:
            finished = (cur.update() == False)
            if finished:
                # advance sequence
                if current_attack == "attack0":
                    current_attack = "attack1"
                elif current_attack == "attack1":
                    current_attack = "attack2"
                elif current_attack == "attack2":
                    current_attack = "attack3"
                elif current_attack == "attack3":
                    current_attack = "attack4"
                elif current_attack == "attack4":
                    current_attack = "attack5"
                elif current_attack == "attack5":
                    current_attack = "attack6"
                elif current_attack == "attack6":
                    current_attack = "attack7"
                elif current_attack == "attack7":
                    current_attack = "attack8"
                elif current_attack == "attack8":
                    current_attack = "attack9"
                elif current_attack == "attack9":
                    current_attack = "attack10"
                elif current_attack == "attack10":
                    current_attack = "attack11"
                elif current_attack == "attack11":
                    current_attack = "attack12"
                elif current_attack == "attack12":
                    current_attack = "attack13"
                elif current_attack == "attack13":
                    current_attack = "attack14"
                elif current_attack == "attack14":
                    current_attack = "attack15"
                elif current_attack == "attack15":
                    current_attack = "attack_wait"
                elif current_attack == "attack_wait":
                    current_attack = "attack_wait_2"
                elif current_attack == "attack_wait_2":
                    current_attack = "attack_wait_3"
                elif current_attack == "attack_wait_3":
                    current_attack = "attack16"
                elif current_attack == "attack16":
                    current_attack = "attack17"
                elif current_attack == "attack17":
                    current_attack = "attack18"
                elif current_attack == "attack18":
                    current_attack = "attack19"
                elif current_attack == "attack19":
                    current_attack = "attack20"
                elif current_attack == "attack20":
                    current_attack = "attack21"
                elif current_attack == "attack21":
                    current_attack = "attack22"
                elif current_attack == "attack22":
                    current_attack = "attack23"
                elif current_attack == "attack23":
                    current_attack = "attack24"
                elif current_attack == "attack24":
                    current_attack = "attack25"
                elif current_attack == "attack25":
                    current_attack = "attack26"
                elif current_attack == "attack26":
                    current_attack = "attack27"
                elif current_attack == "attack27":
                    current_attack = "attack28"
                elif current_attack == "attack28":
                    current_attack = "attack29"
                elif current_attack == "attack29":
                    current_attack = "attack30"
        
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
1 Y
2 Y
3 Y
4 Y
12 Y
13 Y
14 Y
23 Y
24 Y
34 Y
123 Y
124 Y
134 Y
234 Y
1234 Y
total: 15
"""

"""
Orange
1 Y
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
