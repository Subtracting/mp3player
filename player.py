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

screen_width, screen_height = (600, 200)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('2 DA MAXXX')
pygame.event.pump()

gameIcon = pygame.image.load('icon.png')
pygame.display.set_icon(gameIcon)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

file = 'unassigned'
paused = False


def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    smallText = pygame.font.SysFont("helvetica", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    screen.blit(textSurf, textRect)


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
    root.destroy()
    stop_song()
    play_song()


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
    events = pygame.event.get()
    timer = pygame.mixer.music.get_pos() + timer_last*1000

    # initialize buttons
    play_button = button('play', 30, 30, 60, 30, GRAY, WHITE)
    pause_button = button('pause', 100, 30, 60, 30, GRAY, WHITE)
    stop_button = button('stop', 30, 80, 60, 30, GRAY, WHITE)
    file_button = button('browse', 30, 150, 80, 30, GRAY, WHITE)
    progress_bar()
    playtime()
    playing()

    # input
    for event in events:

        # button input
        if event.type == pygame.MOUSEBUTTONDOWN:
            play_button = button('play', 30, 30, 60, 30,
                                 GRAY, WHITE, play_song)
            pause_button = button('pause', 100, 30, 60,
                                  30, GRAY, WHITE, pause_song)
            stop_button = button('stop', 30, 80, 60, 30,
                                 GRAY, WHITE, stop_song)
            file_button = button('browse', 30, 150, 80, 30,
                                 GRAY, WHITE, select_file)

        if event.type == pygame.QUIT:

            # write last known time when quitting
            clear_table(conn, 'lasttime')
            insert_row(conn, timer, str(file), 'lasttime')

            pygame.mixer.quit()
            running = False

    pygame.display.update()

conn.close()
