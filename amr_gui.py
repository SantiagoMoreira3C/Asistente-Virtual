
import speech_recognition as sr
import subprocess as sub
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import keyboard
import colors
import os
import threading as tr
from pygame import mixer
from tkinter import *
from PIL import Image, ImageTk

main_window=Tk()
main_window.title("AMR assitent virtual")

main_window.geometry("800x450")
main_window.resizable(0,0)
main_window.configure(bg='#FFF')

comandos = """
        Comandos que puedes usar:
        - Reproduce...(canción)
        - Busca...(algo)
        - Abre...(página web o app)
        - Alarma..(hora en 24H)
        - Archivo...(nombre)
        - Colores(rojo, azul, amarillo)
        - Termina   
"""


# label_title = Label(main_window, text="AMR", bg="#FFE4E1", fg="#8A2BE2", font=('Arial', 50, 'bold'))

canvas_comandos= Canvas(bg='#FFE4E1', height=170, width=195)
canvas_comandos.place(x=0, y=0)
canvas_comandos.create_text(90, 80, text=comandos, fill='black', font='Arial 10')

text_info = Text(main_window, bg='#6AFFFE', fg='black')
text_info.place(x=0, y=170, height=280, width=195)



# label_title.pack(pady=10)
logo_amr = ImageTk.PhotoImage(Image.open("logo.png"))

window_photo = Label(main_window, image=logo_amr)
window_photo.pack(pady=5)



def spanish_voice():
    change_voice(0)
def english_voice():
    change_voice(1)    
def mexican_voice():
    change_voice(3)    

    

def change_voice(id):
    engine.setProperty('voice', voices[id].id)
    talk("Hola soy tu asistente virtual AMR")


name = "amr"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[3].id)

""" for voice in voices:
    print(voice) """

sites = {
    'google': 'google.com',
    'youtube': 'youtube.com',
    'facebook': 'facebook.com',
    'cursos': 'freecodecamp.org/learn',
    'udemy': 'udemy.com'
}

files = {
    'proyecto': 'PRESENTACION_PROYECTO1.pdf'
}

programs = {
    'word': r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"
}


def talk(text):
    engine.say(text)
    engine.runAndWait()

def read_and_talk():
    text = text_info.get("1.0", 'end')
    talk(text)
def write_text(text_wiki):
    text_info.insert(INSERT, text_wiki)


def listen():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        talk('Te escucho')
        listener.adjust_for_ambient_noise(source)
        pc = listener.listen(source)

    try:
        rec = listener.recognize_google(pc, language="es")
        rec = rec.lower()
    except sr.UnknownValueError:
        print("No te entendí, intenta de nuevo")
        if name in rec:
            rec = rec.replace(name, '')
    return rec



def run_amr():
    while True:
        try:
            rec = listen()
        except UnboundLocalError:
            print("No te entendí, intenta de nuevo")
            continue
        if 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            print("Reproduciendo " + music)
            talk("Reproduciendo " + music)
            pywhatkit.playonyt(music)
        elif 'busca' in rec:
            search = rec.replace('busca', '')
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 1)
            talk(wiki)
            write_text(search + ":" + wiki)
            break 
        elif 'alarma' in rec:
            num = rec.replace('alarma', '')
            num = num.strip()
            talk("Alarma activida a las " + num + "horas")
            while True:
                if datetime.datetime.now().strftime('%H:%M') == num:
                    print("DESPIERTA")
                    mixer.init()
                    mixer.music.load("auronplay-alarma.mp3")
                    mixer.music.play()
                    if keyboard.read_key() == "s":
                        mixer.music.stop()
                        break
        elif 'colores' in rec:
            talk("Enseguida")
            colors.capture()
        elif 'abre' in rec:
            for site in sites:
                if site in rec:
                    sub.call(f'start chrome.exe {sites[site]}', shell=True)
                    talk(f'Abriendo {site}')
            for app in programs:
                if app in rec:
                    talk(f'Abriendo {app}')
                    os.startfile(programs[app])

        elif 'archivo' in rec:
            for file in files:
                if file in rec:
                    sub.Popen([files[file]], shell=True)
                    talk(f'Abriendo {file}')
        elif 'escribe' in rec:
            try:
                with open("nota.txt", 'a') as f:
                    write(f)

            except FileNotFoundError as e:
                file = open("nota.txt", 'a')
                write(file)

        elif 'termina' in rec:
            talk('Adios')
            break


def write(f):
    talk("¿Qué quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True)

button_voice_mx = Button(main_window, text="Voz México", fg="white", bg='purple', font=("Arial", 10,"bold"), command=mexican_voice)

button_voice_mx.place(x=625, y=70, width=100, height=30)

button_voice_es = Button(main_window, text="Voz España", fg="white", bg='purple', font=("Arial", 10,"bold" ), command=spanish_voice)

button_voice_es.place(x=625, y=40,  width=100, height=30)

button_voice_us = Button(main_window, text="Voz USA", fg="white", bg='purple', font=("Arial", 10,"bold" ), command=english_voice)

button_voice_us.place(x=625, y=100,  width=100, height=30)

button_listen = Button(main_window, text="Escuchar", fg="white", bg='purple', width=20,font=("Arial", 15,"bold" ), command=run_amr)

button_listen.pack(pady=10)


button_speak = Button(main_window, text="Hablar", fg="white", bg='blue', font=("Arial", 10,"bold"), command=read_and_talk)

button_speak.place(x=625, y=140, width=100, height=30)



main_window.mainloop()