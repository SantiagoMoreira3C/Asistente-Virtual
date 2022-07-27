
import speech_recognition as sr
import subprocess as sub
import pyttsx3, pywhatkit, wikipedia, datetime, keyboard, colors, os
from pygame import mixer 
import threading as tr

name ="amr"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

sites = {
        'google':'google.com',
        'youtube':'youtube.com',
        'facebook':'facebook.com',
        'cursos':'freecodecamp.org/learn',
        'udemy':'udemy.com'
}

files ={
    'proyecto':'PRESENTACION_PROYECTO1.pdf'
}

programs={
    'zoom': r"C:\Users\Supersan30\AppData\Roaming\Zoom\bin\zoom.exe",
    'word': r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"
}


def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    listener = sr.Recognizer()     
    with sr.Microphone() as source:
        print("Escuchando...")
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


def clock(rec):
    num = rec.replace('alarma', '')
    num = num.strip()
    talk("Alarma activada a las " + num + " horas")
    if num[0] != '0' and len(num) < 5:
        num = '0' + num
    print(num)
    while True:
        if datetime.datetime.now().strftime('%H:%M') == num:
            print("DESPIERTA!!!")
            mixer.init()
            mixer.music.load("alarma.mp3")
            mixer.music.play()
        else:
            continue
        if keyboard.read_key() == "s":
            mixer.music.stop()
            break

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
            print(search +":"+ wiki)
            talk(wiki)
        elif 'alarma' in rec:
            t = tr.Thread(target=clock, args=(rec,))
            t.start()
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
                file = open("nota.txt",'a')
                write(file)
                
        elif 'termina' in rec:
                talk('Adios')
                break 

            
def write(f):
    talk("¿Qué quieres que escriba?")
    rec_write = listen()
    f.write(rec_write+ os.linesep)
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True)

if __name__ == "__main__":
    run_amr()


