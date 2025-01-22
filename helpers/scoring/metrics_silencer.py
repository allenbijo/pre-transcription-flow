import torchaudio
import torch

def normalize_waveform(waveform):
    return waveform / torch.max(torch.abs(waveform))

def detect_non_silent_segments(waveform, sample_rate=16000, silence_threshold=-40.0, chunk_size=1024, min_silence_duration=0.3):
    if waveform.ndim == 1:
        waveform = waveform[None, :]  # Add channel dimension if mono

    waveform = torch.Tensor(waveform)

    # Convert to mono
    if waveform.size(0) > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)

    waveform = normalize_waveform(waveform)
    
    # Calculate dB levels for chunks
    def calculate_db(chunk):
        rms = torch.sqrt(torch.mean(chunk**2))
        return 20 * torch.log10(rms + 1e-6)

    min_silence_samples = int(min_silence_duration * sample_rate)  # Minimum silence duration in samples
    non_silent_segments = []

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
            # If silence was long enough, skip it
            if current_silence_start is not None:
                silence_duration = start - current_silence_start
                if silence_duration >= min_silence_samples:
                    current_silence_start = None
            non_silent_segments.append((start, end))

    # Handle trailing silence
    if current_silence_start is not None:
        silence_duration = waveform.size(1) - current_silence_start
        if silence_duration < min_silence_samples:
            non_silent_segments.append((current_silence_start, waveform.size(1)))

    return non_silent_segments

def apply_segments_to_audio(waveform, segments):
    if waveform.ndim == 1:
        waveform = waveform[None, :]  # Add channel dimension if mono

    waveform = torch.Tensor(waveform)
    
    non_silent_parts = [waveform[:, start:end] for start, end in segments]
    if non_silent_parts:
        output_waveform = torch.cat(non_silent_parts, dim=1)
    else:
        output_waveform = torch.zeros((1, 0))  # Return empty audio if no segments
    return output_waveform.numpy()

def silence(audio1_waveform, audio2_waveform, sample_rate=16000, silence_threshold=-40.0, chunk_size=1024, min_silence_duration=0.3):
    # Detect non-silent segments from audio1
    segments = detect_non_silent_segments(audio1_waveform, sample_rate, silence_threshold, chunk_size, min_silence_duration)
    
    # Apply these segments to audio2
    processed_audio2 = apply_segments_to_audio(audio2_waveform, segments)
    return processed_audio2

# Example Usage:
# waveform1, sr1 = torchaudio.load("testing_denoised.wav")
# waveform2, sr2 = torchaudio.load("noisy_test_audios/audio2.wav")
# assert sr1 == sr2, "Sample rates of both audios must match."

# processed_audio2 = process_audio_pair(waveform1, waveform2, sample_rate=sr1)
# torchaudio.save("processed_audio2.wav", torch.Tensor(processed_audio2), sr1)
