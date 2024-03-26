from audio_features import extract_audio_features
from pydub import AudioSegment
from show_image import show_image
from transition import add_video_to_queue, process_videos, video_queue
import time
from queue import Queue

last_video = None
def main():
    
    global last_video
    
    # Load audio file
    audio = AudioSegment.from_file('live_audio1.wav')
    duration = len(audio)
    segment_duration = 5 * 1000

    # Iterate over the audio file, segment by segment
    for start_time in range(0, duration, segment_duration):
        end_time = start_time + segment_duration
        # Slice the audio segment
        audio_segment = audio[start_time:end_time]

        # Save the sliced audio to a new file
        audio_segment.export("sliced_audio.wav", format="wav")
        # Extract audio features from the sliced audio
        pitch_mean, intensity_mean, tempo_mean = extract_audio_features('sliced_audio.wav')

        # Print the mean pitch for the current segment
        print(f"Time: {start_time / 1000} to {end_time / 1000} seconds, Mean pitch: {pitch_mean}, Mean intensity: {intensity_mean}, Mean tempo: {tempo_mean}")

        show_image(pitch_mean, intensity_mean, tempo_mean)
        
        new_video = show_image(pitch_mean, intensity_mean, tempo_mean)
        
        if last_video:
            # If there is a last video, add it to the queue first
            add_video_to_queue(last_video)
        
        add_video_to_queue(new_video)
        
        last_video = new_video
        
        if video_queue.qsize() >= 2:
            process_videos()
        
        time.sleep(1)
if __name__ == "__main__":
    main() 
    
    
    #live_audio = capture_audio('live_audio.wav', duration=10)
    #transcript = sr.speech_recognition('live_audio1.wav')
    #print(f"Transcript: {transcript}")
    # Load audio file
    #prompt1 = transcript
    #print(f"Prompt: '{prompt1}'")
    #chat_with_gpt(prompt1)
    #generate_dalle(prompt1, 'Images')
    #create_video('Images', 'video.mp4')