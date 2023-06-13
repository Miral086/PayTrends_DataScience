# -*- coding: utf-8 -*-
"""
Created on Tue May 30 10:27:54 2023

@author: miral
"""

import Glassdoor_WebScrapper as gs
import os
import csv
import pandas as pd

path = "D:/ResumeThings/PayTrends_DataScience/chromedriver"

# df = gs.get_jobs('Data Scientist', 'India', 500 , False, path, 2)
# df.to_csv("glassdoor_data", index=False)

# Path to the directory containing CSV files
directory = 'D:\ResumeThings\PayTrends_DataScience\csv'

# Get all CSV files in the directory
csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]

# Initialize an empty list to store the concatenated data
concatenated_data = []

# Iterate over each CSV file
for csv_file in csv_files:
    # Open the CSV file with the appropriate encoding
    with open(os.path.join(directory, csv_file), 'r', encoding='utf-8') as file:
        # Read the contents of the CSV file
        csv_reader = csv.reader(file)
        # Skip the header row if it exists
        header = next(csv_reader, None)
        # Append the rows to the concatenated data list
        concatenated_data.extend(csv_reader)

# Path to the output file
output_file = 'concatenated.csv'

# Write the concatenated data to the output file
with open(output_file, 'w', newline='', encoding='utf-8') as file:
    # Create a CSV writer object
    csv_writer = csv.writer(file)
    # Write the header row if it exists
    if header:
        csv_writer.writerow(header)
    # Write the rows of concatenated data
    csv_writer.writerows(concatenated_data)
