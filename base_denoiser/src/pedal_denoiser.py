from pedalboard import Pedalboard, HighpassFilter, LowpassFilter, NoiseGate, Compressor, Reverb, Gain

def get_pedalboard(
    highpass_freq,
    noise_gate1_threshold, noise_gate1_ratio, noise_gate1_attack, noise_gate1_release,
    lowpass_freq,
    comp1_threshold, comp1_ratio, comp1_attack, comp1_release,
    comp2_threshold, comp2_ratio, comp2_attack, comp2_release,
    noise_gate2_threshold, noise_gate2_ratio, noise_gate2_attack, noise_gate2_release,
    reverb_room_size, reverb_damping, reverb_wet, reverb_dry,
    final_lowpass_freq,
    comp3_threshold, comp3_ratio, comp3_attack, comp3_release,
    gain
):
    """_summary_

    Args:
        highpass_freq (int): feature value
        noise_gate1_threshold (int): feature value
        noise_gate1_ratio (int): feature value
        noise_gate1_attack (int): feature value
        noise_gate1_release (int): feature value
        lowpass_freq (int): feature value
        comp1_threshold (int): feature value
        comp1_ratio (int): feature value
        comp1_attack (int): feature value
        comp1_release (int): feature value
        comp2_threshold (int): feature value
        comp2_ratio (int): feature value
        comp2_attack (int): feature value
        comp2_release (int): feature value
        noise_gate2_threshold (int): feature value
        noise_gate2_ratio (int): feature value
        noise_gate2_attack (int): feature value
        noise_gate2_release (int): feature value
        reverb_room_size (int): feature value
        reverb_damping (int): feature value
        reverb_wet (int): feature value
        reverb_dry (int): feature value
        final_lowpass_freq (int): feature value
        comp3_threshold (int): feature value
        comp3_ratio (int): feature value
        comp3_attack (int): feature value
        comp3_release (int): feature value
        gain (int): feature value

    Returns:
        board: Peddleboard object
    """

    board = Pedalboard([
        HighpassFilter(cutoff_frequency_hz=float(highpass_freq)),

        NoiseGate(
            threshold_db=float(noise_gate1_threshold),
            ratio=float(noise_gate1_ratio),
            attack_ms=float(noise_gate1_attack),
            release_ms=float(noise_gate1_release)
        ),

        LowpassFilter(cutoff_frequency_hz=float(lowpass_freq)),

        Compressor(
            threshold_db=float(comp1_threshold),
            ratio=float(comp1_ratio),
            attack_ms=float(comp1_attack),
            release_ms=float(comp1_release)
        ),

        Compressor(
            threshold_db=float(comp2_threshold),
            ratio=float(comp2_ratio),
            attack_ms=float(comp2_attack),
            release_ms=float(comp2_release)
        ),

        NoiseGate(
            threshold_db=float(noise_gate2_threshold),
            ratio=float(noise_gate2_ratio),
            attack_ms=float(noise_gate2_attack),
            release_ms=float(noise_gate2_release)
        ),

        Reverb(
            room_size=float(reverb_room_size),
            damping=float(reverb_damping),
            wet_level=float(reverb_wet),
            dry_level=float(reverb_dry)
        ),

        LowpassFilter(cutoff_frequency_hz=float(final_lowpass_freq)),

        Compressor(
            threshold_db=float(comp3_threshold),
            ratio=float(comp3_ratio),
            attack_ms=float(comp3_attack),
            release_ms=float(comp3_release)
        ),

        Gain(gain_db=float(gain))
    ])

    return board

def get_board_params(n=0):
    params = [
        # works on noised audio
        [ 7.14953125e+01, -1.87119532e+00,  1.56583726e+00,  5.82645427e+00,
        2.99543665e+02,  4.60161771e+03, -6.56976811e+00,  9.26214690e+00,
        9.82423212e+00,  6.75739754e+02, -1.80744498e+01,  1.30263196e+01,
        4.96031418e+00,  3.75365992e+02, -2.99787749e+01,  4.86058514e+00,
        3.98244505e+00,  8.86356692e+02,  1.23133537e-01,  9.77184826e-01,
        5.62562536e-02,  4.60995189e-01,  5.46851189e+03, -7.67800768e+00,
        1.48302194e+01,  6.37752651e+00,  4.38056855e+02,  3.86108439e+00],
        
        # better on noised audio
        [ 2.54561034e+01, -2.49104975e+00,  2.36584342e+00,  2.16725431e+00,
        2.55691828e+02,  5.74676956e+03, -2.54933426e+01,  9.50205350e+00,
        6.68988523e+00,  6.77016743e+02, -2.11695063e+01,  5.82422148e+00,
        6.08617668e+00,  6.13416030e+02, -4.82068524e+01,  1.85770605e+00,
        4.08766383e+00,  6.66330310e+02,  4.42761718e-01,  5.88542297e-01,
        3.23400188e-02,  7.42210287e-01,  7.94055996e+03, -2.68234348e+01,
        1.49472630e+01,  5.58931430e+00,  3.10414857e+01,  8.77961760e+00,]
    ]
    
    return params[n]

def run_pedal_denoiser(audio, sr, version=0):
    params = get_board_params(version)
    board = get_pedalboard(*params)
    return board.process(audio, sr)