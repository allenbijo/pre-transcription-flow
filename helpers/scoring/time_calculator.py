import numpy as np


def calculate_time(waveform, sample_rate):
    waveform = np.array(waveform, dtype=np.float32)
    duration = len(waveform) / sample_rate
    return duration
