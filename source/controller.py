"""
Functions that connect the buttons and touchscreen to the main program
- Checking handles to decide whether a button is pressed or not
- Pygame codes that draw a music symbol
- Checking handle to decide whether the music symbol is touched or not
Control Panal Design:
- GPIO #17 (The First Button): Start/Continue Recording
- GPIO #22 (The Second Button): Pause Recording
- GPIO #23 (The Third Button): End Recording
- GPIO #27 (The Last Button): Quit
"""

import RPi.GPIO as GPIO
import pygame
import os

_START = 17
_PAUSE = 22
_END = 23
_QUIT = 27
_WIDTH = 320
_HEIGHT = 240
_IMAGE_PATH = "source/music_symbol.jpg"
_SIZE = 100
_RED = (255, 0, 0)
_WHITE = (255, 255, 255)

os.putenv('SDL_VIDEODRIVER', 'fbcon')  # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb0')
os.putenv('SDL_MOUSEDRV', 'TSLIB')  # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()
pygame.mouse.set_visible(False)

width, height = _WIDTH, _HEIGHT
size = (width, height)
screen = pygame.display.set_mode(size)
screen.fill(_WHITE)


def mouse_on_button(mouse, rect):
    x, y, width, height = rect.centerx, rect.centery, rect.w, rect.h
    return (x - width//2 < mouse[0] < x + width//2) and \
           (y - height//2 < mouse[1] < y + height//2)


def get_music_note_symbol(image_path, size, x, y):
    music_note_symbol = pygame.image.load(image_path)
    music_note_symbol = pygame.transform.scale(music_note_symbol, [size, size])
    music_note_symbol_rect = music_note_symbol.get_rect()
    music_note_symbol_rect = music_note_symbol_rect.move([int(x), int(y)])
    return music_note_symbol, music_note_symbol_rect


def draw_boundary(rect, color):
    x, y, width, height = rect.centerx, rect.centery, rect.w, rect.h
    vertex = [(x - width//2, y - height//2),
              (x - width//2, y + height//2),
              (x + width//2, y + height//2),
              (x + width//2, y - height//2)]
    boundary = pygame.draw.lines(screen, color, True, vertex, 3)
    return boundary

# Warning: draw a large number of lines, need to be optimize


def highlight(rect):
    draw_boundary(rect, _RED)
    pygame.display.flip()


def resume(rect):
    draw_boundary(rect, _WHITE)
    pygame.display.flip()


music_note_symbol, music_note_symbol_rect = get_music_note_symbol(
    _IMAGE_PATH, _SIZE, _WIDTH / 3, _HEIGHT / 3)
screen.blit(music_note_symbol, music_note_symbol_rect)
pygame.display.flip()

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

# The funciton will be invoked in the whole process loop


def beat_pressed() -> bool:
    is_pressed = False
    for ev in pygame.event.get():

        mouse_pos = pygame.mouse.get_pos()
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit()

        if mouse_on_button(mouse_pos, music_note_symbol_rect):
            if ev.type == pygame.MOUSEBUTTONDOWN:
                is_pressed = True
                highlight(music_note_symbol_rect)
                pygame.display.flip()
            if ev.type == pygame.MOUSEBUTTONUP:
                resume(music_note_symbol_rect)

    return is_pressed
