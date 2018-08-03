import glob
import os
import re
import pygame
from math import log2, pow

try:
    pygame.init() # Throws error in pylint: security issue for C module. Ignore.
except ImportError:
    exit("This script requires the pygame module\nInstall with: sudo pip3 install pygame")

BANK = os.path.join(os.path.dirname(__file__), "sounds")

NOTE_OFFSET = 0
FILETYPES = ['*.wav', '*.ogg']
samples = []
files = []

# Tuning, and constants for freq-to-note conversion
A4 = 440
C0 = A4*pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.mixer.set_num_channels(256)

patches = glob.glob(os.path.join(BANK, '*'))
print(patches)
patch_index = 0

if len(patches) == 0:
    exit("Couldn't find any .wav files in {}".format(BANK))


def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    """Used to ensure samples load in sane order from filesystem."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s)]


def load_samples(patch):
    """Load audio samples into buffers for playback."""
    global samples, files, octave, octaves
    files = []
    print('Loading samples from: {}'.format(patch))
    for filetype in FILETYPES:
        files.extend(glob.glob(os.path.join(patch, filetype)))
    files.sort(key=natural_sort_key)
    octaves = len(files) / 12
    samples = [pygame.mixer.Sound(sample) for sample in files]
    octave = int(octaves / 2)


def handle_note(channel, octave):
    """Synthesise a commanded note using Pygame samples: direct audio playback."""
    channel = channel + (12 * octave) + NOTE_OFFSET
    if channel < len(samples):
        # print('Playing Sound: {}'.format(files[channel]))
        print('Playing sound: {}'.format(channel))
        samples[channel].play(loops=0)
    else:
        print('Note out of bounds')


def handle_octave_up():
    global octave
    if octave < octaves:
        octave += 1
        print('Selected Octave: {}'.format(octave))


def handle_octave_down():
    global octave
    if octave > 0:
        octave -= 1
        print('Selected Octave: {}'.format(octave))


def scale_up(notes, delay):
    global octave
    for note in range(notes):
        handle_note(note, octave)
        sleep(delay)


def scale_down(notes, delay):
    global octave
    for note in range(notes):
        handle_note(notes-note, octave)
        sleep(delay)


def freq_to_note(freq):
    """Outputs note and octave for input frequency.

    Based on https://www.johndcook.com/blog/2016/02/10/musical-pitch-notation/
    by John D. Cook
    """
    h = round(12*log2(freq/C0)) # Python3 only
    # h = round(12*(log(freq/C0)/log(2)))
    octave = (h // 12) - 6
    n = h % 12
    return name[int(n)], int(octave)

# Load audio samples
load_samples(patches[patch_index])

