import playsound
import logging

async def play_sound(sound_file):
    try:
        playsound(sound_file)
    except Exception as e:
        logging.error(f"Error playing sound: {e}")