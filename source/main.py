import numpy as np
import time

from recording import record_short_piece, record_long_piece, write_piece
from controller import start_pressed, pause_pressed, end_pressed, quit_pressed

####### Recording ########
"""
Control Panal:
- GPIO #17 (The First Button): Start Recording
- GPIO #22 (The Second Button): Pause / Continue Recording
- GPIO #23 (The Third Button): End Recording
- GPIO #27 (The Last Button): Quit
"""
# This is the interval of control polling
long_seconds = 600
short_seconds = 0.2
started = False
event_times = []
while True:
    # Idle mode, it can either start or quit
    if quit_pressed():
        print("Quit the entire program")
        exit(0)
    if start_pressed():
        if not started:
            print("Start recording...")
            total_length = 0
            status = 0
            started = True
    if not started:
        continue
    event_times.append(("start", time.time()))
    
    # Started mode, it can either pause, resume, or quit
    while status == 0:
        piece = record_long_piece(short_seconds)
        total_length += 1
      
        if quit_pressed():
            print("Quit the entire program")
            exit(0)
        
        if end_pressed():
            status = 1
            break
        
        if pause_pressed() and not start_pressed():
            print("Pause the recording after %f seconds"%(total_length*short_seconds))
            status = 2
            break
    
    if end_pressed() or status == 1:
        # Merge pieces, and save it to a wav file
        print("Finish the recording (%f seconds)"%(total_length*short_seconds))
        if len(pieces) > 0:
            large_piece = np.vstack(pieces)
            write_piece(large_piece, "melody.wav")
        else:
            print("Nothing is recorded")

        total_length = 0
        started = False
    
    if pause_pressed() and start_pressed():
        # Press the puase button again, it will resume
        print("Resume the recording")
        status = 0


####### Pitch dectection ########






####### Output to notation ########







####### Interaction with Pi ########
# Button1: start recording
# Button2: pause / continue
# Button3: end
# Button4: quit