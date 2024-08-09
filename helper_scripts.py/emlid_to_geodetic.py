import pandas as pd
import os
import re

# Load the CSV file
input_csv = 'KY Pit Outer Edge.csv'
data = pd.read_csv(input_csv)

# Ensure the 'Code' column is treated as strings
data['Name'] = data['Name'].astype(str)

# Create a directory to store the output CSVs
output_dir = 'output_csvs'
os.makedirs(output_dir, exist_ok=True)

# Extract the unique prefixes by removing numeric suffixes
def extract_prefix(code):
    match = re.match(r'^([a-zA-Z-_]+)', code)
    return match.group(1) if match else code

data['Prefix'] = data['Name'].apply(extract_prefix)
unique_prefixes = data['Prefix'].unique()

# Process the data for each unique prefix and create separate CSV files
# for prefix in unique_prefixes:
    # Filter rows that match the prefix
    # filtered_data = data[data['Prefix'] == prefix]
    
    # Select only Latitude, Longitude, and add a third column of zeros
output_data = data[['Latitude', 'Longitude']].copy()
output_data['Zero'] = 0

# Create the output CSV file
output_csv = os.path.join(output_dir, f'{input_csv}')
output_data.to_csv(output_csv, index=False, header=False)

print('CSV files have been created in the output_csvs directory.')
