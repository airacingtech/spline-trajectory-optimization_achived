import os

def convert_csvs_to_text(input_folder, output_file):
    with open(output_file, 'w') as outfile:
        for filename in os.listdir(input_folder):
            if filename.endswith('.csv'):
                file_path = os.path.join(input_folder, filename)
                
                # Read and write each CSV file's content
                with open(file_path, 'r') as infile:
                    outfile.write(f'Contents of {filename}:\n')
                    for line in infile:
                        outfile.write(line)  # Write each line as is
                    outfile.write('\n')  # Add a newline for separation

    print(f'All CSV files have been converted and saved to {output_file}')

# Example usage
input_folder = 'TTL_2_M1_mpc_INSIDE(1).csv'  # Replace with your folder path
output_file = 'output.txt'  # Replace with your desired output file name
convert_csvs_to_text(input_folder, output_file)
