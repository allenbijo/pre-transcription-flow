def run_facebook_denoiser(audio, sr, version=0):
    """
    Run the facebook denoiser.

    :param denoiser: The denoiser to run.
    :type denoiser: str
    """
    
    if waveform.ndim == 1:
        waveform = waveform[None, :]
    
    waveform = torch.Tensor(waveform)
    
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
    
    if waveform.ndim == 1:
        waveform = torch.Tensor(waveform[None, :])
    
    waveform = torch.Tensor(waveform)
    
    return resemble_denoise(audio, sr)

def run_ai_denoiser(audio, sr, denoiser=None, version=0):
    """
    Run the AI denoiser.

    :param denoiser: The denoiser to run.
    :type denoiser: str
    """
    
    if denoiser==None:
        return audio
    
    elif denoiser=='facebook':
        denoised = run_facebook_denoiser(audio, sr, version)
        return denoised[-1,:].numpy()
    
    elif denoiser=='resemble':
        denoised = run_resemble_denoiser(audio, sr, version)
        return denoised[-1,:].numpy()
    
    else:
        raise ValueError(f'Unknown AI denoiser: {denoiser}')