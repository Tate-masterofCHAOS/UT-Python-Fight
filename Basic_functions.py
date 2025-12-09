
import pygame
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((1600,1200))
pygame.display.set_caption("UT-Fight")
pygame_icon = pygame.image.load(r'resources\soul_red.png')
pygame.display.set_icon(pygame_icon)

#Plays background music for battle scenes
def play_bgm_battle():
    mixer.music.load(r'resources\Undertale Time Paradox [OST] - Doopix.mp3')
    mixer.music.play(-1)

def damage_sound():
    damage = pygame.mixer.Sound(r'resources\Taken_damage.mp3')
    damage.set_volume(0.3)
    damage.play()

#Plays sound effect for selection actions
def select_sound():
    pygame.mixer.Sound(r'resources\select.wav').play()

