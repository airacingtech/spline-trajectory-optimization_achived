import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from scipy.interpolate import splprep, splev
from scipy.integrate import cumtrapz

# Load and parse the CSV file
def load_csv_file(file_path):
    data = pd.read_csv(file_path)
    x_csv = data.iloc[:, 0].values
    y_csv = data.iloc[:, 1].values
    z_csv = data.iloc[:, 2].values
    return x_csv, y_csv, z_csv

# Load abscissa and bank angle pairs from CSV
def load_abscissa_bank_csv(file_path):
    data = pd.read_csv(file_path)
    distances = data['distance'].values
    bank_angles = data['bank_angle'].values
    return distances, bank_angles

# Find the closest distance in `bank_data` to each point in `centerline_distances`
def find_closest_bank_angles(centerline_distances, bank_distances, bank_angles):
    distances = cdist(centerline_distances.reshape(-1, 1), bank_distances.reshape(-1, 1))
    closest_indices = np.argmin(distances, axis=1)
    closest_angles = bank_angles[closest_indices]
    return closest_angles

# Interpolate points to create a smooth centerline
def interpolate_points(x, y, z, num_points=1000):
    tck, _ = splprep([x, y, z], s=0)
    u_new = np.linspace(0, 1, num_points)
    new_x, new_y, new_z = splev(u_new, tck)
    
    return np.array(new_x), np.array(new_y), np.array(new_z)

# Calculate distances along the centerline using arc length
def calculate_arc_length(x, y):
    dx = np.diff(x)
    dy = np.diff(y)
    segment_lengths = np.sqrt(dx**2 + dy**2)
    arc_lengths = cumtrapz(segment_lengths, initial=0)
    return arc_lengths

# Calculate the centerline coordinates
def calculate_centerline(inside_x, inside_y, inside_z, outside_x, outside_y, outside_z):
    inside_points = np.column_stack((inside_x, inside_y, inside_z))
    outside_points = np.column_stack((outside_x, outside_y, outside_z))
    closest_points_inside = find_closest_points(inside_points, outside_points)
    
    # Calculate centerline coordinates directly
    center_x = (outside_x + closest_points_inside[:, 0]) / 2
    center_y = (outside_y + closest_points_inside[:, 1]) / 2
    center_z = (outside_z + closest_points_inside[:, 2]) / 2
    
    return center_x, center_y, center_z

# Find closest points from `inside` to `outside`
def find_closest_points(inside, outside):
    distances = cdist(outside, inside)
    closest_indices = np.argmin(distances, axis=1)
    closest_points = inside[closest_indices]
    return closest_points

# Plot the boundaries and centerline
def plot_boundaries_and_centerline(inner_x, inner_y, outer_x, outer_y, center_x, center_y):
    plt.figure(figsize=(10, 6))
    plt.plot(inner_x, inner_y, color='blue', label='Inner Boundary')
    plt.plot(outer_x, outer_y, color='red', label='Outer Boundary')
    plt.plot(center_x, center_y, color='green', label='Centerline', linestyle='--')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('Boundaries and Centerline')

    plt.scatter(center_x, center_y, color='red', s=10)
    plt.legend()
    plt.grid(True)
    plt.show()

# Write the results to a CSV file
def write_results_to_csv(file_path, center_x, center_y, center_z, bank_angles):
    min_length = min(len(center_x), len(bank_angles))
    results_data = np.column_stack((center_x[:min_length], center_y[:min_length], center_z[:min_length], bank_angles[:min_length]))
    np.savetxt(file_path, results_data, delimiter=',', header='x,y,height,bank_angle', comments='', fmt='%.6f')

# Main script
if __name__ == "__main__":
    # File paths (replace with your actual file paths)
    in_file_path = 'ky_center_line_enu.csv'
    out_file_path = 'KY_MAIN_OUTER_enu.csv'
    abscissa_bank_file_path = 'TUM_KY_Banking.csv'
    result_file_path = 'high_ma_centerline_with_bank_angles.csv'

    # Load the data
    x_in, y_in, z_in = load_csv_file(in_file_path)
    x_out, y_out, z_out = load_csv_file(out_file_path)

    # Interpolate and calculate the centerline
    num_interpolated_points = 400
    interpolated_x_in, interpolated_y_in, interpolated_z_in = interpolate_points(x_in, y_in, z_in, num_points=num_interpolated_points)
    interpolated_x_out, interpolated_y_out, interpolated_z_out = interpolate_points(x_out, y_out, z_out, num_points=num_interpolated_points)

    # Calculate the centerline
    center_x, center_y, center_z = calculate_centerline(interpolated_x_in, interpolated_y_in, interpolated_z_in, interpolated_x_out, interpolated_y_out, interpolated_z_out)

    # Calculate arc lengths along the centerline
    centerline_arc_lengths = calculate_arc_length(center_x, center_y)

    # Plot the boundaries and centerline
    plot_boundaries_and_centerline(interpolated_x_in, interpolated_y_in, interpolated_x_out, interpolated_y_out, center_x, center_y)

    # Load abscissa-bank angle pairs and adjust distances
    bank_distances, bank_angles = load_abscissa_bank_csv(abscissa_bank_file_path)

    # Interpolate bank angles along the entire centerline
    closest_bank_angles = find_closest_bank_angles(centerline_arc_lengths, bank_distances, bank_angles)

    # Write the results to a CSV file
    write_results_to_csv(result_file_path, center_x, center_y, center_z, closest_bank_angles)

    # Plot the final results with bank angles
    plt.figure(figsize=(10, 6))
    min_length = min(len(center_x), len(center_y), len(closest_bank_angles))
    scatter = plt.scatter(center_x[:min_length], center_y[:min_length], c=closest_bank_angles[:min_length], cmap='viridis', s=10)

    plt.colorbar(scatter, label='Bank Angle (radians)')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('Final Bank Angles Along Centerline')
    plt.grid(True)
    plt.show()
