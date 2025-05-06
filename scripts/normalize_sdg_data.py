"""
normalize_sdg_data.py
===================

This script normalizes a CSV file containing SDG data by performing the following operations:
1. Converts all column names to lowercase.
2. Adds an 'id' column if it doesn't already exist and assigns in ascending order ids (starting from 1).
3. Normalizes latitude and longitude columns by replacing commas with dots.
4. Renames the 'website' column to 'homepage' and prepends 'https://' to its values if that isn't the case already.
5. Writes the normalized data to a new CSV file.

Author:
-------
Christopher-Julian Müller
"""

import csv
import sys

def lowercase_column_names(csv_data):
    """
    Converts all column names in the CSV data to lowercase.

    Parameters:
    -----------
    csv_data : list of dict
        The CSV data as a list of dictionaries.

    Returns:
    --------
    list of dict
        The updated CSV data with all column names in lowercase.
    """

    updated_data = []
    for row in csv_data:
        updated_row = {key.lower(): value for key, value in row.items()}
        updated_data.append(updated_row)

    return updated_data

def add_id_column(csv_data):
    """
    Adds an 'id' column to the CSV data if it doesn't already exist.
    Assigns each row an ID starting from 1 (ascending).

    Parameters:
    -----------
    csv_data : list of dict
        The CSV data as a list of dictionaries.

    Returns:
    --------
    list of dict
        The updated CSV data with the 'id' column added.
    """

    fieldnames = csv_data[0].keys() if csv_data else []
    if 'id' not in fieldnames:
        updated_data = []
        for idx, row in enumerate(csv_data, start=1):
            row['id'] = idx
            updated_data.append(row)
        return updated_data
    return csv_data

def normalize_lat_lon(csv_data):
    """
    Replaces latitude and longitude notations with commas to dots.

    Parameters:
    -----------
    csv_data : list of dict
        The CSV data as a list of dictionaries.

    Returns:
    --------
    list of dict
        The updated CSV data with latitude and longitude in dot notation.
    """

    for row in csv_data:
        if 'latitude' in row:
            row['latitude'] = row['latitude'].replace(',', '.')
        if 'longitude' in row:
            row['longitude'] = row['longitude'].replace(',', '.')
    return csv_data

def rename_and_prepend_website(csv_data):
    """
    Renames the 'website' column to 'homepage' and prepends 'https://' to its values 
    if not empty and does not already start with 'https://'.

    Parameters:
    -----------
    csv_data : list of dict
        The CSV data as a list of dictionaries.

    Returns:
    --------
    list of dict
        The updated CSV data with the 'website' column renamed to 'homepage' and prepended 'https://'.
    """

    for row in csv_data:
        if 'website' in row:
            if row['website'] and not row['website'].startswith('https://'):
                row['homepage'] = f"https://{row['website']}"
            else:
                row['homepage'] = row['website']
            del row['website']
    return csv_data

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

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python normalize_sdg_data.py <input_csv_file> <output_csv_file_path>")

    input_csv_file_path = sys.argv[1]
    final_output_csv_file_path = sys.argv[2]

    csv_data = read_csv(input_csv_file_path)

    csv_data = lowercase_column_names(csv_data)
    csv_data = add_id_column(csv_data)
    csv_data = normalize_lat_lon(csv_data)
    csv_data = rename_and_prepend_website(csv_data)

    write_csv(final_output_csv_file_path, csv_data)