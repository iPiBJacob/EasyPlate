import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import argparse
import pprint
import tkinter as tk
from tkinter import filedialog as fd
from scipy.optimize import curve_fit 
from collections import namedtuple

root = tk.Tk()  # These lines hide the Root tkinter window from view
root.withdraw()

linregress_output = namedtuple('linear_regression_fit', ['slope', 'intercept'])
def linear_fit(x, y):
    line = lambda x, m, b: m * x + b
    fit = curve_fit(line, x, y)
    output = linregress_output(fit[0][0], fit[0][1])
    return output

logistic_output = namedtuple('logistic_regression_fit', ['magnitude', 'steepness', 'midpoint', 'y_adjust'])
def logistic_fit(x, y):
    logistic = lambda x, L, k, x0, dy: L / (1 + np.exp(-k * (x - x0))) + dy
    # determine if L is positive or negative
    low_x_y = y[x.index(min(x))]  # y_value at low x
    high_x_y = y[x.index(max(x))]  # y_value at high x
    L_estimated = high_x_y-low_x_y  # May not be right value, should have right sign
    fit = curve_fit(logistic, x, y, p0 = [L_estimated, 1, 1, 0])
    output = logistic_output(fit[0][0], fit[0][1], fit[0][2], fit[0][3])
    return output


methods = {'linear': linear_fit,
           'logistic': logistic_fit}
def fit(data: pd.DataFrame, method: str):
    x = data.index.to_numpy()
    output = {}
    for label in data.columns:
        y_fit = data[label].to_numpy()
        x_fit = x
        if len(x_fit) != len(y_fit):
            x_fit = x_fit[0:len(y_fit)]
        output[label] = methods[method](x_fit, y_fit)
    return output

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-f', '--filename',
                        required=False)
arg_parser.add_argument('-e', '--exclude',
                        nargs='+',
                        help='Any data inlcuding listed strings will not be plotted')
arg_parser.add_argument('-t', '--title',
                        required=False)
arg_parser.add_argument('-s', '--save',
                        action='store_true',
                        required=False)
arg_parser.add_argument('-r', '--regression',
                        required=False,
                        choices=['linear', 'logistic'])
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

if args.regression:
    pprint.pprint(fit(data, args.regression))

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
