import pygame

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

    #colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (100, 100, 100)

    #images
    gameIcon = pygame.image.load('icon.png')
    playIcon = pygame.image.load('play.png')
    pauseIcon = pygame.image.load('pause.png')
    stopIcon = pygame.image.load('stop.png')
    browseIcon = pygame.image.load('browse.png')
    volumeUp = pygame.image.load('volumeUp.png')
    volumeDown = pygame.image.load('volumeDown.png')
    a_button = pygame.image.load('a.png')
    b_button = pygame.image.load('b.png')