

def run_base_denoiser(audio, sr, denoiser=None):
    """
    Run the base denoiser.

    :param denoiser: The denoiser to run.
    :type denoiser: str
    """
    if denoiser==None:
        return audio
    
    elif denoiser=='scipy-lib':
        return run_scipy_denoiser(audio, sr)
    
    elif denoiser=='peddleboard':
        return run_pedalboard_denoiser(audio, sr)
    
    else:
        raise ValueError(f'Unknown denoiser: {denoiser}')