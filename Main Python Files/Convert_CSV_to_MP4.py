import cv2
import pandas as pd
import numpy as np
import os
from pync import Notifier

# Paths
csv_folder = '/Users/aryankhimani/Downloads/Mouse-Pose-Estimation-main/CSV Files'
video_folder = '/Volumes/okamoto_lab/shared/4 Jay/behaviour/in vivo imaging'
output_folder = '/Users/aryankhimani/Downloads/Mouse-Pose-Estimation-main/output_videos'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get list of CSV files
csv_files = [f for f in os.listdir(csv_folder) if f.endswith('_analysis.csv')]

# Initialize variables
mode = 'trackbars'  # Initial mode: 'trackbars', 'playback', 'saving'

def update_image(frame_index, start_index, data, video_capture, image_size):
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ret, frame = video_capture.read()
    if not ret:
        print(f"Failed to read frame {frame_index}.")
        return np.zeros((image_size[1], image_size[0], 3), dtype=np.uint8)

    num_points = 6
    end_index = start_index + num_points
    points_to_plot = data.iloc[start_index:end_index]

    for _, row in points_to_plot.iterrows():
        x = int(row['x'])
        y = int(row['y'])
        cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

    return frame

def process_file(csv_file):
    global mode
    # Load data from CSV
    data = pd.read_csv(os.path.join(csv_folder, csv_file))
    print(f"Data loaded successfully from {csv_file}.")

    # Get corresponding video path
    video_name = csv_file.replace('_analysis.csv', '')
    video_path = os.path.join(video_folder, video_name + '.mp4')
    output_video_path = os.path.join(output_folder, video_name + '_with_points.mp4')

    if not os.path.exists(video_path):
        print(f"Video file {video_path} not found.")
        return

    video_capture = cv2.VideoCapture(video_path)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    image_size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Video loaded: {fps} FPS, {total_frames} frames for {video_name}.")

    current_index = 0
    start_frame = 0

    def create_trackbars():
        cv2.createTrackbar('Frame', window_name, 0, total_frames - 1, on_trackbar_change)
        cv2.createTrackbar('PoGS', window_name, 0, len(data) - 1, on_trackbar_change)
        cv2.setTrackbarPos('Frame', window_name, current_index)
        cv2.setTrackbarPos('PoGS', window_name, start_frame)

    def on_trackbar_change(val):
        nonlocal current_index, start_frame
        current_index = cv2.getTrackbarPos('Frame', window_name)
        start_frame = cv2.getTrackbarPos('PoGS', window_name)
        img = update_image(current_index, start_frame, data, video_capture, image_size)
        cv2.imshow(window_name, img)

    # Create a window and trackbars
    window_name = 'Point Viewer'
    cv2.namedWindow(window_name)
    create_trackbars()

    img = update_image(current_index, start_frame, data, video_capture, image_size)
    cv2.imshow(window_name, img)
    print("Initial window setup complete.")

     # Send notification
    

    while True:
        key = cv2.waitKey(30)  # Wait for 30 ms or until a key is pressed

        if key == 27:  # ESC key to exit
            print("Exiting...")
            break

        if mode == 'trackbars':
            if key == ord('l'):  # 'l' key to increase the current index
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
            elif key == ord('n'):  # 'n' key to start video playback with points
                mode = 'playback'
                cv2.destroyWindow(window_name)  # Close the trackbars window
                starting_frame = current_index
                current_PoGS = start_frame
                video_capture.set(cv2.CAP_PROP_POS_FRAMES, starting_frame)
                while True:
                    frame_index = int(video_capture.get(cv2.CAP_PROP_POS_FRAMES))
                    frame = update_image(frame_index, current_PoGS, data, video_capture, image_size)

                    if frame is None:
                        break

                    cv2.imshow('Video with Points', frame)
                    key = cv2.waitKey(30)

                    if key == 27:  # ESC key to exit playback
                        break

                    if key == ord('b'):  # 'b' key to go back to trackbars mode
                        cv2.destroyWindow('Video with Points')
                        mode = 'trackbars'
                        cv2.namedWindow(window_name)
                        create_trackbars()
                        img = update_image(current_index, start_frame, data, video_capture, image_size)
                        cv2.imshow(window_name, img)
                        break

                    # Increment the PoGS for the next frame
                    current_PoGS += 6
                    if current_PoGS + 6 > len(data):
                        current_PoGS = 0

        if key == ord('u'):  # 'u' key to save video with points
            mode = 'saving'
            print("Saving...")
            starting_frame = current_index
            current_PoGS = start_frame

            # Set up video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, image_size)

            # Process each frame of the video starting from the specified frame
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, starting_frame)
            while True:
                frame_index = int(video_capture.get(cv2.CAP_PROP_POS_FRAMES))
                frame = update_image(frame_index, current_PoGS, data, video_capture, image_size)

                if frame is None:
                    break

                video_writer.write(frame)

                # Increment the PoGS for the next frame
                current_PoGS += 6
                if current_PoGS + 6 > len(data):
                    break

            # Release resources
            video_writer.release()
            mode = 'trackbars'  # Go back to trackbars mode after saving
            create_trackbars()
            print("Saved!")
            
            # Send notification
            Notifier.notify(
                title='Video Processing Complete',
                message=f'The video {video_name} with points has been saved successfully.',
                app_name='Point Viewer'
            )

    # Release resources
    video_capture.release()
    cv2.destroyAllWindows()

for csv_file in csv_files:
    process_file(csv_file)
    mode = 'trackbars'  # Reset mode for the next file
