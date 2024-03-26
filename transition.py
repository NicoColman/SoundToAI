import os
import subprocess
import time
import threading
from queue import Queue

video_queue = Queue()

def add_video_to_queue(video_path):
    """ Add new video to the queue """
    video_queue.put(video_path)
    print(f"Added to queue: {video_path}") 
    
def run_ffmpeg_command(command):
    """ Run an FFmpeg command. """
    subprocess.run(command, shell=True, check=True, stderr=subprocess.DEVNULL)
    
def update_playlist(video_file):
    """ Appends a new video file to the playlist. """
    with open('playlist.m3u', 'a') as playlist:
        formatted_path = video_file.replace("\\", "/")  # Replace backslashes with forward slashes for consistency
        playlist.write(f'{formatted_path}\n')

def process_videos():
    """ Process videos from the queue """
    if video_queue.qsize() >= 2:
        video1 = video_queue.get()
        video2 = video_queue.get()  # Get the next video without removing from queue
        print(f"Processing videos: {video1} and {video2}")
            
    output_path = 'output_video1.mp4'

    # Duration of the crossfade effect
    crossfade_duration = 2  # seconds

    # 1. Extract the ending of the first video
    cmd = f'ffmpeg -y -sseof -{crossfade_duration} -i {video1} -t {crossfade_duration} -c:v h264_nvenc -preset fast first_end.mp4'
    run_ffmpeg_command(cmd)

    # 2. Extract the beginning of the second video
    cmd = f'ffmpeg -ss 0 -y -i {video2} -t {crossfade_duration} -c:v h264_nvenc -preset fast second_start.mp4'
    run_ffmpeg_command(cmd)

    # 3. Create a crossfade transition (complex filter command)
    cmd = f'ffmpeg -y -i first_end.mp4 -i second_start.mp4 -filter_complex \
    "[0:v]format=pix_fmts=yuva420p,fade=t=out:st=0:d={crossfade_duration}:alpha=1[va0]; \
    [1:v]format=pix_fmts=yuva420p,fade=t=in:st=0:d={crossfade_duration}:alpha=1[va1]; \
    [va0][va1]overlay=shortest=1[vo]" -map "[vo]" -c:v h264_nvenc -preset fast {output_path}'
    run_ffmpeg_command(cmd)

    print(f"Created transition video: {output_path}")

    # Optionally, you can delete the temporary files
    for file in ['first_end.mp4', 'second_start.mp4']:
        os.remove(file)
        
    update_playlist(output_path)

def main():
    # Add test videos to the queue
    add_video_to_queue('Videos/Melancholic.mp4')
    add_video_to_queue('Videos/Colorful.mp4')

    # Start processing videos
    process_videos()

if __name__ == "__main__":
    main()