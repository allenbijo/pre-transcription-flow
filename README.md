# 🎧 Audio Denoising and Processing Pipeline

This Python script provides an end-to-end audio processing pipeline for cleaning up noisy recordings. It supports both traditional and AI-based denoising, resampling, and optional silence removal — making it ideal for preprocessing audio for podcasts, transcriptions, or machine learning tasks.

---

## 📦 Features

- ✅ **Base denoising** using conventional noise reduction techniques  
- 🤖 **AI-powered denoising** with advanced ML models  
- 🔇 **Optional silence removal** based on configurable thresholds  
- 🔁 **Audio resampling** to a consistent rate (default: 16 kHz)  
- 💾 **Saves cleaned audio** in a structured format

---

## 🚀 Getting Started

### Requirements

- Python 3.8+
- Install dependencies as required by your denoising and audio libraries:
  ```bash
  pip install -r requirements.txt
  ```

---

## 🛠️ Usage

```bash
python audio_pipeline.py --input_audio path/to/noisy.wav \
                         --output_dir path/to/output \
                         --resample_rate 16000 \
                         --base_denoiser spectralgate \
                         --ai_denoiser demucs \
                         --silence_removal \
                         --silence_threshold -50.0 \
                         --min_silence_duration 0.3
```

---

## ⚙️ Arguments

| Argument                | Type   | Default   | Description |
|-------------------------|--------|-----------|-------------|
| `--input_audio`         | `str`  | **REQUIRED** | Path to the input noisy `.wav` file |
| `--output_dir`          | `str`  | `.`       | Directory to save the processed file |
| `--resample_rate`       | `int`  | `16000`   | Target sampling rate for output audio |
| `--base_denoiser`       | `str`  | `'None'`  | Name of the base denoising algorithm |
| `--ai_denoiser`         | `str`  | `'None'`  | Name of the AI-based denoiser |
| `--silence_removal`     | `flag` | `False`   | If set, enables silence removal |
| `--silence_threshold`   | `float`| `-50.0`   | dBFS threshold for detecting silence |
| `--min_silence_duration`| `float`| `0.3`     | Minimum silence length (in seconds) to be removed |

---

## 🧠 Example Output

Processed audio files are saved as:

```
output_dir/filename_baseDenoiser_silenceFlag_aiDenoiser.wav
```

Example:
```
cleaned_audio/speech_spectralgate_True_demucs.wav
```

---

## 📂 Output Explanation

- `spectralgate`, `demucs`: Denoiser names used
- `True`: Indicates silence removal was applied

---

## 📢 Notes

- Ensure that the denoiser names passed to `--base_denoiser` and `--ai_denoiser` match supported implementations in your codebase (e.g., `spectralgate`, `noisereduce`, `demucs`, `rnnoise`, etc.).
- Adjust silence thresholds and durations based on your use case (podcast, call, ambient recordings, etc.).
- Output WAV files are always saved in 16-bit PCM format by default.

---

## 🧪 TODOs

- Add VAD-based segmentation
- Support batch processing of directories
- UI for interactive tuning

---

## 📄 License

MIT License
