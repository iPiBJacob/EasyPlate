import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import argparse
import tkinter as tk
from tkinter import filedialog as fd
from scipy.optimize import curve_fit 
from collections import namedtuple


root = tk.Tk()  # These lines hide the Root tkinter window from view
root.withdraw()

line = lambda x, m, b: m * x + b
logistic = lambda x, L, k, x0, dy: L / (1 + np.exp(-k * (x - x0))) + dy

linregress_output = namedtuple('linear_regression_fit', ['slope', 'intercept'])
def linear_fit(x, y):
    
    fit = curve_fit(line, x, y)
    output = linregress_output(*fit[0])
    return output

logistic_output = namedtuple('logistic_regression_fit', ['magnitude', 'steepness', 'midpoint', 'y_adjust'])
def logistic_fit(x, y):
    
    # determine if L is positive or negative
    low_x_y = y[x.index(min(x))]  # y_value at low x
    high_x_y = y[x.index(max(x))]  # y_value at high x
    L_estimated = high_x_y-low_x_y  # May not be right value, should have right sign
    fit, covariance = curve_fit(logistic, x, y, p0 = [L_estimated, 1, 1, 0])
    output = logistic_output(*fit)
    print(np.diag(covariance))
    return output

def _check_duplicate(data, header):
    max_decimals = max([head.count('.') for head in data.columns])
    if header.count('.') == max_decimals:
        return True
    return False

def _dict_to_tuples(input):
    return [(i,x) for i in input for x in input[i]]

def _restrict_fit_window(x_array, y_array, args):
    lower_bound = float(args.regression_window[0])
    upper_bound = float(args.regression_window[1])
    filter_low = x_array > lower_bound
    filter_high = x_array < upper_bound
    filter_merge = np.logical_and(filter_high, filter_low)
    x_fit = x_array[filter_merge]
    y_fit = y_array[filter_merge]
    return x_fit, y_fit

def _pool_replicates(data, args):
    data_dict = {}
    for header in data.columns:
        if args.exclude and any([substr in header for substr in args.exclude]):
            continue
        if _check_duplicate(data, header):
            label = header.rpartition('.')[0]
        else:
            label = header  
        if label not in data_dict:
            data_dict[label] = []
        for time, fluor in zip(data.index, data[header]):
            '''if args.regression and args.regression_window:
                if time < float(args.regression_window[0]):
                    continue  # Don't include time before start of window
                if time > float(args.regression_window[1]):
                    continue  # Don't include time after end of window'''
            data_dict[label].append((time, fluor))
    return data_dict

def _parse_data(data, args):
    data_dict = {}
    for header in data.columns:
        if args.exclude and any([substr in header for substr in args.exclude]):
            continue
        label = header  
        if label not in data_dict:
            data_dict[label] = []
        for time, fluor in zip(data.index, data[header]):
            '''if args.regression and args.regression_window:
                if time < float(args.regression_window[0]):
                    continue  # Don't include time before start of window
                if time > float(args.regression_window[1]):
                    continue  # Don't include time after end of window'''
            data_dict[label].append((time, fluor))
    return data_dict

methods = {'linear': linear_fit,
           'logistic': logistic_fit}
def fit(x, y, method: str):
    x = np.array(x)
    output = {}
    for label in data.columns:
        y_fit = np.array(y)
        x_fit = x
        if len(x_fit) != len(y_fit):
            x_fit = x_fit[0:len(y_fit)]
        return methods[method](x_fit, y_fit)


if __name__ == '__main__':
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
    arg_parser.add_argument('-rw', '--regression_window',
                            nargs=2,
                            default=None)
    arg_parser.add_argument('-c', '--convert',
                            default=None)
    arg_parser.add_argument('-sr', '--split_replicates',
                            action='store_true')
    args = arg_parser.parse_args()


    filename = args.filename
    if not filename:
        filename = fd.askopenfilename(initialdir='./Processed_CSV', title='Select formatted CSV to plot')
        if filename is None or filename == '': 
            raise(Exception('No filename provided'))
    data = pd.read_csv(filename, index_col='Time [s]')

    if args.split_replicates:
        raw_data = _parse_data(data, args)
    else:
        raw_data = _pool_replicates(data, args)

    for label, xy_data in raw_data.items():
        x = np.array([pair[0] for pair in xy_data])
        y = np.array([pair[1] for pair in xy_data])

        if args.convert:
            y = y / float(args.convert)

        if args.regression:
            x_fit, y_fit = x, y
            if args.regression_window:
                x_fit, y_fit = _restrict_fit_window(x, y, args)
            print(fit(x_fit, y_fit, args.regression))

        ax = sns.lineplot(x=x, y=y, label=label)
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    if args.title:
        plt.title(args.title)
    plt.ylabel('fluorescense [RFU]')
    plt.xlabel('time (s)')
    if args.convert:
        plt.ylabel('[product] (M)')
    plt.subplots_adjust(right=0.7)
    if args.save:
        save_filename = fd.asksaveasfilename()
        plt.savefig(save_filename, format=save_filename.split('.')[-1])
    plt.show()