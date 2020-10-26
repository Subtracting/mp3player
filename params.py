import pygame
from mp3db import *

class Params:
    #screen
    screen_width, screen_height = (600, 150)
    screen = pygame.display.set_mode((screen_width, screen_height))
 
    #parameters
    file = 'unassigned'
    paused = False
    volume = 0.5
    new_timer = 0
    a_rep = 0
    b_rep = 0
    timer_last = 0

    #colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (100, 100, 100)

    #images
    gameIcon = pygame.image.load('icons\\icon.png')
    playIcon = pygame.image.load('icons\\play.png')
    pauseIcon = pygame.image.load('icons\\pause.png')
    stopIcon = pygame.image.load('icons\\stop.png')
    browseIcon = pygame.image.load('icons\\browse.png')
    volumeUp = pygame.image.load('icons\\volumeUp.png')
    volumeDown = pygame.image.load('icons\\volumeDown.png')
    a_button = pygame.image.load('icons\\a.png')
    b_button = pygame.image.load('icons\\b.png')