from .src.pedal_denoiser import run_pedal_denoiser

def run_base_denoiser(audio, sr, denoiser=None, version=0):
    """
    Run the base denoiser.

    :param denoiser: The denoiser to run.
    :type denoiser: str
    """
    if denoiser==None:
        return audio
    
    elif denoiser=='scipy-lib':
        return run_scipy_denoiser(audio, sr)
    
    elif denoiser=='pedalboard':
        return run_pedal_denoiser(audio, sr, version)
    
    else:
        raise ValueError(f'Unknown denoiser: {denoiser}')