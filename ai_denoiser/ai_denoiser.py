from .src.facebook_denoiser import facebook64_denoise, facebook48_denoise
# from .src.resemble_denoiser import resemble_denoise
import torch

def run_facebook_denoiser(audio, sr, version=0):
    """
    Run the facebook denoiser.

    :param denoiser: The denoiser to run.
    :type denoiser: str
    """
    
    if audio.ndim == 1:
        audio = audio[None, :]
    
    audio = torch.Tensor(audio)
    
    if version==64:
        return facebook64_denoise(audio, sr)
    elif version==48:
        return facebook48_denoise(audio, sr)
    else:
        raise ValueError(f'Unknown facebook denoiser version: {version}')

def run_resemble_denoiser(audio, sr, version=0):
    """
    Run the resemble denoiser.

    :param denoiser: The denoiser to run.
    :type denoiser: str
    """
    
    if audio.ndim == 1:
        audio = torch.Tensor(audio[None, :])
    
    audio = torch.Tensor(audio)
    
    return resemble_denoise(audio, sr)

def run_ai_denoiser(audio, sr, denoiser='None'):
    """
    Run the AI denoiser.

    :param denoiser: The denoiser to run.
    :type denoiser: str
    """
    
    if denoiser=='None':
        return audio
    
    elif denoiser=='facebook64':
        denoised = run_facebook_denoiser(audio, sr, 64)
        return denoised[-1,:].numpy()
    
    elif denoiser=='facebook48':
        denoised = run_facebook_denoiser(audio, sr, 48)
        return denoised[-1,:].numpy()
    
    elif denoiser=='resemble':
        denoised = run_resemble_denoiser(audio, sr, version)
        return denoised[-1,:].numpy()
    
    else:
        raise ValueError(f'Unknown AI denoiser: {denoiser}')