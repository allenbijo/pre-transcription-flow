from utils.audio_utils import load_and_resample, save_audio
from base_denoiser.base_denoiser import run_base_denoiser
from silence_remover.silencer import run_silence_remover
from ai_denoiser.ai_denoiser import run_ai_denoiser

import argparse


def main():
    parser = argparse.ArgumentParser(description="Audio denoising and processing pipeline.")

    parser.add_argument('--input_audio', type=str, required=True, 
                        help="Path to the input noisy audio file.")
    parser.add_argument('--output_dir', type=str, default='.', 
                        help="Directory to save the processed audio file.")
    parser.add_argument('--resample_rate', type=int, default=16000, 
                        help="Target sample rate for resampling (default: 16000).")
    parser.add_argument('--base_denoiser', type=str, default='None', 
                        help="Base denoiser to use.")
    parser.add_argument('--ai_denoiser', type=str, default='None', 
                        help="AI denoiser to use.")
    parser.add_argument('--silence_removal', action='store_true', 
                        help="Enable silence removal (default: False).")
    parser.add_argument('--silence_threshold', type=float, default=-50.0, 
                        help="Silence threshold in dBFS for silence remover (default: -50.0).")
    parser.add_argument('--min_silence_duration', type=float, default=0.3, 
                        help="Minimum duration of silence to be removed (default: 0.3 seconds).")

    args = parser.parse_args()

    # Load and resample the audio
    audio, sr = load_and_resample(args.input_audio, args.resample_rate)

    # Run the base denoiser
    denoised_audio = run_base_denoiser(audio, sr, denoiser=args.base_denoiser, version=2)

    # Run silence removal if enabled
    if args.silence_removal:
        silenced_audio = run_silence_remover(denoised_audio, sr, 
                                             silence_threshold=args.silence_threshold, 
                                             chunk_size=1024, 
                                             min_silence_duration=args.min_silence_duration)
    else:
        silenced_audio = denoised_audio

    # Run the AI denoiser
    ai_denoised_audio = run_ai_denoiser(silenced_audio, sr, denoiser=args.ai_denoiser)

    # Save the final audio
    output_filename = f"{args.output_dir}/{args.input_audio.split('/')[-1].split('.')[0]}_{args.base_denoiser}_{args.silence_removal}_{args.ai_denoiser}.wav"
    save_audio(ai_denoised_audio, sr, output_filename)

    print(f"Processed audio saved at: {output_filename}")

if __name__ == "__main__":
    main()
