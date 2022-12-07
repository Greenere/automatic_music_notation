import RPi.GPIO as GPIO
import time
import pygame
import os

_START = 17
_PAUSE = 22
_END = 23
_QUIT = 27
_WIDTH = 320
_HEIGHT = 240

os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT 
os.putenv('SDL_FBDEV', '/dev/fb1') 
os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT 
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()
pygame.mouse.set_visible(False)

width, height = _WIDTH, _HEIGHT
size = (width, height)
screen = pygame.display.set_mode(size)

def mouse_on_button(mouse, rect):
    x, y, width, height = rect.x, rect.y, rect.w, rect.h
    return (x - width//2 < mouse[0] < x + width//2) and \
           (y - height//2 < mouse[1] < y + height//2)


def get_music_note_symbol(image_path, size, x, y):
    music_note_symbol = pygame.image.load(image_path)
    music_note_symbol = pygame.transform.scale(music_note_symbol, [size, size])
    music_note_symbol_rect = music_note_symbol.get_rect()
    music_note_symbol_rect = music_note_symbol_rect.move([x,y])
    return music_note_symbol, music_note_symbol_rect



GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering
GPIO.setup(_START, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(_PAUSE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(_END, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(_QUIT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def start_pressed() -> bool:
    return not GPIO.input(_START)

def pause_pressed() -> bool:
    return not GPIO.input(_PAUSE)

def end_pressed() -> bool:
    return not GPIO.input(_END)

def quit_pressed() -> bool:
    return not GPIO.input(_QUIT)

def beat_pressed():
    pass