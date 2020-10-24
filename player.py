import pygame
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
import datetime
import playfunctions
import params
import primecrime
import layout
import mp3db

# init playunctions & params
pf = playfunctions.PlayFunctions
p = params.Params
pc = primecrime.PrimeCrime
l = layout.Layout
db = mp3db

# database connection
conn = db.create_connection('mp3_db.sqlite')

# initialize pygame etc.
pygame.init()
pygame.mixer.init()
pygame.display.set_caption('2 DA MAXXX')
pygame.event.pump()
pygame.display.set_icon(p.gameIcon)


def playtime():
    msg = str(datetime.timedelta(seconds=int(round(timer/1000))))
    if pc.is_prime(int(round(timer/1000))):
        smallText2 = pygame.font.SysFont("helvetica", 20, 1, 1)
    else:
        smallText2 = pygame.font.SysFont("helvetica", 20)
    textSurf2, textRect2 = l.text_objects(msg, smallText2)
    textRect2.midleft = (250, 80)
    p.screen.blit(textSurf2, textRect2)


def playing():
    msg = "playing song: " + str(str(p.file).split("/")[-1])
    smallText3 = pygame.font.SysFont("helvetica", 10)
    textSurf3, textRect3 = l.text_objects(msg, smallText3)
    textRect3.midleft = (250, 120)
    p.screen.blit(textSurf3, textRect3)


running = True

# check if to continue playing since last time
last_time = db.read_rows(conn, 'lasttime')

if last_time != () and last_time[1] != 'unassigned' and last_time[0] != '-1':
    p.file = last_time[1]
    timer_last = int(float(last_time[0])/1000)
    pygame.mixer.music.load(p.file)
    pygame.mixer.music.play(1, timer_last)
else:
    timer_last = 0

# main loop
while running:
    global songLength
    global volume
    global timer

    p.screen.fill(p.BLACK)

    timer = pygame.mixer.music.get_pos() + timer_last*1000
    # buttons
    play_button = l.button(30, 20, p.playIcon)
    pause_button = l.button(100, 20, p.pauseIcon)
    stop_button = l.button(30, 80, p.stopIcon)
    file_button = l.button(100, 80, p.browseIcon)
    volume_button_up = l.button(540, 20, p.volumeUp)
    volume_button_down = l.button(540, 60, p.volumeDown)
    a_repeater = l.button(250, 5, p.a_button)
    b_repeater = l.button(270, 5, p.b_button)

    # misc
    prog_loc = l.progress_location()
    l.progress_bar()

    volume_loc = l.volume_location()

    playtime()
    pc.number_is_prime()
    playing()
    pf.volume_bar()

    # quit check
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            # write last known time when quitting
            db.clear_table(conn, 'lasttime')
            db.insert_row(conn, timer, str(p.file), 'lasttime')

            pygame.mixer.quit()
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            # If the button collides with the mouse position.
            if play_button.collidepoint(event.pos):
                pf.play_song()
            if pause_button.collidepoint(event.pos):
                pf.pause_song()
            if stop_button.collidepoint(event.pos):
                pf.stop_song()
            if file_button.collidepoint(event.pos):
                pf.select_file()
            if volume_button_up.collidepoint(event.pos):
                pf.set_volume(1)
            if volume_button_down.collidepoint(event.pos):
                pf.set_volume(0)
            if prog_loc.collidepoint(event.pos):
                try:
                    timer_last = ((event.pos[0]-250)/250) * p.songLength
                    pygame.mixer.music.play(1, timer_last)
                except:
                    pass
            if volume_loc.collidepoint(event.pos):
                volume = abs(event.pos[1]-90)*(1/60)
                pf.set_volume2(volume)

            if a_repeater.collidepoint(event.pos):
                pf.a_b_repeater_a(timer)
            if b_repeater.collidepoint(event.pos):
                pf.a_b_repeater_b(timer)

    pygame.display.update()

conn.close()
