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