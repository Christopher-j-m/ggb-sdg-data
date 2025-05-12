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
        with open(input_csv_file_path, mode='r', newline='', encoding='utf-8-sig') as input_file:
            sniffer = csv.Sniffer().sniff(input_file.read(), delimiters=",;")
            input_file.seek(0)
            reader = csv.DictReader(input_file, delimiter=sniffer.delimiter)
            return list(reader)
    except FileNotFoundError:
        sys.exit(f"Error: The file '{input_csv_file_path}' was not found.")
    except Exception as e:
        sys.exit(f"An error occurred: {e}")

def write_csv(csv_data, output_csv_file_path):
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

def write_failed_rows_to_textfile(txt_data, output_text_file_path):
    """
    Writes the failed rows during the geocoding to a text file in the format:
    [Row X] Reason: name - street_address

    Parameters:
    -----------
    failed_rows : list of dict
        The list of failed rows with reasons and addresses.
    output_text_file_path : str
        The path to the output text file.
    """

    try:
        with open(output_text_file_path, mode='w', encoding='utf-8') as text_file:
            for row in txt_data:
                row_index = row.get("row_index", "Unknown index")
                reason = row.get("reason", "Unknown reason")
                name = row.get("name", "Unknown name")
                street_address = row.get("street_address", "Unknown address")
                text_file.write(f"[Row {row_index}] {reason}: {name} - {street_address}\n")
    except Exception as e:
        sys.exit(f"An error occurred while writing to the text file: {e}")