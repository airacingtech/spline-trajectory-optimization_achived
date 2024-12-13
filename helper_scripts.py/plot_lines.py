import matplotlib.pyplot as plt
import pandas as pd

# Function to load and plot paths from CSVs
def load_and_plot_paths(csv_files):
    plt.figure(figsize=(10, 8))
    
    # Iterate through each file and plot the X, Y data
    for i, csv_file in enumerate(csv_files):
        data = pd.read_csv(csv_file, header=None)
        x = data[0]  # First column as X
        y = data[1]  # Second column as Y
        
        plt.plot(x, y, label=f'Path {i+1}')
    
    # Add labels and legend
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('Paths Plot')
    plt.legend()
    plt.grid(True)
    plt.show()

# List of CSV files to load
csv_files = ['LVMS_MAIN_OUTTER_2024_enu(2).csv', 'LVMS_MAIN_INNER_2024_enu(2).csv', 'tum_lvms_shifted_2.csv']

# Call the function
load_and_plot_paths(csv_files)
