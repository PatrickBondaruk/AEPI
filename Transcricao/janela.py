from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
import datetime
import time
import pyaudio
import wave
import threading
import random
import sys


import os
from os import listdir
from os.path import isfile, join



class Start (Popup):

    def __init__(self):
        super().__init__()
        f = open("disc.txt", "r")
        self.ids.texto.text=f.read()

    def load(self):

        self.janela.nome = self.ids.nome.text
        self.janela.load()
        self.dismiss()

class Gameover (Popup):

    def __init__(self):
        super().__init__()
        self.ids.textox.text="Thanks for you participation"

    def kill(self):
        sys.exit()







class Janela(BoxLayout):
    files = None
    i = None
    popup = None
    multicalltrigger = False
    recording = False

    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 1
    WAVE_OUTPUT_FILENAME = "file.wav"
    audio = pyaudio.PyAudio()
    stream = None
    frames=[]
    data=None
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                                  rate=RATE, input=True,
                                  frames_per_buffer=CHUNK)
    reaction=None
    lastlenght=None
    def __init__(self):
        super().__init__()





    def pop(self):
        self.popup = Start()
        self.popup.open()

    def load(self):

        self.starttime = time.time()
        self.i = 0
        self.mypath = os.getcwd()+'/audio'
        self.files = [f for f in listdir(self.mypath) if isfile(join(self.mypath, f))]
        print(self.files)
        random.shuffle(self.files)
        now = datetime.datetime.now()

        report = self.nome+ "-"
        report += str(now.day)
        report += str(now.month)
        report += str(now.hour)
        report += str(now.minute)



        try:
            os.stat("Results")
        except:
            os.mkdir("Results")

        try:
            os.stat(self.nome+"-responses")
        except:
            os.mkdir(self.nome+"-responses")

        self.file = open("Results/"+report+".csv", "w")
        self.file.write("Audio,Likert,Decision_time,Audio_lenght,Total_time \n")
        self.file.flush()
        self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                                      rate=self.RATE, input=True,
                                      frames_per_buffer=self.CHUNK)




    def gravathread(self):

        self.frames = []



        self.recording = True

        # for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
        while (self.recording == True):
            self.data = self.stream.read(self.CHUNK)
            self.frames.append(self.data)






    def gravar(self):
        self.WAVE_OUTPUT_FILENAME=self.nome+"-responses/"+self.files[self.i]+"_"+self.nome+".wav"
        self.ids.parar.disabled = False
        self.ids.gravador.disabled = True
        # start Recording
        thread1 = threading.Thread(target=self.gravathread)
        thread1.daemon = True
        thread1.start()

        self.reaction= time.time() - self.starttime





    def parar(self):
        self.recording=False
        self.ids.parar.disabled = True
        self.ids.slido.disabled = False



        self.data = None

        waveFile = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(self.frames))
        waveFile.close()

    def next(self):
        if(self.i==len(self.files)):

            pop=Gameover()
            pop.open()
        else:
            self.starttime = time.time()
            self.ids.gravador.disabled =False

            self.ids.proximo.disabled=True

            sound = SoundLoader.load(join(self.mypath,self.files[self.i]))
            if sound:
                self.lastlenght= sound.length
                sound.play()

    def escreve(self):
        if(self.multicalltrigger ==False):
            self.escreveu = time.time() - self.starttime
            self.ids.slido.disabled=False
            self.multicalltrigger = True
        pass

    def slide(self):
        if(self.ids.slido.disabled==False and self.ids.pronto.disabled==True):
            self.ids.pronto.disabled=False

    def pronto(self):
        self.ids.pronto.disabled=True
        self.ids.proximo.disabled=False





        pressao = time.time() - self.starttime
        linha = self.files[self.i]+","
        linha +=str(self.ids.slido.value)+","
        linha +=str(self.reaction)+","
        linha += str(self.lastlenght) + ","
        linha +=str(pressao)+"\n"



        self.file.write(linha)
        self.file.flush()
        self.ids.slido.disabled = True
        self.multicalltrigger = False
        self.i += 1
        self.ids.slido.value = 1.0


class Test(App):
    global f
    f = None
    def build(self):
        self.f = Janela()
        self.icon = 'aepi.png'
        self.title = 'AEPI - Aplicativo para Estudos em Percepção e Inteligibilidade'
        return self.f

    def on_start(self):
        pop = Start()
        pop.open()
        pop.janela = self.f;




#Window.fullscreen = True
Test().run()
