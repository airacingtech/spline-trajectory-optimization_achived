import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

# Load and parse the CSV file
def load_csv_file(file_path):
    data = pd.read_csv(file_path)
    x_csv = data.iloc[:, 0].values
    y_csv = data.iloc[:, 1].values
    z_csv = data.iloc[:, 2].values
    return x_csv, y_csv, z_csv

# Find the closest point in `inside` to each point in `outside`
def find_closest_points(inside, outside):
    distances = cdist(outside, inside)
    closest_indices = np.argmin(distances, axis=1)
    closest_points = inside[closest_indices]
    return closest_points

# Apply a low-pass filter to data
def low_pass_filter(data, alpha=0.1):
    filtered_data = np.zeros_like(data)
    filtered_data[0] = data[0]  # Initialize the first value
    for i in range(1, len(data)):
        filtered_data[i] = alpha * data[i] + (1 - alpha) * filtered_data[i-1]
    return filtered_data

# Calculate the centerline coordinates
def calculate_centerline(inside_x, inside_y, inside_z, outside_x, outside_y, outside_z, N):
    inside_points = np.column_stack((inside_x, inside_y, inside_z))
    outside_points = np.column_stack((outside_x, outside_y, outside_z))
    closest_points_inside = find_closest_points(inside_points, outside_points)
    
    # Calculate rolling averages
    def rolling_average(arr, N):
        return np.convolve(arr, np.ones(N)/N, mode='valid')
    
    outside_x_avg = rolling_average(outside_x, N)
    outside_y_avg = rolling_average(outside_y, N)
    outside_z_avg = rolling_average(outside_z, N)
    
    closest_x_avg = rolling_average(closest_points_inside[:, 0], N)
    closest_y_avg = rolling_average(closest_points_inside[:, 1], N)
    closest_z_avg = rolling_average(closest_points_inside[:, 2], N)
    
    # Calculate centerline coordinates using rolling averages
    center_x = (outside_x_avg + closest_x_avg) / 2
    center_y = (outside_y_avg + closest_y_avg) / 2
    center_z = (outside_z_avg + closest_z_avg) / 2
    
    # Calculate bank angles using rolling averages
    horizontal_distance = np.sqrt((outside_x_avg - closest_x_avg)**2 + (outside_y_avg - closest_y_avg)**2)
    vertical_distance = outside_z_avg - closest_z_avg
    bank_angle = np.arctan2(vertical_distance, horizontal_distance)  # Bank angle in radians
    
    return center_x, center_y, center_z, bank_angle

# Apply flooring and capping to the bank angle
def floor_and_cap(data, min_value, max_value):
    return np.clip(data, min_value, max_value)

# Write centerline coordinates to a CSV file
def write_centerline_to_csv(file_path, x, y, z, bank_angle):
    centerline_data = np.column_stack((x, y, z, bank_angle))
    np.savetxt(file_path, centerline_data, delimiter=',', header='x,y,z,bank_angle', comments='', fmt='%.6f')

# Plot the coordinates and centerline
def plot_coordinates_with_centerline(inside_x, inside_y, outside_x, outside_y, center_x, center_y, point_size=2):
    plt.figure(figsize=(10, 6))
    plt.scatter(inside_x, inside_y, color='blue', label='Inside Edge Coordinates', s=point_size)
    plt.scatter(outside_x, outside_y, color='red', label='Outside Edge Coordinates', s=point_size)
    plt.plot(center_x, center_y, color='green', label='Centerline', linestyle='--')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('X-Y Coordinates with Centerline')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot the Z heights
def plot_z_heights(in_z, out_z, point_size=2):
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(in_z)), in_z, color='blue', label='Inside Heights', s=point_size)
    plt.scatter(range(len(out_z)), out_z, color='red', label='Outside Heights', s=point_size)
    
    plt.xlabel('Index')
    plt.ylabel('Z Height')
    plt.title('Z Heights for Inside and Outside Edges')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot bank angles
def plot_bank_angles(bank_angle, point_size=2):
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(bank_angle)), bank_angle, color='purple', label='Bank Angles', s=point_size)
    
    plt.xlabel('Index')
    plt.ylabel('Bank Angle (radians)')
    plt.title('Bank Angles')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot the bank angle at each (x, y) point on the centerline
def plot_bank_angle_at_xy(center_x, center_y, bank_angle):
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(center_x, center_y, c=bank_angle, cmap='viridis', s=10)
    plt.colorbar(scatter, label='Bank Angle (radians)')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('Bank Angle at Each X-Y Point on the Centerline')
    plt.grid(True)
    plt.show()

# File paths (replace with your actual file paths)
in_file_path = 'KY_MAIN_INNER_enu.csv'
out_file_path = 'KY_MAIN_OUTER_enu.csv'
centerline_file_path = 'centerline_kentucky_bank_enu.csv'

# Load the data
x_in, y_in, z_in = load_csv_file(in_file_path)
x_out, y_out, z_out = load_csv_file(out_file_path)
plot_z_heights(z_in, z_out)

# Apply low-pass filter to the heights
alpha = 0.08  # Smoothing factor for low-pass filter
filtered_z_in = low_pass_filter(z_in, alpha)
filtered_z_out = low_pass_filter(z_out, alpha)
plot_z_heights(filtered_z_in, filtered_z_out)

# Calculate the centerline coordinates with filtered heights
center_x, center_y, center_z, bank_angle = calculate_centerline(x_in, y_in, filtered_z_in, x_out, y_out, filtered_z_out, N=3)

# Apply flooring and capping to the bank angle
min_bank_angle = 0.0698132  # Example minimum value (in radians)
max_bank_angle = 0.296706  # Example maximum value (in radians)
capped_bank_angle = floor_and_cap(bank_angle, min_bank_angle, max_bank_angle)

# Write the centerline coordinates to a CSV file
write_centerline_to_csv(centerline_file_path, center_x, center_y, center_z, -capped_bank_angle)

# Plot the original data and centerline
plot_coordinates_with_centerline(x_in, y_in, x_out, y_out, center_x, center_y)

# Plot the bank angle at each (x, y) point
plot_bank_angle_at_xy(center_x, center_y, capped_bank_angle)
