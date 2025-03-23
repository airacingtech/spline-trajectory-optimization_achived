import csv
import pymap3d as pm
import numpy as np
import argparse

def distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)

def filter_outliers(data, threshold):
    filtered_data = [data[0]]
    for i in range(1, len(data) - 1):
        dist_prev = distance(data[i], data[i - 1])
        dist_next = distance(data[i], data[i + 1])
        if dist_prev < threshold and dist_next < threshold:
            filtered_data.append(data[i])
    filtered_data.append(data[-1])
    return filtered_data

def main(args):
    input_data = []
    output_data = []

    with open(args.input_file, 'r') as f_in:
        csv_reader = csv.reader(f_in)
        for _ in range(args.ignore_lines):
            next(csv_reader)
        for row in csv_reader:
            input_data.append(row)
            lat, lon, alt = pm.geodetic2enu(
                float(row[0]), float(row[1]), float(row[2]),
                args.origin_lat, args.origin_lon, args.origin_alt
            )
            output_data.append([lat, lon, alt] + row[3:])

    filtered_output_data = filter_outliers(output_data, args.threshold)

    with open(args.output_file, 'w') as f_out:
        csv_writer = csv.writer(f_out)
        for row in filtered_output_data:
            csv_writer.writerow([str(item) for item in row])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', required=True)
    parser.add_argument('--output_file', required=True)
    parser.add_argument('--origin_lat', type=float, required=True)
    parser.add_argument('--origin_lon', type=float, required=True)
    parser.add_argument('--origin_alt', type=float, default=0.0)
    parser.add_argument('--threshold', type=float, default=100.0)
    parser.add_argument('--ignore_lines', type=int, default=1)
    args = parser.parse_args()
    main(args)
