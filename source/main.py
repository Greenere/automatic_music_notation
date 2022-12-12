import time
import enum

from controller import start_pressed, pause_pressed, end_pressed, quit_pressed, beat_pressed
from exchange import leave_message
from logger import log_info, log_warning, log_debug
from notation import compose_pitches, write_music, export_music
from pitch_detection import pitch_detection, write_pitch
from pitch_detection import pitch_duration_detection, clef_detection,wave_plot
from recording import record_long_piece, extract_pieces, write_piece, _SAMPLE_RATE

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

_RESUlT_PATH = "./results"
def name2path(filename: str) -> str:
    return "%s/%s"%(_RESUlT_PATH, filename)

# The length of the visualized period
vis_sec = 2
# Assuming one beat is a quarter length
beat_base = 4
# This is the maximal length of a recording
long_seconds = 600
# This is the piece counter
melody_count = 0
# This is the sample rate
sample_rate = _SAMPLE_RATE
# This is the status of the recording program
status = STATUS.END_PRESSED
log_info("Start the program, sample_rate: %d /s, max recording: %d s"%(sample_rate, long_seconds))
while True:
    # Idle mode, it can either start or quit
    if quit_pressed():
        log_info("Quit the entire program")
        exit(0)
    if start_pressed():
        log_info("Start recording...")
        # Start a long recording process in the background
        start_time = time.time()
        last_time = start_time
        piece = record_long_piece(long_seconds)
        # Set the initial states
        paused = False
        event_secs = [("start", 0)]
        beat_secs = [0]
        status = STATUS.START_PRESSED
    if status != STATUS.START_PRESSED:
        continue

    # Started mode, it can either pause, resume, or quit
    while status == STATUS.START_PRESSED:
        cur_time = time.time()
        if (cur_time - last_time) > vis_sec:
            if (cur_time - start_time) < vis_sec:
                wave_plot(piece, start_time, sample_rate, beat_secs, cur_time - start_time)
            else:
                wave_plot(piece, cur_time - start_time - vis_sec, sample_rate, beat_secs, vis_sec)
            last_time = cur_time
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
            beat_secs.append(time.time() - start_time)

    if status == STATUS.END_PRESSED:
        # Extract beat, and beat durations
        log_debug("Recorded beats: %s"%(str(beat_secs)))
        beat_itv_length = len(beat_secs) - 1
        if beat_itv_length < 1:
            log_warning("No beat recorded, using 0.5s as default")
            beat_itv_length = int((end_time - start_time)*2)
            beat_itvs = [0.5]*beat_itv_length
            beat_secs.append(0.5)
        else:
            beat_itvs = []
            for i in range(beat_itv_length):
                beat_itvs.append(beat_secs[i+1] - beat_secs[i])

        # Align the events with beats
        event_secs[0] = ('start', beat_secs[1] - beat_itvs[0]/2)
        event_secs.append(("end", end_time - start_time))
        # Cut and concatenate the recordings according to events
        final_piece = extract_pieces(piece, event_secs)
        log_debug("Length of the Final Piece: %d" %len(final_piece))
        # Save the recording
        write_piece(final_piece, name2path("melody_%d.wav" % (melody_count)))
        
        log_info("Start creating the music notation")

        # Extract the raw pitches
        pitches = pitch_detection(name2path("melody_%d.wav" % (melody_count)), beat_itvs, sample_rate)
        log_debug("Length of beat intervals %d" %beat_itv_length)
        log_debug("Length of pitches %d" %len(pitches))
        log_debug("Detected pitches: %s"%(str(pitches)))
        # Save the extracted pitches
        write_pitch(pitches, name2path("pitches_%d" % (melody_count)))

        # Post-processing the pitches according to the beat base
        pitches, durations = pitch_duration_detection(beat_base, pitches)
        log_debug("Durations: %s"%(str(durations)))

        # Determine the clef according to pitches
        clef = clef_detection(pitches)

        # Compose the pitches
        stream = compose_pitches(clef, pitches, durations)

        # Write the note stream and export it into a svg
        write_music(stream, name2path("melody_%d"%(melody_count)))
        export_music(stream, "melody_%d"%(melody_count))

        # Plot the last piece of wave
        wave_plot(piece, end_time - start_time - vis_sec, sample_rate, beat_secs, vis_sec)

        leave_message("update", 2)

        #melody_count += 1
