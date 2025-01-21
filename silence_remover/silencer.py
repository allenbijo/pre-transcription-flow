import torchaudio
import torch
import numpy as np

def remove_silence(audio_path, output_path, silence_threshold=-40.0, chunk_size=1024, sample_rate=16000):
    # Load audio file
    waveform, sr = torchaudio.load(audio_path)
    
    # Resample if needed
    if sr != sample_rate:
        resampler = torchaudio.transforms.Resample(sr, sample_rate)
        waveform = resampler(waveform)
    
    # Convert to mono
    if waveform.size(0) > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)

    # Calculate dB levels for chunks
    def calculate_db(chunk):
        rms = torch.sqrt(torch.mean(chunk**2))
        return 20 * torch.log10(rms + 1e-6)
    
    non_silent_parts = []
    total_chunks = waveform.size(1) // chunk_size

    for i in range(total_chunks):
        start = i * chunk_size
        end = start + chunk_size
        chunk = waveform[:, start:end]

        # Check if chunk is above threshold
        if calculate_db(chunk) > silence_threshold:
            non_silent_parts.append(chunk)
    
    # Combine non-silent parts
    if non_silent_parts:
        output_waveform = torch.cat(non_silent_parts, dim=1)
    else:
        # No non-silent parts, return empty audio
        output_waveform = torch.zeros((1, 0))

    # Save the resulting audio
    torchaudio.save(output_path, output_waveform, sample_rate)

# Example usage
input_file = "audio.wav"
output_file = "output_audio_no_silence.wav"
remove_silence(input_file, output_file, silence_threshold=-40.0, chunk_size=1024, sample_rate=16000)
