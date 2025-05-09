import sys
import csv

def read_csv(input_csv_file_path):
    """
    Reads a CSV file and returns its data as a list of dictionaries.

    Parameters:
    -----------
    input_csv_file_path : str
        The path to the input CSV file.

    Returns:
    --------
    list of dict
        The CSV data as a list of dictionaries.
    """

    try:
        with open(input_csv_file_path, mode='r', newline='', encoding='utf-8') as input_file:
            reader = csv.DictReader(input_file)
            return list(reader)
    except FileNotFoundError:
        sys.exit(f"Error: The file '{input_csv_file_path}' was not found.")
    except Exception as e:
        sys.exit(f"An error occurred: {e}")

def write_csv(output_csv_file_path, csv_data):
    """
    Writes the CSV data to a file.

    Parameters:
    -----------
    output_csv_file_path : str
        The path to the output CSV file.
    csv_data : list of dict
        The CSV data as a list of dictionaries that should be written to file.
    """
    
    try:
        if csv_data:
            fieldnames = csv_data[0].keys()
            with open(output_csv_file_path, mode='w', newline='', encoding='utf-8') as output_file:
                writer = csv.DictWriter(output_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)
    except Exception as e:
        sys.exit(f"An error occurred while writing to the file: {e}")