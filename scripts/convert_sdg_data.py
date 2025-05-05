"""
convert_sdg_data.py
===================

This script converts a CSV file with SDG project data with the following fields into a JSON file.
- Name: The name of the SDG.
- Website: The URL of the project.
- Description: Description of the project.
- SDGs: The Sustainable Development Goals (SDGs) associated with the project, represented as a comma-separated string.
- Address: The address of the project.
- Latitude: The latitude of the project location.
- Longitude: The longitude of the project location.

Author:
-------
Christopher-Julian Müller
"""

import csv
import sys
import json

def convert_csv_to_json(file_path):
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
    
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            data = []

            # Convert the SDGs field into an array and append the remaining fields
            for row in reader:
                if 'SDGs' in row and row['SDGs']:
                    row['SDGs'] = [int(sdg.strip()) for sdg in row['SDGs'].split(',')]
                data.append(row)

            # Ensure non-ASCII characters are not escaped
            return json.dumps(data, indent=4, ensure_ascii=False)
        
    except FileNotFoundError:
        sys.exit(f"Error: The provided file path '{file_path}' was not valid.")

    except Exception as e:
        sys.exit(f"An error occurred while converting the input CSV to JSON: {e}")

if __name__ == "__main__":
    """
    Validate the amount of input arguments, processes the input CSV file, and writes the resulting JSON data to
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
        sys.exit("This script assumes the following inputs: <input_csv_file> <output_json_file_path>; received instead: " + str(len(sys.argv) - 1))
    
    csv_file_path = sys.argv[1]
    json_file_path = sys.argv[2]
    json_data = convert_csv_to_json(csv_file_path)

    if json_data is not None:
        try:
            with open(json_file_path, mode='w', encoding='utf-8') as json_file:
                json_file.write(json_data)
            print(f"JSON data has been saved to '{json_file_path}'")
        except Exception as e:
            print(f"An error occurred while saving the JSON file: {e}")