import cv2
import pandas as pd
import numpy as np

# Load data from CSV
data = pd.read_csv('/path/to/Mouse-Pose-Estimation-main/CSV Files/2023-06-16_Trial 1_cropped_20fps_analysis.csv')

# Initialize variables
window_name = 'Point Viewer'
video_path = '/Volumes/okamoto_lab/shared/4 Jay/behaviour/in vivo imaging/2023-06-16_Trial 1_cropped_20fps.mp4'
video_capture = cv2.VideoCapture(video_path)
total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
image_size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
current_index = 0
start_frame = 0

# Function to update the image
def update_image(index, start_frame):
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, index)  # Set the video frame to the current index
    ret, frame = video_capture.read()
    if not ret:
        return np.zeros((image_size[1], image_size[0], 3), dtype=np.uint8)  # Black image if frame is not read

    # Plot up to 6 points
    num_points = 6
    start_index = start_frame
    end_index = start_index + num_points

    # Ensure we don't go out of bounds
    points_to_plot = data.iloc[start_index:end_index]
    
    for _, row in points_to_plot.iterrows():
        x = int(row['x'])
        y = int(row['y'])
        cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)  # Draw a green dot at (x, y)

    return frame

# Callback function for the index trackbar
def on_trackbar_index(val):
    global current_index
    current_index = val
    img = update_image(current_index, start_frame)
    cv2.imshow(window_name, img)

# Callback function for the start frame trackbar
def on_trackbar_start(val):
    global start_frame
    start_frame = val
    img = update_image(current_index, start_frame)
    cv2.imshow(window_name, img)

# Create a window and trackbars
cv2.namedWindow(window_name)
cv2.createTrackbar('Frame', window_name, 0, total_frames - 1, on_trackbar_index)
cv2.createTrackbar('PoGS', window_name, 0, len(data) - 1, on_trackbar_start)

# Show the first image
img = update_image(current_index, start_frame)
cv2.imshow(window_name, img)

# Wait until the user presses a key
while True:
    key = cv2.waitKey(30)  # Wait for 30 ms or until a key is pressed
    if key == 27:  # ESC key to exit
        break
    elif key == ord('l'):  # 'l' key to increase the current index
        current_index = min(current_index + 10, total_frames - 1)
        cv2.setTrackbarPos('Frame', window_name, current_index)
    elif key == ord('j'):  # 'j' key to decrease the current index
        current_index = max(current_index - 10, 0)
        cv2.setTrackbarPos('Frame', window_name, current_index)
    elif key == ord('i'):  # 'i' key to increase the current index
        current_index = min(current_index + 1, total_frames - 1)
        cv2.setTrackbarPos('Frame', window_name, current_index)
    elif key == ord('k'):  # 'k' key to decrease the current index
        current_index = max(current_index - 1, 0)
        cv2.setTrackbarPos('Frame', window_name, current_index)

    elif key == ord('a'):  # 'a' key to decrease the start frame
        start_frame = max(start_frame - 10, 0)
        cv2.setTrackbarPos('PoGS', window_name, start_frame)
    elif key == ord('d'):  # 'd' key to increase the start frame
        start_frame = min(start_frame + 10, len(data) - 1)
        cv2.setTrackbarPos('PoGS', window_name, start_frame)
    elif key == ord('s'):  # 's' key to decrease the start frame
        start_frame = max(start_frame - 1, 0)
        cv2.setTrackbarPos('PoGS', window_name, start_frame)
    elif key == ord('w'):  # 'w' key to increase the start frame
        start_frame = min(start_frame + 1, len(data) - 1)
        cv2.setTrackbarPos('PoGS', window_name, start_frame)

    img = update_image(current_index, start_frame)
    cv2.imshow(window_name, img)

# Release video capture and close windows
video_capture.release()
cv2.destroyAllWindows()
