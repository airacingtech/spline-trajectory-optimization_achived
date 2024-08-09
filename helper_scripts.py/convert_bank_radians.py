import csv
import math

def convert_degrees_to_radians(input_csv, output_csv):
    with open(input_csv, mode='r') as infile, open(output_csv, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            # Convert the third column from degrees to radians
            row[3] = str(math.radians(float(row[2])))
            writer.writerow(row)

# Usage
input_csv = 'centerline_kentucky_bank_enu.csv'
output_csv = 'centerline_kentucky_bank_enu_rad.csv'
convert_degrees_to_radians(input_csv, output_csv)
