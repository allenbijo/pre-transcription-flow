import torch
import torch.nn.functional as F
from pesq import pesq


def pad_waveforms(waveform1, waveform2):
    max_length = max(waveform1.size(1), waveform2.size(1))
    waveform1 = F.pad(waveform1, (0, max_length - waveform1.size(1)))
    waveform2 = F.pad(waveform2, (0, max_length - waveform2.size(1)))
    return waveform1, waveform2

def normalize_waveform(waveform):
    return waveform / torch.max(torch.abs(waveform))

def calculate_psnr(waveform1, waveform2):
    mse = F.mse_loss(waveform1, waveform2)
    if mse == 0:
        return float('inf')
    max_signal = torch.max(waveform1)
    psnr = 20 * torch.log10(max_signal / torch.sqrt(mse))
    return psnr.item()

def calculate_pesq(waveform1, waveform2, sample_rate):
    pesqw = pesq(sample_rate, waveform1, waveform2, 'wb')
    pesqn = pesq(sample_rate, waveform1, waveform2, 'nb')
    return pesqw, pesqn

def run_metric(waveform1, waveform2, sample_rate):
    waveform1 = torch.Tensor(waveform1)
    waveform2 = torch.Tensor(waveform2)
    
    waveform1, waveform2 = pad_waveforms(waveform1, waveform2)

    waveform1 = normalize_waveform(waveform1)
    waveform2 = normalize_waveform(waveform2)

    psnr = calculate_psnr(waveform1, waveform2)
    pesqw, pesqn = calculate_pesq(waveform1, waveform2, sample_rate)

    return psnr, pesqw, pesqn