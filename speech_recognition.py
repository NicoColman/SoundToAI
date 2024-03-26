from spleeter.separator import Separator
import io
import os
from pydub import AudioSegment
from openai import OpenAI

def convert_to_mono(filename):
    sound = AudioSegment.from_wav(filename)
    sound = sound.set_channels(1)
    sound.export(filename, format="wav")

# Convert the audio file to mono before transcribing it
convert_to_mono('output/live_audio/vocals.wav')

def speech_recognition(filename='live_audio1.wav'):
    # Load the audio file
    audio = AudioSegment.from_file(filename)

    # Slice from 20 to 30 seconds
    slice_20_to_30_seconds = audio[20000:30000]

    # Save the sliced audio to a new file
    slice_20_to_30_seconds.export("sliced_audio.wav", format="wav")
    # Use spleeter to separate the audio
    separator = Separator('spleeter:2stems')
    separator.separate_to_file('sliced_audio.wav', 'output')
    filename_without_extension = os.path.splitext("sliced_audio.wav")[0]
    convert_to_mono(f'output/{filename_without_extension}/vocals.wav')
    
    os.environ["OPENAI_API_KEY"] = "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"
    client = OpenAI()

    with open(f"output/{filename_without_extension}/vocals.wav", "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
    transcript_text = transcript.text
    return transcript_text
    
if __name__ == '__main__':
    speech_recognition()