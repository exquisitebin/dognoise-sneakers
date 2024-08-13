from gpiozero import Button, DistanceSensor
from time import sleep
from signal import signal, SIGTERM, SIGHUP, pause
import pygame
from os import walk, path
from threading import Thread

shoes_enabled = False

def safe_exit(signum, frame):
    print("Exiting")
    pygame.quit()
    exit(0)


def load_sounds():
    pygame.init()
    sounds = []
    exts = ('.wav', '.mp3')
    for root, _, files in walk('dog-sounds'):
        for filename in files:
            print(filename)
            if filename.endswith(exts):
                sounds.append(pygame.mixer.Sound(path.join(root, filename)))

    print(sounds)
    return sounds
    

def bark(sounds):
    print("Woof!")
    sounds[0].play()

def button_thread():
    global shoes_enabled
    sounds = load_sounds()

    sole_btn = Button(27)

    while True:
        if sole_btn.is_pressed and shoes_enabled:
            if not pressed:
                pressed = True
                bark(sounds)
        else:
            pressed = False

def sensor_thread():
    global shoes_enabled
    sensor = DistanceSensor(echo=20, trigger=21)
    while True:
        if sensor.distance < 0.04:
            shoes_enabled = True
            break
        sleep(0.1)
    sensor.close()

      
    

def dognoise():
    global shoes_enabled

    thread_button = Thread(target=button_thread)
    thread_sensor = Thread(target=sensor_thread)
    sensor = DistanceSensor(echo=20, trigger=21)
    print("Dog noise started")

    try:
        thread_button.start()
        thread_sensor.start()
        
        thread_sensor.join()
        thread_button.join()
       
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting")

        thread_sensor.join()
        thread_button.join()
        sensor.close()
        print("Cleaning up")
        pygame.quit()
        exit(0)


if __name__ == '__main__':
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    dognoise()