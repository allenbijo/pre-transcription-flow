from resemble_enhance.enhancer.inference import denoise
import torch
import torchaudio


def resemble_denoise(dwav, sr):
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"

    dwav = dwav.mean(dim=0)
    wav1, new_sr = denoise(dwav, sr, device)
    wav1 = torchaudio.transforms.Resample(orig_freq=new_sr, new_freq=sr)(wav1)
    wav1 = wav1.cpu().numpy()
    return wav1

def run_resemble_denoise(audio, sr):
    """
    Run the resemble denoiser.

    :param audio: The audio to denoise.
    :type audio: np.ndarray
    :param sr: The sample rate of the audio.
    :type sr: int
    
    Returns:
        denoised_audio: Audio after denoising
    """
    audio = torch.Tensor(audio)
    return resemble_denoise(audio, sr)