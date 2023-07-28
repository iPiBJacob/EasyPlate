import sys
import json
import pandas as pd

data_filename = sys.argv[1]
key_filename = sys.argv[2]
output_filename = sys.argv[3]
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