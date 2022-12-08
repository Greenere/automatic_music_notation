import numpy as np
import time
from enum import Enum

from recording import record_long_piece, extract_pieces, write_piece
from controller import start_pressed, pause_pressed, end_pressed, quit_pressed, beat_pressed

####### Recording ########
"""
Control Panal:
- GPIO #17 (The First Button): Start/Continue Recording
- GPIO #22 (The Second Button): Pause Recording
- GPIO #23 (The Third Button): End Recording
- GPIO #27 (The Last Button): Quit
"""
# Technically, we use status flags to indicate the states of the microphone
class Status(Enum):
    START_PRESSED = 1
    PAUSE_PRESSED = 2
    CONTINUE_PRESSED = 3
    END_PRESSED = 4
# This is the maximal length of a recording
long_seconds = 600
# This is the piece counter
melody_count = 0
# This is the status of the recording program
status = Status.END_PRESSED
while True:
    # Idle mode, it can either start or quit
    if quit_pressed():
        print("Quit the entire program")
        exit(0)
    if start_pressed():
        print("Start recording...")
        # Start a long recording process in the background
        start_time = time.time()
        piece = record_long_piece(long_seconds)
        status = Status.START_PRESSED
    if status != Status.START_PRESSED:
        continue
    
    # Started mode, it can either pause, resume, or quit
    paused = False
    event_secs = [("start", 0)]
    while status == Status.START_PRESSED:
        if quit_pressed():
            print("Quit the entire program")
            exit(0)
        
        if end_pressed():
            end_time = time.time()
            print("End the recording after %f seconds"%(end_time - start_time))
            status = Status.END_PRESSED
        
        # Time out equals to an end_pressed()
        if time.time() - start_time >= long_seconds:
            end_time = time.time()
            print("End the recording due to time out (%f seconds)"%(end_time - start_time))
            status = Status.END_PRESSED
        
        # The `paused` is used to debounce the buttons
        if pause_pressed() and not paused:
            pause_time = time.time()
            print("Pause the recording after %f seconds" % (pause_time - start_time))
            event_secs.append(("pause", pause_time-start_time))
            paused = True
        
        if start_pressed() and paused:
            resume_time = time.time()
            print("Resume the recording after %f seconds" % (resume_time - start_time))
            event_secs.append(("resume", resume_time-start_time))
            paused = False
    
    if status == Status.END_PRESSED:
        event_secs.append(("end", end_time - start_time))
        final_piece = extract_pieces(piece, event_secs)
        write_piece(final_piece, "melody_%d.wav"%(melody_count))
        melody_count += 1
        event_secs = []

####### Pitch dectection ########






####### Output to notation ########







####### Interaction with Pi ########
# Button1: start recording
# Button2: pause / continue
# Button3: end
# Button4: quit