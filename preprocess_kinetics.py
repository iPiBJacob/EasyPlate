import re
import sys
import json
import argparse
import numpy as np
import tkinter as tk
import openpyxl as xl
from tkinter import filedialog as fd

root = tk.Tk()
root.withdraw()

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-i',
                        '--input',
                        required=False,
                        help='Name of input Excel file from plate reader')
arg_parser.add_argument('-k',
                        '--key',
                        required=False,
                        default='plate_map.json',
                        help='JSON file to convert well IDs to meaningful \
                            labels. Defaults to plate_map.json')
arg_parser.add_argument('-o',
                        '--output',
                        required=False,
                        help='Filename for saving processed data')
arg_parser.add_argument('-d',
                        '--delimiter',
                        required=False,
                        default='-',
                        help='Character(s) to place between row\
                              and column labels')
arg_parser.add_argument('-ir',
                        '--ignore_row',
                        required=False,
                        default=False,
                        action='store_true',
                        help='If True, do not include row label in output')
arg_parser.add_argument('-ic',
                        '--ignore_column',
                        required=False,
                        default=False,
                        action='store_true',
                        help='If True, do not include column label in output')
arg_parser.add_argument('-il',
                        '--ignore_label',
                        required=False,
                        default=False,
                        action='store_true',
                        help='If True, do not include data label in output')
args = arg_parser.parse_args()


data_filename = args.input
if not data_filename:
    data_filename = fd.askopenfilename(initialdir='./Raw_Excel',
                                       title='Select raw data to process',
                                       filetypes=[['Excel', 'xlsx']])
    if data_filename is None: 
        raise(Exception('No input file selected'))

output_filename = args.output
if not output_filename:
    output_filename = fd.asksaveasfilename(initialdir='./Processed_CSV',
                                            title='Save processed data',
                                            defaultextension='csv',
                                            filetypes=[['csv', 'csv']])
    if output_filename is None: 
        raise(Exception('No input file selected'))

key_filename = args.key
with open(key_filename) as key_file:
    key = json.load(key_file)

source = xl.load_workbook(filename=data_filename).worksheets[0]
label = None
previous_row = [None]
well_regex = '[A-Z][0-9]+'
output = []
for row in source.iter_rows(values_only=True):
    print(row)
    if row[0] == 'Start Time':  # Shows up once, just before data
        label = row[0]
    if not label: continue  # Still in metadata at top of file
    if previous_row[0] is None and row[0] is not None:
        label = row[0]  #  Labels always follow empty rows
    previous_row = row
    if row[0] is None: continue

    if row[0] == 'Time [s]':  # Initialize a DataFrame with the time column
        if output: continue
        output.append(row)

    print(f'in: {row[0]}, match: {re.match(well_regex, row[0])}')
    print(f'label: {label}')
    if not re.match(well_regex, row[0]): continue
    row_label = row[0][0]
    column_label = row[0][1:]
    print(f'row: {row_label}, column: {column_label}')
    title = ''
    if not args.ignore_column:
        title += f'{key["column"][column_label]}{args.delimiter}'
    if not args.ignore_row:
        title += f'{key["row"][row_label]}'
    if not args.ignore_label:
        title += f'{args.delimiter}{label}'
    if row[0] in key["override_well"]:
        title = key["override_well"][row[0]] + args.delimiter + label
    row = list(row)
    row[0] = title
    output.append(row)
    print(row)

    

output = np.array(output)
np.savetxt(output_filename, output.T, delimiter=',', fmt='%s')
