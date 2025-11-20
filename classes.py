
import pygame
from pygame import mixer
import random
import time
import math

pygame.init()
 
screen = pygame.display.set_mode((1600,1200))
pygame.display.set_caption("UT-Fight")
pygame_icon = pygame.image.load(r'resources\soul_red.png')
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
    def clear(self):
        self.active_bullets.clear()
        self.length = 0
        self.perform_attack()
        
class Bullet_type_B(Bullet):
    def __init__(self, sprite, scale, x_pos, y_pos, x_change, y_change):
        super().__init__(sprite, scale, x_pos, y_pos, x_change, y_change)
        self.frame1 = pygame.image.load(r'resources\attack_1_frame_1.png').convert_alpha()
        self.frame1 = pygame.transform.rotate(self.frame1, 0)
        self.frame2 = pygame.image.load(r'resources/attack_1_frame_2.png').convert_alpha()
        self.frame2 = pygame.transform.rotate(self.frame2, 0)
        self.scale = scale
        self.frame = self.frame1
        self.transformed = pygame.transform.scale(self.frame, self.scale)
        self.x_pos = 0 if x_pos == 0 else x_pos
        self.y_pos = 600 if y_pos == 0 else y_pos
        self.y_pos2 = 900 if y_pos == 0 else y_pos
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
    def clear(self):
        self.active_bullets.clear()
        self.length = 0
        self.perform_attack()
    
class Bullet_type_C(Bullet):
    def __init__(self, sprite, scale, x_pos, y_pos, x_change, y_change, delay=0.5, speed=6):
        super().__init__(sprite, scale, x_pos, y_pos, x_change, y_change)
        self.frame1 = pygame.image.load(r'resources/attack_1_frame_1.png').convert_alpha()
        self.frame2 = pygame.image.load(r'resources/attack_1_frame_2.png').convert_alpha()
        self.scale = scale
        self.frame = self.frame1
        self.transformed = pygame.transform.scale(self.frame, self.scale)
        # spawn position
        self.x_pos = random.randint(300, 1300) if x_pos == 0 else x_pos
        self.y_pos = 400 if y_pos == 0 else y_pos
        # velocity will be set after delay when targeting player
        self.x_change = 0
        self.y_change = 0
        self.rect = self.transformed.get_rect(topleft=(int(self.x_pos), int(self.y_pos)))
        self._anim_toggle = False
        # delayed start fields
        self.delay_seconds = delay
        self.speed = speed
        self.spawn_time = time.time()
        self.moving = False

    def move(self, player=None):
        # if not moving yet, check delay and lock target when delay passes
        if not self.moving:
            if (time.time() - self.spawn_time) >= self.delay_seconds:
                # compute direction toward player's current center (if provided)
                if player is not None:
                    # player center
                    px = player.x + (player.img.get_width() / 2)
                    py = player.y + (player.img.get_height() / 2)
                else:
                    # fallback target directly downward
                    px = self.x_pos
                    py = self.y_pos + 1
                # bullet center
                bx = self.x_pos + (self.transformed.get_width() / 2)
                by = self.y_pos + (self.transformed.get_height() / 2)
                dx = px - bx
                dy = py - by
                dist = math.hypot(dx, dy) or 1.0
                self.x_change = (dx / dist) * self.speed
                self.y_change = (dy / dist) * self.speed
                self.moving = True
        
        # update position (if moving or stationary)
        # update position (if moving or stationary)
        self.x_pos += self.x_change
        self.y_pos += self.y_change
        self.rect.topleft = (int(self.x_pos), int(self.y_pos))

        # toggle animation each frame (no sleep)
        self._anim_toggle = not self._anim_toggle
        self.frame = self.frame2 if self._anim_toggle else self.frame1
        self.transformed = pygame.transform.scale(self.frame, self.scale)

    def create(self):
        surf = pygame.display.get_surface()
        if surf:
            surf.blit(self.transformed, (int(self.x_pos), int(self.y_pos)))

    def hit(self, player):
        if self.rect.colliderect(player.rect):
            player.health -= random.randint(1, 10)
            return True
        return False
    def clear(self):
        self.active_bullets.clear()
        self.length = 0
        self.perform_attack()

class Bullet_type_D(Bullet):
    def __init__(self, sprite, scale, x_pos, y_pos, x_change, y_change):
        super().__init__(sprite, scale, x_pos, y_pos, x_change, y_change)
        self.frame1 = pygame.image.load(r'resources\attack_1_frame_1.png').convert_alpha()
        self.frame1 = pygame.transform.rotate(self.frame1, 0)
        self.frame2 = pygame.image.load(r'resources/attack_1_frame_2.png').convert_alpha()
        self.frame2 = pygame.transform.rotate(self.frame2, 0)
        self.scale = scale
        self.frame = self.frame1
        self.transformed = pygame.transform.scale(self.frame, self.scale)
        self.x_pos = 300 if x_pos == 0 else x_pos
        self.y_pos = 500 if y_pos == 0 else y_pos
        self.x_pos2 = 1250 if x_pos == 0 else x_pos
        self.x_change = x_change 
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
    def clear(self):
        self.active_bullets.clear()
        self.length = 0
        self.perform_attack()

#Parent class for attacks
class Attack:
    def __init__(self, length):
        self.length = length

    def perform_attack(self):
        pass

    

#Child class for a specific type of attack
class Attack_type_A(Attack):
    def __init__(self, length, spawn_interval=0.3):
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
            return False
        now = time.time()
        # stop when duration elapsed
        if now - self.start_time >= self.length:
            self.running = False
            return False
        # spawn bullets at spawn_interval
        if self.last_spawn == 0.0 or (now - self.last_spawn) >= self.spawn_interval:
            a = Bullet_type_A(None, (50, 50), 0, 0, 0, 1)
            active_bullets.append(a)
            self.last_spawn = now

        
    def clear(self):
        active_bullets.clear()
        self.length = 0
        self.perform_attack()

    def is_ended(self):
        if self.start_time >= self.length:
            return True
        else:
            return False

class Attack_type_B(Attack):
    def __init__(self, length, spawn_interval=0.5):
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
            return False
        now = time.time()
        # stop when duration elapsed
        if now - self.start_time >= self.length:
            self.running = False
            return False
        # spawn bullets at spawn_interval
        if self.last_spawn == 0.0 or (now - self.last_spawn) >= self.spawn_interval:
            a = Bullet_type_B(None, (100, 100), 0, 600, 1, 0)
            b = Bullet_type_B(None, (100, 100), 0, 925, 1, 0)
            active_bullets.append(a)
            active_bullets.append(b)
            self.last_spawn = now
    
    def clear(self):
        active_bullets.clear()
        self.length = 0
        self.perform_attack()

    def is_ended(self):
        if self.start_time >= self.length:
            return True
        else:
            return False

class Attack_type_C(Attack):
    def __init__(self, length, spawn_interval=0.5):
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
            return False
        now = time.time()
        # stop when duration elapsed
        if now - self.start_time >= self.length:
            self.running = False
            return False
        # spawn bullets at spawn_interval
        if self.last_spawn == 0.0 or (now - self.last_spawn) >= self.spawn_interval:
            a = Bullet_type_C(None, (50, 50), 0, 0, 0, 0, delay=1, speed=1)
            active_bullets.append(a)
            self.last_spawn = now
    
    def clear(self):
        active_bullets.clear()
        self.length = 0
        self.perform_attack()

    def is_ended(self):
        if self.start_time >= self.length:
            return True
        else:
            return False
   
class Attack_type_D(Attack):
    def __init__(self, length, spawn_interval=0.5):
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
            return False
        now = time.time()
        # stop when duration elapsed
        if now - self.start_time >= self.length:
            self.running = False
            return False
        # spawn bullets at spawn_interval
        if self.last_spawn == 0.0 or (now - self.last_spawn) >= self.spawn_interval:
            a = Bullet_type_D(None, (100, 100), 0, 0, 0, 1)
            b = Bullet_type_D(None, (100, 100), 1200, 0, 0, 1)
            active_bullets.append(a)
            active_bullets.append(b)
            self.last_spawn = now

    def clear(self):
        active_bullets.clear()
        self.length = 0
        self.perform_attack()

    def is_ended(self):
        if self.start_time >= self.length:
            return True
        else:
            return False
        
class Attack_type_E(Attack):
    def __init__(self, length, spawn_interval=0.5):
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
            return False
        now = time.time()
        # stop when duration elapsed
        if now - self.start_time >= self.length:
            self.running = False
            return False
        # spawn bullets at spawn_interval
        if self.last_spawn == 0.0 or (now - self.last_spawn) >= self.spawn_interval:
            a = Bullet_type_D(None, (100, 100), 0, 0, 0, 1)
            b = Bullet_type_D(None, (100, 100), 1200, 0, 0, 1)
            c = Bullet_type_B(None, (100, 100), 0, 600, 1, 0)
            e = Bullet_type_B(None, (100, 100), 0, 925, 1, 0)
            active_bullets.append(a)
            active_bullets.append(b)
            active_bullets.append(c)
            active_bullets.append(e)
            self.last_spawn = now

    def clear(self):
        active_bullets.clear()
        self.length = 0
        self.perform_attack()

    def is_ended(self):
        if self.start_time >= self.length:
            return True
        else:
            return False
        
class Attack_type_F(Attack):
    def __init__(self, length, spawn_interval=0.5):
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
            return False
        now = time.time()
        # stop when duration elapsed
        if now - self.start_time >= self.length:
            self.running = False
            return False
        # spawn bullets at spawn_interval
        if self.last_spawn == 0.0 or (now - self.last_spawn) >= self.spawn_interval:
            a = Bullet_type_C(None, (50, 50), 0, 0, 0, 0, delay=1, speed=1)
            b = Bullet_type_A(None, (50, 50), 0, 0, 0, 1)
            active_bullets.append(a)
            active_bullets.append(b)
            self.last_spawn = now
    
    def clear(self):
        active_bullets.clear()
        self.length = 0
        self.perform_attack()

    def is_ended(self):
        if self.start_time >= self.length:
            return True
        else:
            return False
        
class Attack_type_G(Attack):
    def __init__(self, length, spawn_interval=0.5):
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
            return False
        now = time.time()
        # stop when duration elapsed
        if now - self.start_time >= self.length:
            self.running = False
            return False
        # spawn bullets at spawn_interval
        if self.last_spawn == 0.0 or (now - self.last_spawn) >= self.spawn_interval:
            a = Bullet_type_D(None, (100, 100), 0, 0, 0, 1)
            b = Bullet_type_D(None, (100, 100), 1200, 0, 0, 1)
            c = Bullet_type_A(None, (50, 50), 0, 0, 0, 1)
            active_bullets.append(a)
            active_bullets.append(b)
            active_bullets.append(c)
            self.last_spawn = now

    def clear(self):
        active_bullets.clear()
        self.length = 0
        self.perform_attack()

    def is_ended(self):
        if self.start_time >= self.length:
            return True
        else:
            return False
        
class Attack_type_H(Attack):
    def __init__(self, length, spawn_interval=0.5):
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
            return False
        now = time.time()
        # stop when duration elapsed
        if now - self.start_time >= self.length:
            self.running = False
            return False
        # spawn bullets at spawn_interval
        if self.last_spawn == 0.0 or (now - self.last_spawn) >= self.spawn_interval:
            a = Bullet_type_C(None, (50, 50), 0, 0, 0, 0, delay=1, speed=1)
            c = Bullet_type_B(None, (100, 100), 0, 600, 1, 0)
            b = Bullet_type_B(None, (100, 100), 0, 925, 1, 0)
            active_bullets.append(a)
            active_bullets.append(b)
            active_bullets.append(c)
            self.last_spawn = now

    def clear(self):
        active_bullets.clear()
        self.length = 0
        self.perform_attack()

    def is_ended(self):
        if self.start_time >= self.length:
            return True
        else:
            return False

class Attack_type_I(Attack):
    def __init__(self, length, spawn_interval=0.5):
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
            return False
        now = time.time()
        # stop when duration elapsed
        if now - self.start_time >= self.length:
            self.running = False
            return False
        # spawn bullets at spawn_interval
        if self.last_spawn == 0.0 or (now - self.last_spawn) >= self.spawn_interval:
            a = Bullet_type_B(None, (100, 100), 0, 600, 1, 0)
            b = Bullet_type_B(None, (100, 100), 0, 925, 1, 0)
            c = Bullet_type_A(None, (50, 50), 0, 0, 0, 1)
            active_bullets.append(a)
            active_bullets.append(b)
            active_bullets.append(c)
            self.last_spawn = now
    
    def clear(self):
        active_bullets.clear()
        self.length = 0
        self.perform_attack()

    def is_ended(self):
        if self.start_time >= self.length:
            return True
        else:
            return False

class Attack_type_J(Attack):
    def __init__(self, length, spawn_interval=0.5):
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
            return False
        now = time.time()
        # stop when duration elapsed
        if now - self.start_time >= self.length:
            self.running = False
            return False
        # spawn bullets at spawn_interval
        if self.last_spawn == 0.0 or (now - self.last_spawn) >= self.spawn_interval:
            c = Bullet_type_C(None, (50, 50), 0, 0, 0, 0, delay=1, speed=1)
            a = Bullet_type_D(None, (100, 100), 0, 0, 0, 1)
            b = Bullet_type_D(None, (100, 100), 1200, 0, 0, 1)
            active_bullets.append(a)
            active_bullets.append(b)
            active_bullets.append(c)
            self.last_spawn = now
    
    def clear(self):
        active_bullets.clear()
        self.length = 0
        self.perform_attack()

    def is_ended(self):
        if self.start_time >= self.length:
            return True
        else:
            return False
        
class Attack_type_K(Attack):
    def __init__(self, length, spawn_interval=0.5):
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
            return False
        now = time.time()
        # stop when duration elapsed
        if now - self.start_time >= self.length:
            self.running = False
            return False
        # spawn bullets at spawn_interval
        if self.last_spawn == 0.0 or (now - self.last_spawn) >= self.spawn_interval:
            a = Bullet_type_B(None, (100, 100), 0, 600, 1, 0)
            b = Bullet_type_B(None, (100, 100), 0, 925, 1, 0)
            c = Bullet_type_A(None, (50, 50), 0, 0, 0, 1)
            d = Bullet_type_C(None, (50, 50), 0, 0, 0, 0, delay=1, speed=1)
            active_bullets.append(a)
            active_bullets.append(b)
            active_bullets.append(c)
            active_bullets.append(d)
            self.last_spawn = now
    
    def clear(self):
        active_bullets.clear()
        self.length = 0
        self.perform_attack()

    def is_ended(self):
        if self.start_time >= self.length:
            return True
        else:
            return False

class Attack_type_L(Attack):
    def __init__(self, length, spawn_interval=0.5):
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
            return False
        now = time.time()
        # stop when duration elapsed
        if now - self.start_time >= self.length:
            self.running = False
            return False
        # spawn bullets at spawn_interval
        if self.last_spawn == 0.0 or (now - self.last_spawn) >= self.spawn_interval:
            a = Bullet_type_B(None, (100, 100), 0, 600, 1, 0)
            b = Bullet_type_B(None, (100, 100), 0, 925, 1, 0)
            c = Bullet_type_A(None, (50, 50), 0, 0, 0, 1)
            d = Bullet_type_D(None, (100, 100), 0, 0, 0, 1)
            e = Bullet_type_D(None, (100, 100), 1200, 0, 0, 1)
            active_bullets.append(a)
            active_bullets.append(b)
            active_bullets.append(c)
            active_bullets.append(d)
            active_bullets.append(e)
            self.last_spawn = now

class Attack_type_M(Attack):
    def __init__(self, length, spawn_interval=0.5):
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
            return False
        now = time.time()
        # stop when duration elapsed
        if now - self.start_time >= self.length:
            self.running = False
            return False
        # spawn bullets at spawn_interval
        if self.last_spawn == 0.0 or (now - self.last_spawn) >= self.spawn_interval:
            a = Bullet_type_D(None, (100, 100), 0, 0, 0, 1)
            b = Bullet_type_D(None, (100, 100), 1200, 0, 0, 1)
            c = Bullet_type_A(None, (50, 50), 0, 0, 0, 1)
            d = Bullet_type_C(None, (50, 50), 0, 0, 0, 0, delay=1, speed=1)
            active_bullets.append(a)
            active_bullets.append(b)
            active_bullets.append(c)
            active_bullets.append(d)
            self.last_spawn = now
    
    def clear(self):
        active_bullets.clear()
        self.length = 0
        self.perform_attack()

    def is_ended(self):
        if self.start_time >= self.length:
            return True
        else:
            return False
        
class Attack_type_N(Attack):
    def __init__(self, length, spawn_interval=0.5):
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
            return False
        now = time.time()
        # stop when duration elapsed
        if now - self.start_time >= self.length:
            self.running = False
            return False
        # spawn bullets at spawn_interval
        if self.last_spawn == 0.0 or (now - self.last_spawn) >= self.spawn_interval:
            a = Bullet_type_D(None, (100, 100), 0, 0, 0, 1)
            b = Bullet_type_D(None, (100, 100), 1200, 0, 0, 1)
            d = Bullet_type_C(None, (50, 50), 0, 0, 0, 0, delay=1, speed=1)
            c = Bullet_type_B(None, (100, 100), 0, 600, 1, 0)
            e = Bullet_type_B(None, (100, 100), 0, 925, 1, 0)
            f = Bullet_type_A(None, (50, 50), 0, 0, 0, 1)
            active_bullets.append(a)
            active_bullets.append(b)
            active_bullets.append(c)
            active_bullets.append(d)
            active_bullets.append(e)
            active_bullets.append(f)
            self.last_spawn = now
    
    def clear(self):
        active_bullets.clear()
        self.length = 0
        self.perform_attack()

    def is_ended(self):
        if self.start_time >= self.length:
            return True
        else:
            return False

class Attack_type_O(Attack):
    def __init__(self, length, spawn_interval=0.5):
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
            return False
        now = time.time()
        # stop when duration elapsed
        if now - self.start_time >= self.length:
            self.running = False
            return False
        # spawn bullets at spawn_interval
        if self.last_spawn == 0.0 or (now - self.last_spawn) >= self.spawn_interval:
            a = Bullet_type_D(None, (100, 100), 0, 0, 0, 1)
            b = Bullet_type_D(None, (100, 100), 1200, 0, 0, 1)
            d = Bullet_type_C(None, (50, 50), 0, 0, 0, 0, delay=1, speed=1)
            c = Bullet_type_B(None, (100, 100), 0, 600, 1, 0)
            e = Bullet_type_B(None, (100, 100), 0, 925, 1, 0)
            active_bullets.append(a)
            active_bullets.append(b)
            active_bullets.append(c)
            active_bullets.append(d)
            self.last_spawn = now
    
    def clear(self):
        active_bullets.clear()
        self.length = 0
        self.perform_attack()

    def is_ended(self):
        if self.start_time >= self.length:
            return True
        else:
            return False

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
        if isinstance(b, Bullet_type_C):
            b.move(player)
        else:
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
try:
    _soul_red = pygame.image.load(r'resources\soul_red.png').convert_alpha()
    _soul_orange = pygame.image.load(r'resources\soul_orange.png').convert_alpha()
    _soul_blue = pygame.image.load(r'resources\soul_blue.webp').convert_alpha()
    _soul_purple = pygame.image.load(r'resources\soul_purple.png').convert_alpha()
except Exception:
    # fallback surfaces if assets missing (keeps code robust)
    _soul_red = pygame.Surface((64, 64), pygame.SRCALPHA)
    _soul_orange = pygame.Surface((64, 64), pygame.SRCALPHA)
    _soul_blue = pygame.Surface((64, 64), pygame.SRCALPHA)

SOUL_IMAGES = {
    "Red": pygame.transform.scale(_soul_red, (64, 64)),
    "Orange": pygame.transform.scale(_soul_orange, (64, 64)),
    "Blue": pygame.transform.scale(_soul_blue, (64, 64)),
    "Purple": pygame.transform.scale(_soul_purple, (64, 64)),
}
# ...existing code...
class Player_soul:
    def __init__(self, soul_mode, x=800-32, y=600-32, changex=0, changey=0):
        # use preloaded images instead of loading every frame
        self.soul_mode = soul_mode
        self.img = SOUL_IMAGES.get(self.soul_mode, SOUL_IMAGES["Red"])
        self.current_mode = self.soul_mode  # remember which image is active
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

            # only swap the image if the mode actually changed
            if self.soul_mode != self.current_mode:
                self.img = SOUL_IMAGES.get(self.soul_mode, SOUL_IMAGES["Red"])
                self.current_mode = self.soul_mode

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