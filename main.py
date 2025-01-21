from utils.audio_utils import load_and_resample, save_audio
from base_denoiser.base_denoiser import run_base_denoiser
from silence_remover.silencer import run_silence_remover
from ai_denoiser.ai_denoiser import run_ai_denoiser

from helpers.noise_maker.noise_adder import add_noise
from helpers.scoring.scorer import run_metric
from helpers.scoring.time_calculator import calculate_time
import time
import os
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

# clean_audios = ['./test_audios/'+entry for entry in os.listdir('./test_audios') if os.path.isfile(os.path.join('./test_audios', entry))]
# print(clean_audios)
# for clean_audio in clean_audios:
#     audio, sr = load_and_resample(clean_audio, 16000)
#     noisy_audio = add_noise(audio, sr, snr=1)
#     save_audio(noisy_audio, sr, f'./noisy_audios/{clean_audio.split("/")[-1]}')


noisy_audios = [entry for entry in os.listdir('./noisy_test_audios') if os.path.isfile(os.path.join('./noisy_test_audios', entry))]
base_dens = ['nr-lib', 'pedalboard', 'None']
silence_pos = [False]
ai_dens = ['None']
for noisy_audio in noisy_audios:
    for base_den in base_dens:
        for silence_po in silence_pos:
            for ai_den in ai_dens:
                start_time = time.time()
                audio, sr = load_and_resample('./noisy_test_audios/'+noisy_audio, 16000)
                denoised_audio = run_base_denoiser(audio, sr, denoiser=base_den, version=0)
                if silence_po:
                    silenced_audio = run_silence_remover(denoised_audio, sr, silence_threshold=-50.0, chunk_size=1024, min_silence_duration=0.3)
                else:
                    silenced_audio = denoised_audio
                ai_denoised_audio = run_ai_denoiser(silenced_audio, sr, denoiser=ai_den)
                save_audio(ai_denoised_audio, sr, f'./denoised_test_audios/{noisy_audio.split(".")[0]}_{base_den}_{silence_po}_{ai_den}.wav')
                # print(f'{noisy_audio}_{base_den}_{silence_po}_{ai_den[0]}_{ai_den[1]}.wav')
                end_time = time.time()
                
                clean_audio, _ = load_and_resample('./test_audios/'+noisy_audio, 16000)
                inference_time = end_time - start_time
                print('here')
                psnr, pesqw, pesqn = run_metric(clean_audio, ai_denoised_audio, sr)
                print('here')
                audio_time = calculate_time(audio, sr)
                trimmed_time = calculate_time(ai_denoised_audio, sr)
                print('here')
                current_data = [noisy_audio, base_den, silence_po, ai_den, psnr, pesqw, pesqn, inference_time, audio_time, trimmed_time]
                data.append(current_data)
                print(current_data)
                
df = pd.DataFrame(data, columns=headers)
df.to_csv('results.csv', index=False)

