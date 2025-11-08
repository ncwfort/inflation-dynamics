import csv

"""Reads in parameters from a CSV file"""
def get_params(filename):
    all_params = []
    with open(filename, 'r', newline = '') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            all_params.append(row)
    