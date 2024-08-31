from random import randint
from gpiozero import Button, DistanceSensor
from time import sleep
from signal import signal, SIGTERM, SIGHUP, pause
import pygame
from os import walk, path
from threading import Thread

shoes_enabled = False
exit_signal = False
sounds = []

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

def random_index():
    return randint(0, len(sounds) - 1)

def bark():
    global shoes_enabled
    global sounds
    if shoes_enabled:
        index = random_index()
        print(f"Woof! {index}")
        sounds[index].play()

def button_thread():
    global shoes_enabled
    global exit_signal
    sounds = load_sounds()

    sole_btn = Button(27)

    while not exit_signal:
        if sole_btn.is_pressed and shoes_enabled:
            if not pressed:
                pressed = True
                bark(sounds)
        else:
            pressed = False

def sensor_thread():
    global shoes_enabled
    global exit_signal
    sensor = DistanceSensor(echo=20, trigger=21)
    while not exit_signal:
        print(sensor.distance)
        if sensor.distance < 0.1:
            shoes_enabled = True
        else:
            shoes_enabled = False
        sleep(0.5)
    sensor.close()

      
    

def dognoise():
    global shoes_enabled
    global exit_signal

    # thread_button = Thread(target=button_thread)
    thread_sensor = Thread(target=sensor_thread)
    print("Dog noise started")
    button = Button(27)
    button.when_pressed = bark

    try:
        
        # thread_button.start()
        thread_sensor.start()
        
        thread_sensor.join()
        # thread_button.join()
       
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting")
        exit_signal = True
        thread_sensor.join()
        # thread_button.join()
        print("Cleaning up")
        pygame.quit()
        exit(0)


if __name__ == '__main__':
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    sounds = load_sounds()
    dognoise()