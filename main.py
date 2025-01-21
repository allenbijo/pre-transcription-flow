from utils.audio_utils import load_and_resample, save_audio
from base_denoiser.base_denoiser import run_base_denoiser
from ai_denoiser.ai_denoiser import run_ai_denoiser
# from audio_processor import remove_silence

audio, sr = load_and_resample('noised_audio.wav', 16000)
denoised_audio = run_base_denoiser(audio, sr, denoiser='pedalboard', version=1)
ai_denoised_audio = run_ai_denoiser(denoised_audio, sr, denoiser='facebook', version=64)
save_audio(ai_denoised_audio, sr, 'denoised_audio.wav')
# remove_silence('audio.wav', 'unsilence.wav')