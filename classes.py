
import pygame
from pygame import mixer
import random
import time

pygame.init()
 
screen = pygame.display.set_mode((1600,1200))
pygame.display.set_caption("UT-Fight")
pygame_icon = pygame.image.load(r'resources\soul.png')
pygame.display.set_icon(pygame_icon)

#Parent class for bullet(projectiles)
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


#Child class for a specific type of bullet
active_bullets = []

class Bullet_type_A(Bullet):
    def __init__(self, sprite, scale, x_pos, y_pos, x_change, y_change):
        super().__init__(sprite, scale, x_pos, y_pos, x_change, y_change)
        self.frame1 = pygame.image.load(r'resources/attack_1_frame_1.png').convert_alpha()
        self.frame2 = pygame.image.load(r'resources/attack_1_frame_2.png').convert_alpha()
        self.scale = scale
        self.frame = self.frame1
        self.transformed = pygame.transform.scale(self.frame, self.scale)
        self.x_pos = random.randint(300, 1300) if x_pos == 0 else x_pos
        self.y_pos = 400 if y_pos == 0 else y_pos
        self.x_change = x_change
        self.y_change = y_change if y_change != 0 else 5
        self.rect = self.transformed.get_rect(topleft=(int(self.x_pos), int(self.y_pos)))
        self._anim_toggle = False

    def move(self):
        self.x_pos += self.x_change
        self.y_pos += self.y_change
        self.rect.topleft = (int(self.x_pos), int(self.y_pos))
        # toggle animation each frame (no sleep)
        self._anim_toggle = not self._anim_toggle
        self.frame = self.frame2 if self._anim_toggle else self.frame1
        self.transformed = pygame.transform.scale(self.frame, self.scale)

    def create(self):
        screen.blit(self.transformed, (int(self.x_pos), int(self.y_pos)))
        surf = pygame.display.get_surface()
        if surf:
             surf.blit(self.transformed, (int(self.x_pos), int(self.y_pos)))
        surf = pygame.display.get_surface()
        if surf:
            surf.blit(self.transformed, (int(self.x_pos), int(self.y_pos)))

    def hit(self, player):
        if self.rect.colliderect(player.rect):
            player.health -= random.randint(1, 10)
            return True
        return False
        
class Bullet_type_B(Bullet):
    def __init__(self, sprite, scale, x_pos, y_pos, x_change, y_change):
        super().__init__(sprite, scale, x_pos, y_pos, x_change, y_change)
        self.frame1 = pygame.image.load(r'resources/attack_1_frame_1.png').convert_alpha()
        self.frame1 = pygame.transform.rotate(self.frame1, 90)
        self.frame2 = pygame.image.load(r'resources/attack_1_frame_2.png').convert_alpha()
        self.frame2 = pygame.transform.rotate(self.frame2, 90)
        self.scale = scale
        self.frame = self.frame1
        self.transformed = pygame.transform.scale(self.frame, self.scale)
        self.x_pos = 200 if x_pos == 0 else x_pos
        self.y_pos = random.randint(600, 1000) if y_pos == 0 else y_pos
        self.x_change = x_change if x_change != 0 else 5
        self.y_change = y_change 
        self.rect = self.transformed.get_rect(topleft=(int(self.x_pos), int(self.y_pos)))
        self._anim_toggle = False

    def move(self):
        self.x_pos += self.x_change
        self.y_pos += self.y_change
        self.rect.topleft = (int(self.x_pos), int(self.y_pos))
        # toggle animation each frame (no sleep)
        self._anim_toggle = not self._anim_toggle
        self.frame = self.frame2 if self._anim_toggle else self.frame1
        self.transformed = pygame.transform.scale(self.frame, self.scale)

    def create(self):
        screen.blit(self.transformed, (int(self.x_pos), int(self.y_pos)))
        surf = pygame.display.get_surface()
        if surf:
             surf.blit(self.transformed, (int(self.x_pos), int(self.y_pos)))
        surf = pygame.display.get_surface()
        if surf:
            surf.blit(self.transformed, (int(self.x_pos), int(self.y_pos)))

    def hit(self, player):
        if self.rect.colliderect(player.rect):
            player.health -= random.randint(1, 10)
            return True
        return False


#Parent class for attacks
class Attack:
    def __init__(self, length):
        self.length = length

    def perform_attack(self):
        pass

#Child class for a specific type of attack
class Attack_type_A(Attack):
    def __init__(self, length, spawn_interval=0.1):
        super().__init__(length)
        self.length = length
        self.spawn_interval = spawn_interval  # seconds between spawns
        self.running = False
        self.start_time = 0.0
        self.last_spawn = 0.0

    def perform_attack(self):
        # start the timed attack (non-blocking)
        self.running = True
        self.start_time = time.time()
        self.last_spawn = 0.0


    def update(self):
        # call this each frame from main loop
        if not self.running:
            return
        now = time.time()
        # stop when duration elapsed
        if now - self.start_time >= self.length:
            self.running = False
            return
        # spawn bullets at spawn_interval
        if self.last_spawn == 0.0 or (now - self.last_spawn) >= self.spawn_interval:
            a = Bullet_type_A(None, (50, 50), 0, 0, 0, 1)
            active_bullets.append(a)
            self.last_spawn = now

# update/draw bullets each frame; call from main loop
def update_bullets(boundary_rect, player):
    # get the current display/screen rect so we only remove bullets that left the screen
    surf = pygame.display.get_surface()
    if surf:
        screen_rect = surf.get_rect()
    else:
        # fallback: large rect covering expected window size
        screen_rect = pygame.Rect(0, 0, 1600, 1200)

    for b in active_bullets[:]:
        b.move()
        # remove bullets that have left the screen entirely
        if not screen_rect.colliderect(b.rect):
            try:
                active_bullets.remove(b)
            except ValueError:
                pass
            continue

        # draw and check collision against the player (still use boundary_rect if desired for hits)
        b.create()
        if b.hit(player):
            try:
                active_bullets.remove(b)
            except ValueError:
                pass
        

#Parent class for enemies
class Enemy:
    def __init__(self, health):
        self.health = health
        self.max_health = health
        self.attacks = []

#Class for the player, specifically the soul that appears during fights
class Player_soul:
    def __init__(self, x=800-32, y=600-32, changex=0, changey=0):
        img = pygame.image.load(r'resources/soul.png')
        self.img = pygame.transform.scale(img, (64, 64))  # Scale the image to fit the screen 
        self.x = x
        self.y = y
        self.changex = changex
        self.changey = changey
        self.rect = self.img.get_rect(topleft=(x, y))
        self.health = 92
        self.max_health = 92

    def update(self, boundary_rect):
            self.x += self.changex
            self.y += self.changey
            self.rect.topleft = (self.x, self.y)

            self.rect.clamp_ip(boundary_rect)

            # ensure position variables match the clamped rect
            self.x, self.y = self.rect.topleft

    def player_set(self):
         screen.blit(self.img, (self.x, self.y))
         surf = pygame.display.get_surface()
         if surf:
             surf.blit(self.img, (int(self.x), int(self.y)))

#Class for buttons
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