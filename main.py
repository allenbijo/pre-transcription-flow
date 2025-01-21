from utils.audio_utils import load_and_resample, save_audio
from base_denoiser.base_denoiser import run_base_denoiser
from silence_remover.silencer import run_silence_remover
from ai_denoiser.ai_denoiser import run_ai_denoiser


audio, sr = load_and_resample('audio (1).wav', 16000)
denoised_audio = run_base_denoiser(audio, sr, denoiser='nr-lib', version=1)
silenced_audio = run_silence_remover(denoised_audio, sr, silence_threshold=-100.0, chunk_size=1024, min_silence_duration=0.3)
ai_denoised_audio = run_ai_denoiser(denoised_audio, sr, denoiser='facebook', version=48)
save_audio(silenced_audio, sr, 'denoised_audio.wav')
