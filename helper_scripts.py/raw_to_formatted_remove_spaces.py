import csv
import re

"""
Read the raw output from google earth. flips x and y cuz earth does long lat and we want lat long
also makes sure each coordinate is its own line and cleans rand symbols
"""

def replace_spaces_and_clean(input_csv, output_csv):
    with open(input_csv, 'r', newline='') as infile:
        content = infile.read()
    
    # Replace spaces with newlines and remove unwanted symbols
    cleaned_content = re.sub(r'[^0-9,.\s-]', '', content).replace(' ', '\n')
    
    # Write the cleaned content to a temporary file to process it with the csv module
    temp_file = 'temp_cleaned.csv'
    with open(temp_file, 'w', newline='') as tempfile:
        tempfile.write(cleaned_content)
    
    # Read the temporary file and switch the first and second columns
    with open(temp_file, 'r', newline='') as tempfile, open(output_csv, 'w', newline='') as outfile:
        csv_reader = csv.reader(tempfile)
        csv_writer = csv.writer(outfile)
        
        for row in csv_reader:
            if len(row) > 1:
                # Switch the first and second columns
                row[0], row[1] = row[1], row[0]
            csv_writer.writerow(row)
    
    # Optionally, remove the temporary file if needed
    import os
    os.remove(temp_file)

# Usage
input_csv = 'inside_line_kentucky_gps_raw.csv'  # Replace with your input CSV file path
output_csv = 'inside_line_kentucky_gps_formatted.csv'  # Replace with your desired output CSV file path
replace_spaces_and_clean(input_csv, output_csv)

print("Processing completed successfully.")
