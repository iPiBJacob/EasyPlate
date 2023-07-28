import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import argparse
from tkinter import filedialog as fd

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-f', '--filename', required=False)
arg_parser.add_argument('-e', '--exclude', nargs='+', help='Any data inlcuding listed strings will not be plotted')
args = arg_parser.parse_args()
print(args)
print(args.exclude)
filename = args.filename
if not filename:
    filename = fd.askopenfile(initialdir='./Processed_CSV')
data = pd.read_csv(filename, index_col='Time [s]')

exclude = args.exclude

partials = {}
for label in data.columns:
    if exclude is not None:
        if any([substr in label for substr in exclude]):
            continue
    index = 0
    if '.' in label:
        index = int(label.split('.')[-1])
    if index not in partials.keys():
        partials[index] = pd.DataFrame(data.index)
        partials[index] = partials[index].set_index('Time [s]')
    header = label.split('.')[0]

    column = data[label]
    column = column.rename(header)
    partials[index] = partials[index].merge(column.to_frame(), left_index=True, right_index=True)

data = pd.concat(partials.values())
sns.lineplot(data=data)
plt.ylabel('fluorescense [RFU]')
plt.show()
