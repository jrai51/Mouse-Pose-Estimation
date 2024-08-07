import os
import csv
import h5py
import pandas as pd
import numpy as np

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

def preprocess_data(df):
    # Replace 'nan' with np.nan for numerical interpolation
    df.replace('nan', np.nan, inplace=True)
    
    # Convert relevant columns to numeric
    df[['x', 'y']] = df[['x', 'y']].apply(pd.to_numeric)
    
    # Set first 'nan' values to 0 if they exist
    df['x'].fillna(0, inplace=True, limit=1)
    df['y'].fillna(0, inplace=True, limit=1)
    
    # Interpolate to fill NaN values
    df['x'] = df['x'].interpolate()
    df['y'] = df['y'].interpolate()
    
    return df

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
            
            # Load CSV into DataFrame for processing
            df = pd.read_csv(csv_file_path)
            df = preprocess_data(df)
            
            # Save the processed DataFrame back to CSV
            df.to_csv(csv_file_path, index=False)

input_dir = '/path/to/H5 Files'
output_dir = '/path/to/CSV Files'
process_h5_files(input_dir, output_dir)
