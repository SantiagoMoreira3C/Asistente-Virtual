
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

def charge_data(name_dict, name_file):
    try:
        with open(name_file) as f:
            for line in f:
                (key, val) = line.split(",")
                val = val.rstrip("\n")
                name_dict[key] = val
    except FileNotFoundError as e:
        pass


sites = dict()
charge_data(sites, "pages.txt")
files = dict()
charge_data(files, "archivos.txt")
programs = dict()
charge_data(programs, "apps.txt")


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
                    mixer.music.load("alarma.mp3")
                    mixer.music.play()
                    if keyboard.read_key() == "s":
                        mixer.music.stop()
                        break
        elif 'colores' in rec:
            talk("Enseguida")
            colors.capture()
        elif 'abre' in rec:
            task = rec.replace('abre','').strip()
            if task in sites:
                for task in sites:
                    if task in rec:
                        sub.call(f'start chrome.exe {sites[task]}', shell=True)
                        talk(f'Abriendo {task}')
            elif task in programs:
                for task in programs:
                    if task in rec:
                        talk(f'Abriendo {task}')
                        os.startfile(programs[task])
            else:
                talk("Lo siento,  parece que aún no has agregado esa app o página web")

        elif 'archivo' in rec:
            file = rec.replace('archivo','').strip()
            if file in files:
                for file in files:
                    if file in rec:
                        sub.Popen([files[file]], shell=True)
                        talk(f'Abriendo {file}')
            else:
                talk("Lo siento,  parece que aún no has agregado esa archivo")


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

def open_w_files():
    global namefile_entry, pathf_entry
    window_files = Toplevel()
    window_files.title("Agrega Archivos")
    window_files.configure(bg="#FFADE6")
    window_files.geometry("300x200")
    window_files.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(window_files)} center')

    title_tabel = Label(window_files,text="Agrega un archivo", fg="black", bg="#B29F9D", font=('Arial', 15, 'bold'))
    title_tabel.pack(pady=3)

    name_tabel = Label(window_files,text="Nombre del Archivo", fg="black", bg="#B29F9D", font=('Arial', 10, 'bold'))
    name_tabel.pack(pady=2)

    namefile_entry = Entry(window_files)
    namefile_entry.pack(pady=1)

    path_tabel = Label(window_files,text="Ruta del Archivo", fg="black", bg="#B29F9D", font=('Arial', 10, 'bold'))
    path_tabel.pack(pady=2)

    pathf_entry = Entry(window_files, width=35)
    pathf_entry.pack(pady=1)

    save_button = Button(window_files, text="Guardar", bg="green", fg="white", width=8, height=1, command=add_files)
    save_button.pack(pady=4)


def open_w_apps():
    global nameapps_entry, patha_entry
    window_apps = Toplevel()
    window_apps.title("Agrega Apps")
    window_apps.configure(bg="#FFADE6")
    window_apps.geometry("300x200")
    window_apps.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(window_apps)} center')

    title_tabel = Label(window_apps,text="Agrega una app", fg="black", bg="#B29F9D", font=('Arial', 15, 'bold'))
    title_tabel.pack(pady=3)

    name_tabel = Label(window_apps,text="Nombre de la app", fg="black", bg="#B29F9D", font=('Arial', 10, 'bold'))
    name_tabel.pack(pady=2)

    nameapps_entry = Entry(window_apps)
    nameapps_entry.pack(pady=1)

    path_tabel = Label(window_apps,text="Ruta de la app", fg="black", bg="#B29F9D", font=('Arial', 10, 'bold'))
    path_tabel.pack(pady=2)

    patha_entry = Entry(window_apps, width=35)
    patha_entry.pack(pady=1)

    save_button = Button(window_apps, text="Guardar", bg="green", fg="white", width=8, height=1, command=add_apps)
    save_button.pack(pady=4)

def open_w_pages():
    global namepages_entry, pathp_entry
    window_pages = Toplevel()
    window_pages.title("Agrega páginas web")
    window_pages.configure(bg="#FFADE6")
    window_pages.geometry("300x200")
    window_pages.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(window_pages)} center')

    title_tabel = Label(window_pages,text="Agrega una página web", fg="black", bg="#B29F9D", font=('Arial', 15, 'bold'))
    title_tabel.pack(pady=3)

    name_tabel = Label(window_pages,text="Nombre de la página web", fg="black", bg="#B29F9D", font=('Arial', 10, 'bold'))
    name_tabel.pack(pady=2)

    namepages_entry = Entry(window_pages)
    namepages_entry.pack(pady=1)

    path_tabel = Label(window_pages,text="Ruta de la página web", fg="black", bg="#B29F9D", font=('Arial', 10, 'bold'))
    path_tabel.pack(pady=2)

    pathp_entry = Entry(window_pages, width=35)
    pathp_entry.pack(pady=1)

    save_button = Button(window_pages, text="Guardar", bg="green", fg="white", width=8, height=1, command=add_pages)
    save_button.pack(pady=4)

def add_files():
    name_file = namefile_entry.get().strip()
    path_file = pathf_entry.get().strip()

    files[name_file] = path_file
    save_data(name_file, path_file, "archivos.txt")
    namefile_entry.delete(0, "end")
    pathf_entry.delete(0, "end")


def add_apps():
    name_file = nameapps_entry.get().strip()
    path_file = patha_entry.get().strip()

    programs[name_file] = path_file
    save_data(name_file, path_file, "apps.txt")
    nameapps_entry.delete(0, "end")
    patha_entry.delete(0, "end")


def add_pages():
    name_page = namepages_entry.get().strip()
    url_pages = pathp_entry.get().strip()

    sites[name_page] = url_pages
    save_data(name_page, url_pages, "pages.txt")
    namepages_entry.delete(0, "end")
    pathp_entry.delete(0, "end")

def save_data(key, value, file_name):
    try:
        with open(file_name, 'a') as f:
            f.write(key + "," + value + "\n")
    except FileNotFoundError:
        file = open(file_name, 'a')
        file.write(key + "," + value + "\n")

button_add_files = Button(main_window, text="Agregar Archivos", fg="white", bg='#885588', font=("Arial", 10,"bold"), command=open_w_files)

button_add_files.place(x=625, y=180, width=120, height=30)

button_add_apps = Button(main_window, text="Agregar App", fg="white", bg='#885588', font=("Arial", 10,"bold"), command=open_w_apps)

button_add_apps.place(x=625, y=220, width=120, height=30)


button_add_pages = Button(main_window, text="Agregar páginas", fg="white", bg='#885588', font=("Arial", 10,"bold"), command=open_w_pages)

button_add_pages.place(x=625, y=260, width=120, height=30)




main_window.mainloop()