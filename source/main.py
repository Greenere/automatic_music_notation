import numpy as np
import time
import enum

from pitch_detection import pitch_detection, write_pitch, pitch_detection_multi_channel
from recording import record_long_piece, extract_pieces, write_piece
from controller import start_pressed, pause_pressed, end_pressed, quit_pressed, beat_pressed
from controller import beat_pressed
from logger import log_info, log_warning, log_debug
from notation import generate_lilypond_source_file, generate_music_notation

####### Recording ########
"""
Control Panal:
- GPIO #17 (The First Button): Start/Continue Recording
- GPIO #22 (The Second Button): Pause Recording
- GPIO #23 (The Third Button): End Recording
- GPIO #27 (The Last Button): Quit
"""
# Technically, we use status flags to indicate the states of the microphone


class STATUS(enum.Enum):
    START_PRESSED = 1
    PAUSE_PRESSED = 2
    END_PRESSED = 3


# This is the maximal length of a recording
long_seconds = 600
# This is the piece counter
melody_count = 0
# This is the sample rate
sample_rate = 44100
# This is the status of the recording program
status = STATUS.END_PRESSED
while True:
    # Idle mode, it can either start or quit
    if quit_pressed():
        log_info("Quit the entire program")
        exit(0)
    if start_pressed():
        log_info("Start recording...")
        # Start a long recording process in the background
        start_time = time.time()
        piece = record_long_piece(long_seconds)
        status = STATUS.START_PRESSED
    if status != STATUS.START_PRESSED:
        continue

    # Started mode, it can either pause, resume, or quit
    paused = False
    event_secs = [("start", 0)]
    beat_secs = [0]
    while status == STATUS.START_PRESSED:
        if quit_pressed():
            log_info("Quit the entire program")
            exit(0)

        if end_pressed():
            end_time = time.time()
            log_info("End the recording after %f seconds" %
                  (end_time - start_time))
            status = STATUS.END_PRESSED

        # Time out equals to an end_pressed()
        if time.time() - start_time >= long_seconds:
            end_time = time.time()
            log_info("End the recording due to time out (%f seconds)" %
                  (end_time - start_time))
            status = STATUS.END_PRESSED

        # The `paused` is used to debounce the buttons
        if pause_pressed() and not paused:
            pause_time = time.time()
            log_info("Pause the recording after %f seconds" %
                  (pause_time - start_time))
            event_secs.append(("pause", pause_time-start_time))
            paused = True

        if start_pressed() and paused:
            resume_time = time.time()
            log_info("Resume the recording after %f seconds" %
                  (resume_time - start_time))
            event_secs.append(("resume", resume_time-start_time))
            paused = False

        if beat_pressed():
            beat_secs.append(time.time() - start_time - beat_secs[-1])

    if status == STATUS.END_PRESSED:
        log_debug("Recorded beats: %s"%(str(beat_secs)))
        event_secs.append(("end", end_time - start_time))
        final_piece = extract_pieces(piece, event_secs)
        write_piece(final_piece, "melody_%d.wav" % (melody_count))

        try:
            # Pitch detection should be invoked here
            beat_itv_length = len(beat_secs) - 1
            beat_itv =  sum(beat_secs) / beat_itv_length
        except ZeroDivisionError:
            log_warning("No beat detected")
        
        log_info("Start creating the music notation")
        print("Length of the Final Piece: %d" %len(final_piece))

        pitches = pitch_detection("melody_%d.wav" % (melody_count), beat_itv, sample_rate)
        print("Length of beat intervals %d" %beat_itv_length)
        print("Length of pitches %d" %len(pitches))
        log_debug("Detected pitches: %s"%(str(pitches)))
        write_pitch(pitches, "pitches_%d" % (melody_count))

        # Output to notation
        generate_lilypond_source_file(pitches, "melody_%d.wav" % (melody_count))
        #generate_music_notation("melody_%d.wav" % (melody_count))

        melody_count += 1
        event_secs = []
        beat_secs = []


####### Interaction with Pi ########
# Button1: start recording
# Button2: pause / continue
# Button3: end
# Button4: quit
