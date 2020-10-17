import pygame
import tkinter
from tkinter import filedialog
from mp3db import *
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
import datetime

# database connection
conn = create_connection('mp3_db.sqlite')

# initialize pygame etc.
pygame.init()
pygame.mixer.init()

screen_width, screen_height = (600, 150)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('2 DA MAXXX')
pygame.event.pump()

gameIcon = pygame.image.load('icon.png')
playIcon = pygame.image.load('play.png')
pauseIcon = pygame.image.load('pause.png')
stopIcon = pygame.image.load('stop.png')
browseIcon = pygame.image.load('browse.png')
volumeUp = pygame.image.load('volumeUp.png')
volumeDown = pygame.image.load('volumeDown.png')

pygame.display.set_icon(gameIcon)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

file = 'unassigned'
paused = False
volume = 0.5

def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()


def button(x, y, img=None):
    return screen.blit(img, (x, y))


def progress_bar():
    barPos = (250, 30)
    barSize = (250, 20)
    borderColor = (255, 255, 255)
    barColor = (100, 100, 100)

    try:
        song = MP3(file)
        songLength = song.info.length
    except:
        try:
            song = FLAC(file)
            songLength = song.info.length
        except:
            songLength = 100

    progress = (timer/1000)/songLength
    pygame.draw.rect(screen, borderColor, (*barPos, *barSize), 1)

    # set bar to zero length if stopped
    if timer == -1:
        innerPos = (barPos[0]+3, barPos[1]+3)
        innerSize = ((barSize[0]-6), barSize[1]-6)
        pygame.draw.rect(screen, BLACK, (*innerPos, *innerSize))
    else:
        innerPos = (barPos[0]+3, barPos[1]+3)
        innerSize = ((barSize[0]-6) * progress, barSize[1]-6)
        pygame.draw.rect(screen, barColor, (*innerPos, *innerSize))


def playtime():
    msg = str(datetime.timedelta(seconds=int(round(timer/1000))))
    smallText2 = pygame.font.SysFont("helvetica", 20)
    textSurf2, textRect2 = text_objects(msg, smallText2)
    textRect2.midleft = (250, 80)
    screen.blit(textSurf2, textRect2)


def playing():
    msg = "playing song: " + str(str(file).split("/")[-1])
    smallText3 = pygame.font.SysFont("helvetica", 10)
    textSurf3, textRect3 = text_objects(msg, smallText3)
    textRect3.midleft = (250, 120)
    screen.blit(textSurf3, textRect3)


def play_song():
    global paused

    if file != 'unassigned':
        if paused == False:
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
        elif paused == True:
            pygame.mixer.music.unpause()
    else:
        pass


def pause_song():
    global paused

    pygame.mixer.music.pause()
    paused = True


def stop_song():
    global paused
    global timer
    global timer_last

    pygame.mixer.music.stop()
    paused = False
    timer = 0
    timer_last = 0


def select_file():
    global file

    root = tkinter.Tk()
    root.withdraw()
    file = filedialog.askopenfilename(filetypes=(
        ("mp3 files", "*.mp3"), ("flac-elackjes", "*.flac"), ("All files", "*.*")))
    stop_song()
    play_song()
    root.destroy()

def set_volume(n):
    global volume
    if n == 1:
        if volume != 1.0:
            volume += 0.1
            pygame.mixer.music.set_volume(volume)
    if n == 0:
        if volume != 0.0:
            volume -= 0.1
            pygame.mixer.music.set_volume(volume)

running = True

# check if to continue playing since last time
last_time = read_rows(conn, 'lasttime')

if last_time != () and last_time[1] != 'unassigned' and last_time[0] != '-1':
    file = last_time[1]
    timer_last = int(float(last_time[0])/1000)
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(1, timer_last)

else:
    timer_last = 0


# main loop
while running:
    screen.fill(BLACK)
    timer = pygame.mixer.music.get_pos() + timer_last*1000

    # buttons
    play_button = button(30, 20, playIcon)
    pause_button = button(100, 20, pauseIcon)
    stop_button = button(30, 80, stopIcon)
    file_button = button(100, 80, browseIcon)
    volume_button_up = button(540, 20, volumeUp)
    volume_button_down = button(540, 60, volumeDown)

    # misc
    progress_bar()
    playtime()
    playing()

    # quit check
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            # write last known time when quitting
            clear_table(conn, 'lasttime')
            insert_row(conn, timer, str(file), 'lasttime')

            pygame.mixer.quit()
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            # If the button collides with the mouse position.
            if play_button.collidepoint(event.pos):
                play_song()
            if pause_button.collidepoint(event.pos):
                pause_song()
            if stop_button.collidepoint(event.pos):
                stop_song()
            if file_button.collidepoint(event.pos):
                select_file()
            if volume_button_up.collidepoint(event.pos):
                set_volume(1)
            if volume_button_down.collidepoint(event.pos):
                set_volume(0)


    pygame.display.update()

conn.close()
