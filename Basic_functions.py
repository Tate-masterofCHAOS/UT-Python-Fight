
import pygame
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((1600,1200))
pygame.display.set_caption("UT-Fight")
pygame_icon = pygame.image.load(r'resources\soul_red.png')
pygame.display.set_icon(pygame_icon)

#Plays background music for battle scenes
def play_bgm_battle():
    mixer.music.load(r'resources/[Aftertale Original] SharaX - Hello World (Fatal Error).mp3')
    mixer.music.play(-1)

#Plays sound effect for selection actions
def select_sound():
    pygame.mixer.Sound(r'resources\select.wav').play()

