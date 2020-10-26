import params
import pygame
import playfunctions


class Layout:

    def text_objects(text, font):
        textSurface = font.render(text, True, p.WHITE)
        return textSurface, textSurface.get_rect()

    def button(x, y, img=None):
        return p.screen.blit(img, (x, y))

    def progress_bar():

        barPos = (250, 30)
        barSize = (250, 20)
        borderColor = (255, 255, 255)
        barColor = (100, 100, 100)

        if p.song_length != 0:
            p.progress = (p.timer/1000)/p.song_length
        else:
            p.progress = 0

        pygame.draw.rect(p.screen, borderColor, (*barPos, *barSize), 1)

        # set bar to zero length if stopped
        if p.timer == -1:
            innerPos = (barPos[0]+3, barPos[1]+3)
            innerSize = ((barSize[0]-6), barSize[1]-6)
            pygame.draw.rect(p.screen, p.BLACK, (*innerPos, *innerSize))
        else:
            innerPos = (barPos[0]+3, barPos[1]+3)
            innerSize = ((barSize[0]-6) * p.progress, barSize[1]-6)
            pygame.draw.rect(p.screen, barColor, (*innerPos, *innerSize))

    def progress_location():
        return pygame.Rect(250, 30, 250, 20)

    def volume_location():
        return pygame.Rect(575, 20, 10, 70)


p = params.Params
pf = playfunctions.PlayFunctions