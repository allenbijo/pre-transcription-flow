from utils.audio_utils import load_and_resample, save_audio
from base_denoiser.base_denoiser import run_base_denoiser
from silence_remover.silencer import run_silence_remover
from ai_denoiser.ai_denoiser import run_ai_denoiser

from helpers.noise_maker.noise_adder import add_noise
from helpers.scoring.scorer import run_metric
import time
import pandas as pd


# audio, sr = load_and_resample('test_audios/audio (1).wav', 16000)
# noisy = add_noise(audio, sr)
# # denoised_audio = run_base_denoiser(audio, sr, denoiser='nr-lib', version=1)
# # silenced_audio = run_silence_remover(denoised_audio, sr, silence_threshold=-100.0, chunk_size=1024, min_silence_duration=0.3)
# # ai_denoised_audio = run_ai_denoiser(denoised_audio, sr, denoiser='facebook', version=48)
# save_audio(noisy, sr, 'denoised_audio.wav')

headers = [
    "AudioFile", "BaseDenoiser", "Silenced", "AiDenoiser",
    "PSNR", "PESQ(WB)", "PESQ(NB)", "InferenceTime", "AudioTime", "TrimmedTime"
]

data = []

noisy_audios = ['1', '2', '3']
base_dens = ['nr-lib', 'pedalboard', 'None']
silence_pos = [True, False]
ai_dens = ['facebook64', 'facebook48', 'None']
for noisy_audio in noisy_audios:
    for base_den in base_dens:
        for silence_po in silence_pos:
            for ai_den in ai_dens:
                # audio, sr = load_and_resample(f'test_audios/{noisy_audio}', 16000)
                # denoised_audio = run_base_denoiser(audio, sr, denoiser=base_den, version=0)
                # if silence_po:
                #     silenced_audio = run_silence_remover(denoised_audio, sr, silence_threshold=-100.0, chunk_size=1024, min_silence_duration=0.3)
                # else:
                #     silenced_audio = denoised_audio
                # ai_denoised_audio = run_ai_denoiser(silenced_audio, sr, denoiser=ai_den)
                # save_audio(ai_denoised_audio, sr, f'{audio}_{base_den}_{silence_po}_{ai_den[0]}_{ai_den[1]}.wav')
                # print(f'{noisy_audio}_{base_den}_{silence_po}_{ai_den[0]}_{ai_den[1]}.wav')
                psnr, pesqw, pesqn = run_metric(audio, ai_denoised_audio, sr)
                current_data = [noisy_audio, base_den, silence_po, ai_den, psnr, pesqw, pesqn, 0, 0, 0]
                data.append(current_data)
                print(current_data)
                
df = pd.DataFrame(data, columns=headers)
df.to_csv('results.csv', index=False)

