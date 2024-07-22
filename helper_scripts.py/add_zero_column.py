import pandas as pd

def add_zero_column(input_csv, output_csv):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv)
    
    # Create a column of zeros
    zero_column = [0] * len(df)
    
    # Insert the zero column at the 3rd column (index 2)
    df.insert(2, 'ZeroColumn', zero_column)
    
    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    input_csv = 'LVMS_SVL_BANK.csv'  # Replace with your input CSV file path
    output_csv = 'LVMS_SVL_BANK_4col.csv'  # Replace with your desired output CSV file path
    add_zero_column(input_csv, output_csv)
