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
from csv_utils import read_csv, write_csv
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
    list of dict
        The updated CSV data with 'latitude' and 'longitude' columns added where missing.
    """

    geolocator = Nominatim(user_agent="address_geocoding")
    
    for row in csv_data:
        if ('latitude' not in row or not row['latitude']) and ('longitude' not in row or not row['longitude']):
            if 'street_address' in row and row['street_address']:
                try:
                    location = geolocator.geocode(row['street_address'], timeout=10)
                    if location:
                        row['latitude'] = location.latitude
                        row['longitude'] = location.longitude
                    else:
                        print(f"Couldn't geocode address in row '{csv_data.index(row)+1}': {row['street_address']}")
                        row['latitude'] = None
                        row['longitude'] = None
                except GeocoderTimedOut:
                    print(f"Geocoding timed out for row '{csv_data.index(row)+1}': {row['street_address']}")
                    row['latitude'] = None
                    row['longitude'] = None

    return csv_data

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

    if len(sys.argv) != 3:
        sys.exit(f"""This script requires the following inputs:
        <input_csv_file> <output_csv_file_path>
        Received instead: {len(sys.argv) - 1}""")

    input_csv_file_path = sys.argv[1]
    output_csv_file_path = sys.argv[2]

    csv_data = read_csv(input_csv_file_path)
    csv_data = geocode_addresses(csv_data)
    write_csv(output_csv_file_path, csv_data)