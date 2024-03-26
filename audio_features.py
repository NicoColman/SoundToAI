import librosa
import numpy as np
import sounddevice as sd
    
def extract_audio_features(audio_path):
    # Load the audio
    y, sr = librosa.load(audio_path)

    # Extract some basic features
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_mean = np.mean(pitches[pitches > 0])

    intensities = librosa.feature.rms(y=y)[0]
    intensity_mean = np.mean(intensities)

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    tempo_mean = np.mean(tempo)
    # You can add more features as needed

    return pitch_mean, intensity_mean, tempo_mean