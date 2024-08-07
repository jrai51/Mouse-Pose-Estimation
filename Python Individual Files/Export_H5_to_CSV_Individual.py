import csv
import h5py

def load_hdf5_data(file_name):
    with h5py.File(file_name, 'r') as f:
        data = {}
        data['pred_points'] = f['pred_points'][:]
    return data

def save_to_csv(data, csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['x', 'y', 'bool_1', 'bool_2', 'value'])
        # Write the data
        for row in data:
            writer.writerow(row)

file_path = '/path/to/Mouse-Pose-Estimation-main/H5 Files/2023-06-16_Trial 1_cropped_20fps_analysis.h5'
data = load_hdf5_data(file_path)

csv_file_path = '/path/to/Mouse-Pose-Estimation-main/pred_points_data.csv'
save_to_csv(data['pred_points'], csv_file_path)
