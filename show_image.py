# Description: This file contains the function that will show the image based on the emotion detected.

def show_image(pitch_mean, intensity_mean, tempo_mean):
    
    if 1200 > pitch_mean > 1000 and intensity_mean > 0.051 and tempo_mean > 120:
        if 1200 > pitch_mean > 1000 and intensity_mean > 0.075:
            print("Happy")
            play_video = ('Videos\Colorful.mp4')
            return play_video
        else:
            play_video = ('Videos\Bright.mp4')
            return play_video
    else:  
        print("Yellow")
        play_video = ('Videos\Melancholic.mp4')
        return play_video