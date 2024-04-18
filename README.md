# EasyPlate
A quick and easy tool to rapidly process plate reader data

## preparation

To start, I recommend placing the file you want to process in the Raw_Excel folder within EasyPlate. Edit the included plate_map.json file to let EasyPlate know what your columns and rows mean syntactically. It is only necessary to include labels for columns and rows included in your data.

To avoid unexpected behavior in downstream applications when you have replicates, please ensure all labels have the same number of decimals. This is due to the way pandas handles duplicate column headings (by tagging all beyond the first with ".1", ".2", etc) and the need for downstream steps to undo that tagging, which is done by counting the decimals. For example, if you have both "70C" and "65.4C" as row labels, change the "70C" to "70.0C" and everything will behave.

## preprocess_kinetics.py

Once you have plate_map.json edited to your liking, run `python preprocess_kinetics.py`. You will be prompted to select a data file to open. Select your Excel file. After that, you will be prompted for a location to save your output. I recommend doing so in the included Processed_CSV folder. Your plate readings will be saved and labeled, and the metadata from the Excel file (temperature, gain, etc.) will be omitted. You can then use the output with your own code or use the plot_kinetic_data.py script here. There are some useful command line arguments to give more power and flexibility in this process.

To avoid unexpected behavior in downstream applications when you have replicates, please ensure all labels have the same number of decimals. This is due to the way pandas handles duplicate column headings (by tagging all beyond the first with ".1", ".2", etc) and the need for downstream steps to undo that tagging, which is done by counting the decimals. For example, if you have both "70C" and "65.4C" as row labels, change the "70C" to "70.0C" and everything will behave.

"-i" or "--input" allows you to specify your input Excel file from the command line rather than using a popup window. This is useful if you are working on a server where graphical interfaces are unavailable.

"-k" or "--key" allows you to specify a file other than plate_map.json to take the role of plate_map.json. This can be useful if you have a particular layout you use repeatedly and want to save it for quick access.

"-o" or "--output" allows you to specify your output csv filename from the command line rather than using a popup window. This is useful if you are working on a server where graphical interfaces are unavailable.

"-d" or "--delimiter" allows you to specify a particular character or string to connect column and row labels. The labels will be [column label][delimiter][row label], with the default delimiter being "-".

## plot_kinetic_data.py

To view your data, run `python plot_kinetic_data.py` and a graph will be made, combining replicates and generating error bars as needed. For convenience, there are some useful command line arguments that let you edit your plot without editing the script. 

"-e" or "--exclude" will take one or more text strings you provide and omit any wells that include that text from consideration. For example, I have four data fields: Glucose, Mannose, Xylose, and Blank. If I run `python plot_kinetic_data.py -e Blank` the resultant plot will not inlcude the data for the Blank. This works for substrings as well. If I run `python plot_kinetic_data.py --exclude ose` then the plot will exlude Glucose, Mannose, and Xylose, since they all share that substring. Multiple arguments are accepted as well. `python plot_kinetic_data.py -e Blank Glu` would exclude both the Blank and the Glucose readings. This can be useful if one reading is on a different scale than the others and it is compressing your axes.

"-t" or "--title" allows you to pass in a title for the plot, especially useful if you intend to save the plot directly. Spaces can be included in the title if you surround it with quotation marks, eg. `python plot_kinetic_data.py -t "Sugar Data No Glucose"`

"-s" or "--save", if used, will bring up a prompt to save your plot before displaying it.

"-r" or "--regression" will fit a function to each of your data conditions and print the fit parameters to the console. Current options for regression type are linear and logistic. As an example, if I run `python plot_kinetic_data.py -r linear` on my data set that has 12 different headings, e.g. "3333-Glu125", then the console will include one line for each in the format `'3333-Glu125': linear_regression_fit(slope=9.518535916369622, intercept=8259.112158935726)` A future update will give the option of printing in a more concise format, e.g. `'3333-Glu125: linear_regression_fit(m=9.518535916369622, b=8259.112158935726)`.

"-rw" or "--regression_window" will limit the points used for regression to those with x values between two bounding values. This can be useful when you have long-term data but want to look specifically at an initial rate. If you have data that spans an hour but you only want to use data from the first 6 minutes, you can run `python plot_kinetic_data.py -r linear -rw 0 360`. If you don't specify a fit type using -r, then -rw will have no effect. -rw always takes two numerical arguments, with the lower bound first and the upper bound second.

"-c" or "--convert" allows you to convert the y-axis from its default of RFU to a concentration in molar by dividing the RFUs by a provided constant calculated from a standard curve. An example use is `python plot_kinetic_data.py -c 7.95E8`. You can tell the conversion occurred by the y-axis label changing from "Fluoresence [RFU]" to "[product] (M)". 

"-sr" or "--split_replicates" will prevent data fields with identical headings being combined. This means that, rather than getting a line with error for each data type, you will see an individual trace for each well assayed. The primary use of this is to more easily identify problematic data, like wells with bubbles that would otherwise result in large error bars.

## complex_plot.py

This script exists to handle plotting of second-order data, where the y-axis is the slope of a first-order fit. Current implementations are a melt curve (temperature on x-axis, kinetic slope on y-axis) and Michaelis-Menten kinetics (substrate concentration on x-axis, kinetic slope on y-axis) To run, execute `python complex_plot.py -m {your method choice here}`. 

Some arguments apply to all complex_plot methods, detailed here:

"-d" or "--delimiter" allows you to specify the delimiter used during data preprocessing if you changed it from the default of "-". This will be relevant if you have negative numbers in your headings so the "-" would not be an effective delimiter.

"-w" or "--window" will limit the points used for regression to those with x values between two bounding values. This can be useful when you have long-term data but want to look specifically at an initial rate. If you have data that spans an hour but you only want to use data from the first 6 minutes, you can run `python complex_plot.py -m michaelis_menten -w 0 360`. -w always takes two numerical arguments, with the lower bound first and the upper bound second.

"-s" or "--save" will cause a prompt to appear asking for a filename to save the resulting figure. The file type will be inferred from the filename, so be sure to use a common image type like png, eps, or svg or pyplot may break.

"-t" or "--title" allows you to pass in a title for the plot, especially useful if you intend to save the plot directly. Spaces can be included in the title if you surround it with quotation marks, eg. `python complex_plot.py -m melt_curve -t "Melt Curve in Lysate"`

"-f" or "--filename" allows you to specify a data file from the command line. This can be useful if you are trying different settings and don't want to wait for the file dialog to open every time you change settings.

Additionally, each fitting method has multiple options, detailed below:

### melt_curve

"-sr" or "--split_replicates" will prevent data fields with identical headings being combined. This means that, rather than getting a line with error for each data type, you will see an individual trace for each set of wells assayed. For example, if I have 3 replicates each of "Glucose 35C", "Glucose 45C", and "Glucose 55C", the first of each will form a single melt curve, the second of each will form another melt curve, and the third of each will form a third melt curve. The primary use of this is to more easily identify problematic data, like replicates with high/low protein concentration or wells that failed to react.

### michaelis_menten

"-ys" or "--y_scale" allows you to convert the y-axis from its default of RFU to a concentration in molar by dividing the RFUs by a provided constant calculated from a standard curve. An example use is `python complex_plot.py -m michaelis_menten -ys 7.95E8`. You can tell the conversion occurred by the y-axis label changing from "Activity (RFU/s)" to "Activity (M product/s)". 