from pesq import pesq
from utils.audio_utils import load_and_resample

clean, sr = load_and_resample('test_audios/audio1.wav', 16000)

print(pesq(sr, clean, clean, 'wb'))