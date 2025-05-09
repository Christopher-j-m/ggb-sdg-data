"""
address_geocoding.py
===================

This script translates the "street_address" column of a CSV file into latitude and longitude coordinates using the Nominatim geocoding API.
The coordinates are added to the CSV file as "latitude" and "longitude" columns (if not already present).

Author:
-------
Christopher-Julian Müller
"""

import sys
from file_utils import read_csv, write_csv, write_failed_rows_to_textfile
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def geocode_addresses(csv_data):
    """
    Geocodes addresses in the 'street_address' column if 'latitude' and 'longitude' are not already present.

    Parameters:
    -----------
    csv_data : list of dict
        The CSV data as a list of dictionaries.

    Returns:
    --------
    tuple:
        - list of dict: The updated CSV data with 'latitude' and 'longitude' columns added where missing.
        - list of dict: A list of rows that couldn't be geocoded, with the reason and the address field.
    """

    geolocator = Nominatim(user_agent="address_geocoding")
    failed_rows = []  # To store rows that couldn't be geocoded

    for index, row in enumerate(csv_data, start=1):
        if ('latitude' not in row or not row['latitude']) and ('longitude' not in row or not row['longitude']):
            if 'street_address' in row and row['street_address']:
                try:
                    location = geolocator.geocode(row['street_address'], timeout=5)

                    # Long and lat found for address
                    if location:
                        row['latitude'] = location.latitude
                        row['longitude'] = location.longitude

                    # Unknown address
                    else:
                        failed_rows.append({
                            "row_index": index,
                            "reason": "Unknown address(format?)",
                            "name": row.get("name", "Unknown name"),
                            "street_address": row['street_address']
                        })
                        row['latitude'] = None
                        row['longitude'] = None

                # API request timed out
                except GeocoderTimedOut:
                    failed_rows.append({
                        "row_index": index,
                        "reason": "Timeout",
                        "name": row.get("name", "Unknown name"),
                        "street_address": row['street_address']
                    })
                    row['latitude'] = None
                    row['longitude'] = None

    return csv_data, failed_rows

if __name__ == "__main__":
    """
    Validate the amount of input arguments, translates the addresses in the input CSV file into latitude and longitude coordinates &
    writes to the specified output file.

    Command-line Arguments:
    ------------------------
    - sys.argv[1]: Path to the input CSV file (e.g. 'path/to/input.csv').
    - sys.argv[2]: Path to the output CSV file (e.g. 'path/to/output.csv').

    Raises:
    -------
    SystemExit
        If the number of arguments is != 3.
    """

    if len(sys.argv) != 4:
        sys.exit(f"""This script requires the following inputs:
        <input_csv_file> <output_csv_file_path> <failed_output_csv_file_path>
        Received instead: {len(sys.argv) - 1}""")

    input_csv_file_path = sys.argv[1]
    output_csv_file_path = sys.argv[2]
    failed_rows_file_path = sys.argv[3]

    csv_data = read_csv(input_csv_file_path)
    csv_data, failed_rows = geocode_addresses(csv_data)
    
    write_csv(csv_data, output_csv_file_path)
    if failed_rows:
        write_failed_rows_to_textfile(failed_rows, failed_rows_file_path)