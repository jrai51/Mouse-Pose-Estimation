import cv2
import pandas as pd
import numpy as np

# Load data from CSV
data = pd.read_csv('/Users/aryankhimani/Downloads/Mouse-Pose-Estimation-main/pred_points_data.csv')

# Initialize variables
video_path = '/Users/aryankhimani/Downloads/Mouse-Pose-Estimation-main/trial_vids/mouse_trial2.mp4'
output_video_path = '/Users/aryankhimani/Downloads/Mouse-Pose-Estimation-main/output_video_with_points.mp4'
video_capture = cv2.VideoCapture(video_path)
fps = video_capture.get(cv2.CAP_PROP_FPS)
image_size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# Define start and end times (in seconds)
start_time = 4*60+25
end_time = start_time + 10  # 10 seconds later

# Calculate the corresponding frame indices
start_frame = int(start_time * fps)
end_frame = int(end_time * fps)

# Initialize Video Writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use mp4v codec
video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, image_size)

# Function to update the image
def update_image(frame_index):
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)  # Set the video frame to the current index
    ret, frame = video_capture.read()
    if not ret:
        return None  # Return None if frame is not read

    # Plot up to 5 points for each frame
    num_points = 6
    start_index = frame_index * num_points
    end_index = start_index + num_points

    # Ensure we don't go out of bounds
    points_to_plot = data.iloc[start_index:end_index]

    for _, row in points_to_plot.iterrows():
        x = int(row['x'])
        y = int(row['y'])
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)  # Draw a green dot at (x, y)

    return frame

# Set the starting frame
video_capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

# Write video with points to output file
current_frame = start_frame
while current_frame <= end_frame:
    frame = update_image(current_frame)
    if frame is None:
        break  # Exit if no frame is returned

    video_writer.write(frame)  # Write the frame to the output video

    current_frame += 1

# Release resources
video_capture.release()
video_writer.release()
cv2.destroyAllWindows()
