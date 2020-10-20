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
a_button = pygame.image.load('a.png')
b_button = pygame.image.load('b.png')

pygame.display.set_icon(gameIcon)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

file = 'unassigned'
paused = False
volume = 0.5
new_timer = 0
a_rep = 0
b_rep = 0


def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()


def button(x, y, img=None):
    return screen.blit(img, (x, y))


def progress_bar():
    global songLength
    global timer

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


def progress_location():
    return pygame.Rect(250, 30, 250, 20)


def playtime():
    msg = str(datetime.timedelta(seconds=int(round(timer/1000))))
    if is_prime(int(round(timer/1000))):
        smallText2 = pygame.font.SysFont("helvetica", 20, 1, 1)
    else:
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
    number_is_prime()
    root.destroy()


def set_volume(n):
    global volume
    if n == 1:
        if volume < 1.1:
            volume += 0.1
            pygame.mixer.music.set_volume(volume)
    if n == 0:
        if volume > 0.1:
            volume -= 0.1
            pygame.mixer.music.set_volume(volume)

def volume_bar():
    global volume
    barPos = (575, 20)
    barSize = (10, 70)
    borderColor = WHITE
    barColor = GRAY
    progress = int(volume*10)
    innerPos = (barPos[0]+3, barPos[1]+3)
    innerSize = ((barSize[0]-6), barSize[1]-6 * progress)
    pygame.draw.rect(screen, borderColor, (*barPos, *barSize), 1)
    if 1 < progress < 11:
        pygame.draw.rect(screen, barColor, (*innerPos, *innerSize))

def a_b_repeater_a(n):
    global a_rep
    a_rep = n

def a_b_repeater_b(n):
    global a_rep
    global b_rep
    global timer
    b_rep = n
    pygame.mixer.music.play(1, int(float(a_rep)/1000))

def timeroo():
    timeroo = pygame.mixer.music.get_pos()

def number_is_prime():
    global file
    song = MP3(file)
    songLength = int(song.info.length)
    if is_prime(songLength):
        msg = ("Number is prime, yesss!")
    else:
        msg = ("Number is not prime, noooo!")
    smallText2 = pygame.font.SysFont("helvetica", 10)
    textSurf2, textRect2 = text_objects(msg, smallText2)
    textRect2.midleft = (250, 135)
    screen.blit(textSurf2, textRect2)

def is_prime(n):
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return False     
    return True

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
    global songLength
    screen.fill(BLACK)

    timer = pygame.mixer.music.get_pos() + timer_last*1000

    # buttons
    play_button = button(30, 20, playIcon)
    pause_button = button(100, 20, pauseIcon)
    stop_button = button(30, 80, stopIcon)
    file_button = button(100, 80, browseIcon)
    volume_button_up = button(540, 20, volumeUp)
    volume_button_down = button(540, 60, volumeDown)
    a_repeater = button(250, 5, a_button)
    b_repeater = button(270, 5, b_button)

    # misc
    prog_loc = progress_location()
    progress_bar()
    playtime()
    number_is_prime()
    playing()
    volume_bar()

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
            if prog_loc.collidepoint(event.pos):
                try:
                    timer_last = ((event.pos[0]-250)/250) * songLength
                    pygame.mixer.music.play(1, timer_last)
                except:
                    pass
            if a_repeater.collidepoint(event.pos):
                a_b_repeater_a(timer)
            if b_repeater.collidepoint(event.pos):
                a_b_repeater_b(timer)


    pygame.display.update()

conn.close()
