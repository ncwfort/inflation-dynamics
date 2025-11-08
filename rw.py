import csv
from params import SectorParams



"""Reads in parameters from a CSV file"""
def get_params(filename):
    all_params = []
    with open(filename, 'r', newline = '') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            all_params.append(row)

""" Testing parameter reading. Gets a row of the CSV and feeds it into the new
    parameters modeule that I have created."""
def test_param_reading(filename):
    with open(filename, 'r', newline = '') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            these_params = SectorParams(row)
            print(these_params.data)
    