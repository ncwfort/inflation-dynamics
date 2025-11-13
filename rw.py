import csv
from params import SectorParams

"""
This module includes the methods that are used to interact with CSVs. Just
read is implemented at present.
"""

def get_params(filename):
    """
    Reads in parameters from a CSV file and returns a list of lists of
    parameters. All parsing of these lists is handled by Economy and
    SectorParams classes.

    filename: the name of the CSV file to be read in.
    """
    all_params = []
    with open(filename, 'r', newline = '') as csv_file:
        reader = csv.reader(csv_file)
        next(reader) # skip header row
        for row in reader:
            all_params.append(row)
    return all_params

def test_param_reading(filename):
    """
    Test function for parameter reading. Turns a row of data directly into a
    SectorParams object and prints out the data for that object.

    filename: CSV file to be read in.
    """
    with open(filename, 'r', newline = '') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            these_params = SectorParams(row)
            print(these_params.data)
            print('\n')
    