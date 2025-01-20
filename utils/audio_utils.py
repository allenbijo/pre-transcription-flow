import torch
import torchaudio

def load_and_resample(audio_path, target_sample_rate=None):
    waveform, sample_rate = torchaudio.load(audio_path)
    if target_sample_rate and sample_rate != target_sample_rate:
        waveform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=target_sample_rate)(waveform)
        sample_rate = target_sample_rate
    return waveform[-1,:].numpy(), sample_rate

def save_audio(waveform, sample_rate, output_path):
    if waveform.ndim == 1:
        waveform = waveform[None, :]
    torchaudio.save(output_path, torch.Tensor(waveform), sample_rate)