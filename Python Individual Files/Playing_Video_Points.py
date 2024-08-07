import cv2
import pandas as pd
import numpy as np

# Load data from CSV
data = pd.read_csv('/Users/aryankhimani/Downloads/Mouse-Pose-Estimation-main/CSV Files/2023-06-16_Trial 1_cropped_20fps_analysis.csv')

# Configurable starting frame and initial PoGS
starting_frame = 327  # Set the starting frame here
initial_PoGS = 1270  # Set the initial PoGS here

# Initialize variables
video_path = '/Volumes/okamoto_lab/shared/4 Jay/behaviour/in vivo imaging/2023-06-16_Trial 1_cropped_20fps.mp4'
video_capture = cv2.VideoCapture(video_path)
total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
image_size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
current_PoGS = initial_PoGS

# Function to update the image
def update_image(frame_index, start_index):
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)  # Set the video frame to the current index
    ret, frame = video_capture.read()
    if not ret:
        return None  # Return None if frame is not read

    # Plot points based on start_index (current_PoGS)
    num_points = 6
    end_index = start_index + num_points

    # Ensure we don't go out of bounds
    points_to_plot = data.iloc[start_index:end_index]

    for _, row in points_to_plot.iterrows():
        x = int(row['x'])
        y = int(row['y'])
        cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)  # Draw a green dot at (x, y)

    return frame

# Set the video capture to start from the specified frame
video_capture.set(cv2.CAP_PROP_POS_FRAMES, starting_frame)

# Play video
while True:
    frame_index = int(video_capture.get(cv2.CAP_PROP_POS_FRAMES))
    frame = update_image(frame_index, current_PoGS)

    if frame is None:
        break  # Exit if no frame is returned

    cv2.imshow('Video with Points', frame)

    key = cv2.waitKey(30)  # Wait for 30 ms or until a key is pressed
    if key == 27:  # ESC key to exit
        break

    # Increment the PoGS for the next frame
    current_PoGS += 6  # Adjust this value to control the rate of change
    if current_PoGS + 6 > len(data):
        current_PoGS = 0  # Reset PoGS if it exceeds the length of data

# Release video capture and close windows
video_capture.release()
cv2.destroyAllWindows()
