from utils.audio_utils import load_and_resample, save_audio
from helpers.noise_maker.noise_adder import add_noise


audio, sr = load_and_resample('test_audios/audio2.wav', 16000)
noisy = add_noise(audio, sr)
save_audio(noisy, sr, 'denoised_audio.wav')