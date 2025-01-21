from utils.audio_utils import load_and_resample
import numpy as np


def add_noise(data, sr):
    noise_clip, _ = load_and_resample('helpers/noise_maker/assets_cafe_short.wav', sr)
    
    snr = 2

    noise_clip = noise_clip / snr

    if len(noise_clip) < len(data):
        noise_clip = np.tile(noise_clip, int(np.ceil(len(data) / len(noise_clip))))
        noise_clip = noise_clip[:len(data)]

    if data.ndim > 1:
        noise_clip = np.stack([noise_clip, noise_clip], axis=-1)

    audio_clip_cafe = data + noise_clip

    return audio_clip_cafe