import sys
import json
import argparse
import pandas as pd
import tkinter as tk
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
print(data_filename)
print(key)

data = pd.read_excel(data_filename, skiprows = key['excel_params']['data_start_row'], index_col = 'Time [s]')
data.drop(['Temp. [°C]', float('NaN'), 'End Time'], inplace=True)
data = data.T

print(data)

title_dict = {}
for head in data.head():
    row = head[0]
    column = head[1:]
    title_dict[head] = f'{key["column"][column]}-{key["row"][row]}'
    if head in key['override_well']:
        title_dict[head] = key['override_well'][head]

data.rename(title_dict, inplace=True, axis=1)
print(data)

data.to_csv(output_filename, index_label = 'Time [s]')