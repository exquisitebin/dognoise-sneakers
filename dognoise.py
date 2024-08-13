from gpiozero import Button, DistanceSensor
from time import sleep
from signal import signal, SIGTERM, SIGHUP, pause
import pygame
from os import walk, path

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
    

def dognoise():
    sensor = DistanceSensor(echo=20, trigger=21)
    sounds = load_sounds()
    print("Dog noise started")




    bottom_btn = Button(27)

    pressed = False
    try:
        while True:
            if bottom_btn.is_pressed:
                if not pressed:
                    pressed = True
                    bark(sounds)
            else:
                pressed = False

            print(sensor.value)
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        sensor.close()
        print("Cleaning up")
        pygame.quit()
        exit(0)


if __name__ == '__main__':
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    dognoise()