import pygame
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
import tkinter
from tkinter import filedialog
import time
import params
# import primecrime
import mp3db


class PlayFunctions():

    def play_song():
        if p.file != 'unassigned':
            if p.paused == False:
                pygame.mixer.music.load(p.file)
                pygame.mixer.music.play()
            elif p.paused == True:
                pygame.mixer.music.unpause()
        else:
            pass

    def pause_song():
        pygame.mixer.music.pause()
        p.paused = True

    def stop_song():
        pygame.mixer.music.stop()
        p.paused = False
        p.timer = 0
        p.timer_last = 0

    def get_songlength():
        if p.file != 'unassigned':
            try:
                song = MP3(p.file)
            except:
                song = FLAC(p.file)

            p.song_length = int(song.info.length)
        else:
            p.song_length = 0

    def select_file():
        root = tkinter.Tk()
        root.withdraw()
        p.file = filedialog.askopenfilename(filetypes=(
            ("mp3 files", "*.mp3"), ("flac-elackjes", "*.flac"), ("All files", "*.*")))
        PlayFunctions.stop_song()
        PlayFunctions.play_song()
        # pc.number_is_prime()
        db.insert_song(db.create_connection('mp3_db.sqlite'),
                       str(p.file), p.song_length, 'songs')
        root.destroy()

    def set_volume(n):
        if n == 1:
            if p.volume < 1.1:
                p.volume += 0.1
                pygame.mixer.music.set_volume(p.volume)
        if n == 0:
            if p.volume > 0.1:
                p.volume -= 0.1
                pygame.mixer.music.set_volume(p.volume)

    def set_volume2(pos):
        pygame.mixer.music.set_volume(pos)

    def volume_bar():
        barPos = (575, 20)
        barSize = (10, 70)
        borderColor = (255, 255, 255)
        barColor = (100, 100, 100)
        progress_vol = int(p.volume*10)
        innerPos = (barPos[0]+3, barPos[1]+3)
        innerSize = ((barSize[0]-6), barSize[1]-6 * progress_vol)
        pygame.draw.rect(p.screen, borderColor, (*barPos, *barSize), 1)
        if 1 < progress_vol < 11:
            pygame.draw.rect(p.screen, barColor, (*innerPos, *innerSize))

    def a_b_repeater_a(n):
        p.a_rep = n

    def a_b_repeater_b(n):
        p.b_rep = n
        repeat = float(p.b_rep/1000) - float(p.a_rep/1000)
        print(repeat)
        #pygame.mixer.music.play(1, int(float(a_rep)/1000))
        pygame.mixer.music.set_pos(p.a_rep/1000)
        # while pygame.mixer.music.get_busy():
        count = 0
        while count < 6:
            time.sleep(repeat)
            pygame.mixer.music.set_pos(p.a_rep/1000)
            count += 1
        pygame.mixer.music.stop()
        pygame.mixer.music.play()
        pygame.mixer.music.set_pos(p.b_rep/1000)


# init parameters
p = params.Params
# pc = primecrime.PrimeCrime
db = mp3db
