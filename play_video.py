import cv2
import subprocess
from moviepy.editor import VideoFileClip, CompositeVideoClip, concatenate_videoclips
import moviepy.video.fx.all as vfx

def run_ffmpeg_command(command):
    """ Run an FFmpeg command. """
    subprocess.run(command, shell=True, check=True)

def play_video(video_path):

    # Paths to the input videos and the output video
    video1_path = 'Videos/Bright.mp4'
    video2_path = 'Videos/Colorful.mp4'
    output_path = 'output_video1.mp4'

    # Duration of the crossfade effect
    crossfade_duration = 2  # seconds

    # 1. Extract the ending of the first video
    cmd = f'ffmpeg -y -i {video1_path} -t {crossfade_duration} -c:v h264_nvenc -preset fast first_end.mp4'
    run_ffmpeg_command(cmd)

    # 2. Extract the beginning of the second video
    cmd = f'ffmpeg -ss 0 -y -i {video2_path} -t {crossfade_duration} -c:v h264_nvenc -preset fast second_start.mp4'
    run_ffmpeg_command(cmd)

    # 3. Create a crossfade transition (complex filter command)
    cmd = f'ffmpeg -y -i first_end.mp4 -i second_start.mp4 -filter_complex \
    "[0:v]format=pix_fmts=yuva420p,fade=t=out:st=0:d={crossfade_duration}:alpha=1[va0]; \
    [1:v]format=pix_fmts=yuva420p,fade=t=in:st=0:d={crossfade_duration}:alpha=1[va1]; \
    [va0][va1]overlay[vo]" -map "[vo]" -c:v h264_nvenc -preset fast crossfade.mp4'
    run_ffmpeg_command(cmd)

    # 4. Concatenate the videos (excluding the transition parts from the originals)
    cmd = f'ffmpeg -y -i {video1_path} -t {crossfade_duration} -c:v h264_nvenc -preset fast first_part.mp4'
    run_ffmpeg_command(cmd)

    cmd = f'ffmpeg -y -ss  {crossfade_duration} -i {video2_path} -c:v h264_nvenc -preset fast second_part.mp4'
    run_ffmpeg_command(cmd)
    
    # Create a text file with the file names
    with open('files.txt', 'w') as f:
        f.write("file 'first_part.mp4'\n")
        f.write("file 'crossfade.mp4'\n")
        f.write("file 'second_part.mp4'\n")

    # Concatenate the videos
    cmd = f'ffmpeg -y -f concat -safe 0 -i files.txt -c copy {output_path}'
    run_ffmpeg_command(cmd)

    # Load the video clips
    #clip1 = VideoFileClip(video_path).crossfadeout(2)  # Add a 1-second crossfade-out at the end
    #clip2 = VideoFileClip("Videos/Colorful.mp4").crossfadein(2)  # Add a 1-second crossfade-in at the start

    #clip2 = clip2.set_start(clip1.duration - 2)
    # Concatenate the clips
    #final_clip = CompositeVideoClip([clip1, clip2])

    # Write the result to a file
    #final_clip.write_videofile("output_video.mp4", codec="libx264")

    # The rest of your code...
   
   
   
    # Create a VideoCapture object
    cap = cv2.VideoCapture("output_video.mp4")
    
    # Check if video opened successfully
    if not cap.isOpened():
        print("Error opening video file")

    # Read until video is completed
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            # Display the resulting frame
            cv2.imshow('Video', frame)

            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    # Release the VideoCapture object
    cap.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()

