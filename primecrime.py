import params
import pygame
import layout
import playfunctions

pf = playfunctions.PlayFunctions
p = params.Params
l = layout.Layout


class PrimeCrime:

    def number_is_prime():
        if PrimeCrime.is_prime(p.song_length):
            msg = ("Number is prime, yesss!")
        else:
            msg = ("Number is not prime, noooo!")
        smallText2 = pygame.font.SysFont("helvetica", 10)
        textSurf2, textRect2 = l.text_objects(msg, smallText2)
        textRect2.midleft = (250, 135)
        p.screen.blit(textSurf2, textRect2)

    def is_prime(n):
        for i in range(2, int(n**0.5)+1):
            if n % i == 0:
                return False
        return True
