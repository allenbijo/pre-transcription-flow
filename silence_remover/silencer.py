import torchaudio
import torch

def run_silence_remover(waveform, sample_rate=16000, silence_threshold=-40.0, chunk_size=1024, min_silence_duration=0.3):
    if waveform.ndim == 1:
        waveform = waveform[None, :]

    waveform = torch.Tensor(waveform)
    # Convert to mono
    if waveform.size(0) > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)

    # Calculate dB levels for chunks
    def calculate_db(chunk):
        rms = torch.sqrt(torch.mean(chunk**2))
        return 20 * torch.log10(rms + 1e-6)

    min_silence_samples = int(min_silence_duration * sample_rate)  # Minimum silence duration in samples
    non_silent_parts = []

    current_silence_start = None
    for i in range(0, waveform.size(1), chunk_size):
        start = i
        end = min(start + chunk_size, waveform.size(1))
        chunk = waveform[:, start:end]

        # Check if chunk is below the silence threshold
        if calculate_db(chunk) <= silence_threshold:
            if current_silence_start is None:
                current_silence_start = start
        else:
            # If the silence was long enough, skip it
            if current_silence_start is not None:
                silence_duration = start - current_silence_start
                if silence_duration < min_silence_samples:
                    # If silence is too short, include it
                    silent_chunk = waveform[:, current_silence_start:start]
                    non_silent_parts.append(silent_chunk)
                current_silence_start = None
            non_silent_parts.append(chunk)

    # Handle trailing silence
    if current_silence_start is not None:
        silence_duration = waveform.size(1) - current_silence_start
        if silence_duration < min_silence_samples:
            silent_chunk = waveform[:, current_silence_start:]
            non_silent_parts.append(silent_chunk)

    # Combine non-silent parts
    if non_silent_parts:
        output_waveform = torch.cat(non_silent_parts, dim=1)
    else:
        # No non-silent parts, return empty audio
        output_waveform = torch.zeros((1, 0))
    
    output_waveform_np = output_waveform.numpy()
    return output_waveform_np
