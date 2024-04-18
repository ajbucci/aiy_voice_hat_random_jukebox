#!/usr/bin/env python
import os
import subprocess
import time
import random
import RPi.GPIO as GPIO

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)

# Variables to manage playback
is_playing = False
player_process = None
SLEEP_TIMER = 15 * 60  # 15 minutes

# Set system volume
os.system('pactl -- set-sink-volume 0 20%')

def play_random_mp3():
    """Play a random MP3 file in loop until stopped."""
    music_dir = "/home/aj/Music/"
    random_file = random.choice([f for f in os.listdir(music_dir) if f.endswith('.mp3')])
    file_path = os.path.join(music_dir, random_file)
    # Loop the same song indefinitely
    return subprocess.Popen(['mpg123', '--loop', '-1', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Main loop
try:
    end_time = None
    while True:
        if not GPIO.input(23):  # Button is pressed
            if is_playing:
                if player_process:
                    player_process.terminate()  # Terminate the current playing process
                    player_process = None
                    end_time = None
                print("Playback stopped")
            else:
                player_process = play_random_mp3()
                end_time = time.time() + SLEEP_TIMER
                print("Playing music")
            is_playing = not is_playing  # Toggle the playing state

        if is_playing and end_time and time.time() > end_time:
            if player_process:
                player_process.terminate()  # Terminate due to timeout
                player_process = None
                end_time = None
                is_playing = False
                print("Playback stopped due to timeout")

        time.sleep(0.1)  # Small delay to debounce and reduce CPU usage
finally:
    GPIO.cleanup()  # Clean up GPIO on exit
    if player_process:
        player_process.terminate()  # Ensure music stops on script exit
