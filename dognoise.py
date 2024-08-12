from gpiozero import LED, Button
from signal import pause
import pygame
from os import walk, path


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