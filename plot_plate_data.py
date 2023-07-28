import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import argparse
import tkinter as tk
from tkinter import filedialog as fd

root = tk.Tk()  # These lines hide the Root tkinter window from view
root.withdraw()

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-f', '--filename', required=False)
arg_parser.add_argument('-e', '--exclude', nargs='+', help='Any data inlcuding listed strings will not be plotted')
arg_parser.add_argument('-t', '--title', required=False)
arg_parser.add_argument('-s', '--save', action='store_true', required=False)
args = arg_parser.parse_args()

filename = args.filename
if not filename:
    filename = fd.askopenfilename(initialdir='./Processed_CSV', title='Select formatted CSV to plot')
    if filename is None: 
        raise(Exception('No filename provided'))
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
ax = sns.lineplot(data=data)
sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
if args.title:
    plt.title(args.title)
plt.ylabel('fluorescense [RFU]')
plt.subplots_adjust(right=0.7)
if args.save:
    save_filename = fd.asksaveasfilename(filetypes = [['png images', 'png'], ['eps images', 'eps']])
    plt.savefig(save_filename)
plt.show()
