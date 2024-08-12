from gpiozero import LED, Button
from signal import pause
import pygame
from os import walk, path


def load_sounds():
    pygame.init()
    sounds = {}
    exts = ('.wav', '.mp3')
    for root, _, files in walk('sounds'):
        for filename in files:
            if filename.endswith(exts):
                sounds[filename.split('.')[0]] = pygame.mixer.Sound(path.join(root, filename))
    return sounds
    

def bark(sounds):
    print("Woof!")
    sounds['bark'].play()
    

def dognoise():
    sounds = load_sounds()
    print("Dog noise started")

    bottom_btn = Button(27)

    pressed = False

    while True:
        if bottom_btn.is_pressed:
            if not pressed:
                pressed = True
                bark(sounds)
        else:
            pressed = False


if __name__ == '__main__':
    dognoise()