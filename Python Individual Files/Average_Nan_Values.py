import pandas as pd
import numpy as np
import h5py

def load_hdf5_data(file_name):
    with h5py.File(file_name, 'r') as f:
        # Assuming 'pred_points' is a dataset containing the data
        data = f['pred_points'][:]
    return data

def preprocess_data(data):
    # Convert data to a DataFrame
    df = pd.DataFrame(data, columns=['x', 'y', 'bool_1', 'bool_2', 'value'])
    
    # Replace 'nan' with np.nan for numerical interpolation
    df.replace('nan', np.nan, inplace=True)
    
    # Convert relevant columns to numeric
    df[['x', 'y', 'value']] = df[['x', 'y', 'value']].apply(pd.to_numeric)
    
    # Interpolate to fill NaN values
    df[['x', 'y', 'value']] = df[['x', 'y', 'value']].interpolate()
    
    return df

def save_to_csv(df, csv_file):
    df.to_csv(csv_file, index=False)

file_path = '/path/to/Mouse-Pose-Estimation-main/H5 Files/2023-06-16_Trial 1_cropped_20fps_analysis.h5'
data = load_hdf5_data(file_path)

# Process the data
df = preprocess_data(data)

# Save the cleaned data to a CSV file
csv_file_path = '/path/to/Mouse-Pose-Estimation-main/pred_points_data.csv'
save_to_csv(df, csv_file_path)
