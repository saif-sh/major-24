# audio_handler.py

import os
import sounddevice as sd
import soundfile as sf
from datetime import datetime
from config import SAMPLE_RATE, CHANNELS, AUDIO_FORMAT, RECORDINGS_DIR

class AudioHandler:
    def __init__(self):
        self.filename = None
        if not os.path.exists(RECORDINGS_DIR):
            os.makedirs(RECORDINGS_DIR)

    def record_audio(self, duration):
        """Records audio for a specified duration and saves it to a file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = os.path.join(RECORDINGS_DIR, f"recorded_audio_{timestamp}.{AUDIO_FORMAT}")
        print(f"Recording to {self.filename}...")
        audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS)
        sd.wait()  # Wait until recording is finished
        sf.write(self.filename, audio, SAMPLE_RATE)
        print("Recording complete.")

    def play_back_audio(self):
        """Plays back the recorded audio."""
        if self.filename and os.path.exists(self.filename):
            data, samplerate = sf.read(self.filename)
            sd.play(data, samplerate)
            sd.wait()
        else:
            raise FileNotFoundError("No audio recorded yet.")

    def clear_recording(self):
        """Deletes the recorded audio file."""
        if self.filename and os.path.exists(self.filename):
            os.remove(self.filename)
            self.filename = None
            print("Recording cleared.")
        else:
            raise FileNotFoundError("No recordings to clear.")
     