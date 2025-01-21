from scipy.io import wavfile
import numpy as np

# Provide the path to your audio file (ensure it's a WAV file)

##for testing
# file_path = "assets_cafe_short.wav"  # Replace with your audio file path

# Load the audio file

##uncomment for testing
# sample_rate, waveform = wavfile.read(file_path)

# Convert to a NumPy array (float32 for consistency)
def calculate_time(waveform,sample_rate):
    waveform = np.array(waveform, dtype=np.float32)
    duration = len(waveform) / sample_rate
    return duration


#uncomment for testing
# print(calculate_time(waveform,sample_rate))