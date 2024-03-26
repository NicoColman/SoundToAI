import cv2
import glob

def create_video(image_folder, video_name):
    # Get the list of image files
    images = glob.glob(f"{image_folder}/*.jpg")

    # Read the first image to get the width and height
    frame = cv2.imread(images[0])
    height, width, layers = frame.shape

    # Create a VideoWriter object
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), 1, (width, height))

    # Write each image to the video
    for image in images:
        video.write(cv2.imread(image))

    # Release the VideoWriter
    video.release()


