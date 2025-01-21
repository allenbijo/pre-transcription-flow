import noisereduce as nr
from noisereduce.noisereduce import SpectralGateStationary

def dnoise(data,rate):

    # Spectral Gate Noise Reduction
    sg = SpectralGateStationary(
        y=data,
        sr=rate,
        y_noise=None,
        prop_decrease=0.9,
        time_constant_s=2.0,
        freq_mask_smooth_hz=500,
        time_mask_smooth_ms=50,
        n_std_thresh_stationary=2,
        tmp_folder=None,
        chunk_size=6000000,
        padding=30000,
        n_fft=1024,
        win_length=None,
        hop_length=None,
        clip_noise_stationary=False,
        use_tqdm=False,
        n_jobs=1,
    )
    subset_noise_reduce = sg.get_traces(start_frame=0, end_frame=len(data))

    # Reduce Non-Stationary Noise
    reduced_noise_nonstationary = nr.reduce_noise(
        y=subset_noise_reduce,
        sr=rate,
        thresh_n_mult_nonstationary=2,
        stationary=False
    )
    return reduced_noise_nonstationary, rate
