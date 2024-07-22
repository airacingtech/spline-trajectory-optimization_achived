import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

# Load and parse the CSV file
def load_csv_file(file_path):
    data = pd.read_csv(file_path)
    x_csv = data.iloc[:, 0].values
    y_csv = data.iloc[:, 1].values
    return x_csv, y_csv

# Find the closest point in `inside` to each point in `outside`
def find_closest_points(inside, outside):
    distances = cdist(outside, inside)
    closest_indices = np.argmin(distances, axis=1)
    closest_points = inside[closest_indices]
    return closest_points

# Calculate the centerline coordinates
def calculate_centerline(inside_x, inside_y, outside_x, outside_y):
    closest_points_inside = find_closest_points(np.column_stack((inside_x, inside_y)), np.column_stack((outside_x, outside_y)))
    center_x = (outside_x + closest_points_inside[:, 0]) / 2
    center_y = (outside_y + closest_points_inside[:, 1]) / 2
    return center_x, center_y

# Write centerline coordinates to a CSV file
def write_centerline_to_csv(file_path, x, y):
    centerline_data = np.column_stack((x, y, np.zeros_like(x)))  # Adding a third column of zeroes
    np.savetxt(file_path, centerline_data, delimiter=',', header='x,y,z', comments='', fmt='%.6f')


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

# File paths (replace with your actual file paths)
in_file_path = 'inside_line_kentucky_gps_formatted_enu.csv'
out_file_path = 'outside_line_kentucky_gps_formatted_enu.csv'
centerline_file_path = 'centerline_kentucky_enu.csv'

# Load the data
x_in, y_in = load_csv_file(in_file_path)
x_out, y_out = load_csv_file(out_file_path)

# Calculate the centerline coordinates
center_x, center_y = calculate_centerline(x_in, y_in, x_out, y_out)

# Write the centerline coordinates to a CSV file
write_centerline_to_csv(centerline_file_path, center_x, center_y)

# Plot the original data and centerline
plot_coordinates_with_centerline(x_in, y_in, x_out, y_out, center_x, center_y)
