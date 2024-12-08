import pandas as pd
import matplotlib.pyplot as plt

def shift_csv_by_difference(file1: str, file2: str, output_file: str):
    """
    Shift the x-coordinates of the second file by the difference in the leftmost
    x-coordinates of the first and second files, and save the result.
    
    :param file1: Path to the first CSV file (reference).
    :param file2: Path to the second CSV file (to be shifted).
    :param output_file: Path to save the shifted CSV file.
    """
    # Load the CSV files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Ensure the files have at least one column for x-coordinates
    if df1.shape[1] < 1 or df2.shape[1] < 1:
        raise ValueError("Both CSVs must have at least one column for x-coordinates.")

    # Find the leftmost x-coordinate in the first and second files
    leftmost_x1, leftmost_y1 = df1.iloc[:, 0].min(), df1.iloc[:, 1].min()
    leftmost_x2, leftmost_y2 = df2.iloc[:, 0].min(), df2.iloc[:, 1].min()


    # Calculate the shift
    x_shift = leftmost_x2 - leftmost_x1
    y_shift = leftmost_y2 - leftmost_y1

     # Apply the shift to the second file
    df2_shifted = df2.copy()
    df2_shifted.iloc[:, 0] -= x_shift  # Shift the x-coordinates
    df2_shifted.iloc[:, 1] -= y_shift  # Shift the y-coordinates

    # Save the shifted file
    df2_shifted.to_csv(output_file, index=False)
    print(f"Shifted second CSV saved to {output_file}")

    # Plot for visualization
    plt.plot(df1.iloc[:, 0], df1.iloc[:, 1], label="Path 1 (Reference)", color="blue")
    plt.plot(df2.iloc[:, 0], df2.iloc[:, 1], label="Path 2 (Original)", color="orange")
    plt.plot(df2_shifted.iloc[:, 0], df2_shifted.iloc[:, 1], label="Path 2 (Shifted)", linestyle="--", color="red")
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.title("Path Shifting Visualization")
    plt.legend()
    plt.grid()
    plt.show()

# Usage example
shift_csv_by_difference("centerline_lvms_bank_enu.csv", "tum_lvms_corrected.csv", "tum_lvms_shifted.csv")