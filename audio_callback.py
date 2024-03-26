import sounddevice as sd
import numpy as np
import librosa
import soundfile as sf

def capture_audio(filename='live_audio.wav', duration=5, sample_rate=22050):
    # Record audio for the given duration from the default microphone
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  # Wait until the recording is finished

    # Save the audio data to a WAV file
    sf.write(filename, audio_data, sample_rate)

    return audio_data.flatten()
def extract_audio_features(y, sr=22050):
    # Assuming y is the audio data and sr is the sample rate

    # Extract some basic features
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_mean = np.mean(pitches[pitches > 0])

    intensities = librosa.feature.rms(y=y)[0]
    intensity_mean = np.mean(intensities)

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    tempo_mean = np.mean(tempo)  # Note: tempo is a single value, not an array

    # You can add more features as needed
    return pitch_mean, intensity_mean, tempo_mean