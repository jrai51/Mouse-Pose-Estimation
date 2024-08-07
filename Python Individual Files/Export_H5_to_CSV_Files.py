import os
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
        writer.writerow(['x', 'y', 'bool_1', 'bool_2', 'value', 'Seen'])
        # Write the data
        for row in data:
            writer.writerow(list(row) + ['TRUE'])

def process_h5_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.h5'):
            file_path = os.path.join(input_dir, file_name)
            data = load_hdf5_data(file_path)
            
            csv_file_name = os.path.splitext(file_name)[0] + '.csv'
            csv_file_path = os.path.join(output_dir, csv_file_name)
            
            save_to_csv(data['pred_points'], csv_file_path)

input_dir = '/path/to/Mouse-Pose-Estimation-main/H5 Files'
output_dir = '/path/to/Mouse-Pose-Estimation-main/CSV Files'
process_h5_files(input_dir, output_dir)
