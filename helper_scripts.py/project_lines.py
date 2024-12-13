import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def project_csv_onto_path(file1: str, file2: str, output_file: str):
    # Load the CSV files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Ensure the files have at least two columns for x and y
    if df1.shape[1] < 2 or df2.shape[1] < 2:
        raise ValueError("Both CSVs must have at least two columns for x and y positions.")

    # Extract x and y columns
    path1 = df1.iloc[:, :2].to_numpy()  # First file's path as array of (x, y)
    points2 = df2.iloc[:, :2].to_numpy()  # Second file's points as array of (x, y)

    def project_point_onto_segment(p, a, b):
        """
        Project point `p` onto the segment defined by points `a` and `b`.
        :param p: The point to project (x, y).
        :param a: The starting point of the segment (x, y).
        :param b: The ending point of the segment (x, y).
        :return: The projected point (x, y).
        """
        ap = p - a
        ab = b - a
        t = np.dot(ap, ab) / np.dot(ab, ab)
        t = np.clip(t, 0, 1)  # Ensure projection falls on the segment
        return a + t * ab

    # Project each point in the second file onto the first path
    projected_points = []
    for p in points2:
        # Find the closest segment on the first path
        min_dist = float('inf')
        closest_projection = None
        for i in range(len(path1) - 1):
            a, b = path1[i], path1[i + 1]
            projection = project_point_onto_segment(p, a, b)
            dist = np.linalg.norm(projection - p)
            if dist < min_dist:
                min_dist = dist
                closest_projection = projection
        projected_points.append(closest_projection)

    # Create a new DataFrame for the projected points
    projected_df = pd.DataFrame(projected_points, columns=["x", "y"])
    df2_projected = pd.concat([projected_df, df2.iloc[:, 2:]], axis=1)  # Retain other columns if present

    # Save the projected second CSV to an output file
    df2_projected.to_csv(output_file, index=False)
    print(f"Second CSV projected onto the first path and saved to {output_file}")

    # Plot for debugging
    plt.plot(df1.iloc[:, 0], df1.iloc[:, 1], label="Path 1 (Reference)", color="blue")
    plt.plot(df2.iloc[:, 0], df2.iloc[:, 1], label="Path 2 (Original)", color="orange")
    plt.plot(df2_projected.iloc[:, 0], df2_projected.iloc[:, 1], label="Path 2 (Projected)", color="green")
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.title("Paths Projection")
    plt.legend()
    plt.grid()
    plt.show()

# Usage example
project_csv_onto_path("tum_lvms_shifted_lvms_initial_guess.csv", "tum_lvms_corrected.csv", "tum_lvms_projected.csv")
