'''Converts a CSV file to JSON format'''

# TODO
#  1. Do for all directories and augment existing zip files

import pandas as pd
import argparse

def convertCSVToJSON(csv_file:str, json_file:str):
    """
    Converts a CSV file to JSON format

    Args:
        csv_file (str): CSV file
        json_file (str): JSON file
    """
    df = pd.read_csv(csv_file)
    df.to_json(json_file, orient='records')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Converts a CSV file to JSON format')
    parser.add_argument('csv_file', help='CSV file')
    parser.add_argument('json_file', help='JSON file')
    args = parser.parse_args()
    convertCSVToJSON(args.csv_file, args.json_file)