"""
convert_sdg_data.py
===================

This script converts a CSV file into a JSON file with the `SDGs` field converted into an array of integers.

Author:
-------
Christopher-Julian Müller
"""

import sys
import json
from file_utils import read_csv


def convert_csv_to_json(csv_data):
    """
    Converts a CSV file to JSON format.

    This function reads a CSV file, converts the `SDGs` field into an array of integers, and returns the data
    as a JSON string.

    Parameters:
    -----------
    file_path : str
        The path to the input CSV file.

    Returns:
    --------
    str: A JSON-formatted string with the processed data.

    Raises:
    -------
    FileNotFoundError
        If the input file is not found.
    Exception
        If any other error occurs during processing.
    """
    
    for row in csv_data:
        if 'sdgs' in row and row['sdgs']:
            row['sdgs'] = [int(sdg.strip()) for sdg in row['sdgs'].split(',')]
    return json.dumps(csv_data, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    """
    Validate the amount of input arguments, converts the input CSV file, and writes the resulting JSON data to
    the specified output file.

    Command-line Arguments:
    ------------------------
    - sys.argv[1]: Path to the input CSV file (e.g. 'path/to/input.csv').
    - sys.argv[2]: Path to the output JSON file (e.g. 'path/to/output.json').

    Raises:
    -------
    SystemExit
        If the number of arguments is incorrect or if an error occurs during
        writing the output JSON.
    """

    if len(sys.argv) != 3:
        sys.exit("""
        This script requires the following inputs:
        <input_csv_file> <output_json_file_path>
        Received instead: {}
        """.format(len(sys.argv) - 1))

    csv_file_path = sys.argv[1]
    json_file_path = sys.argv[2]

    csv_data = read_csv(csv_file_path)
    json_data = convert_csv_to_json(csv_data)

    if json_data is not None:
        try:
            with open(json_file_path, mode='w', encoding='utf-8') as json_file:
                json_file.write(json_data)
            print(f"JSON data has been saved to '{json_file_path}'")
        except Exception as e:
            print(f"An error occurred while saving the JSON file: {e}")