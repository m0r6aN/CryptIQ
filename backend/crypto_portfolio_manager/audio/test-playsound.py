import time
import playsound
import os

FINISHED_SOUND_FILE = 'tada.mp3'
EXIT_FOUND_SOUND = 'windows-critical-stop.mp3'

def play_sound(file_path):
    print(f"Attempting to play: {file_path}")
    if os.path.exists(file_path):
        print(f"File exists: {file_path}")
        try:
            playsound.playsound(file_path)
            print(f"Successfully played: {file_path}")
        except Exception as e:
            print(f"Error playing {file_path}: {e}")
    else:
        print(f"File does not exist: {file_path}")

if __name__ == '__main__':
    print(f"Current working directory: {os.getcwd()}")
    play_sound(FINISHED_SOUND_FILE)
    time.sleep(0.25)
    play_sound(EXIT_FOUND_SOUND)