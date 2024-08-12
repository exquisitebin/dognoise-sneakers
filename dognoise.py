from gpiozero import LED, Button
from signal import pause
from pygame import mixer
from os import walk, path


def load_sounds():
    mixer.init()
    sounds = {}
    exts = ('.wav', '.mp3')
    for root, _, files in walk('sounds'):
        for filename in files:
            if filename.endswith(exts):
                sounds[filename.split('.')[0]] = mixer.Sound(path.join(root, filename))
    return sounds
    


def dognoise():
    sounds = load_sounds()

    bottom_btn = Button(2)


    while True:
        if bottom_btn.is_pressed:
            bark()
        else:
            pass



def bark():
    print("Woof!")
    


if __name__ == '__main__':
    dognoise()