# Denoising using facebook denoiser

import torch
import torchaudio
import torch.nn.functional as F
from denoiser import pretrained
from denoiser.dsp import convert_audio


model_d = None
model_d2 = None

def facebook64_denoise(wav, sr):
    global model_d
    
    if model_d == None:
        model_d = pretrained.dns64().cuda()

    wav = convert_audio(wav.cuda(), sr, model_d.sample_rate, model_d.chin)
    
    with torch.no_grad():
        denoised = model_d(wav[None])[0]
    denoised = convert_audio(denoised, model_d.sample_rate, sr, model_d.chin)
    denoised = F.pad(denoised, (0, 1), "constant", 0)
    
    return denoised.cpu()

def facebook48_denoise(wav, sr):
    global model_d2
    
    if model_d2 == None:
        model_d2 = pretrained.dns48().cuda()

    wav = convert_audio(wav.cuda(), sr, model_d2.sample_rate, model_d2.chin)
    
    with torch.no_grad():
        denoised = model_d2(wav[None])[0]
    denoised = convert_audio(denoised, model_d2.sample_rate, sr, model_d2.chin)
    denoised = F.pad(denoised, (0, 1), "constant", 0)

    return denoised.cpu()