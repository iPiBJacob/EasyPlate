# EasyPlate
A quick and easy tool to rapidly process plate reader data

## preparation

To start, I recommend placing the file you want to process in the Raw_Excel folder within EasyPlate. Edit the included plate_map.json file to let EasyPlate know what your columns and rows mean syntactically. It is only necessary to include labels for columns and rows included in your data.

## preprocess_plate_reader.py

Once you have plate_map.json edited to your liking, run `python preprocess_plate_reader.py`. You will be prompted to select a data file to open. Select your Excel file. After that, you will be prompted for a location to save your output. I recommend doing so in the included Processed_CSV folder. Your plate readings will be saved and labeled, and the metadata from the Excel file (temperature, gain, etc.) will be omitted. You can then use the output with your own code or use the plot_plate_data.py script here. There are some useful command line arguments to give more power and flexibility in this process.

"-i" or "--input" allows you to specify your input Excel file from the command line rather than using a popup window. This is useful if you are working on a server where graphical interfaces are unavailable.

"-k" or "--key" allows you to specify a file other than plate_map.json to take the role of plate_map.json. This can be useful if you have a particular layout you use repeatedly and want to save it for quick access.

"-o" or "--output" allows you to specify your output csv filename from the command line rather than using a popup window. This is useful if you are working on a server where graphical interfaces are unavailable.

"-d" or "--delimiter" allows you to specify a particular character or string to connect column and row labels. The labels will be [column label][delimiter][row label], with the default delimiter being "-".

## plot_plate_data.py

To view your data, run `python plot_plate_data.py` and a graph will be made, combining replicates and generating error bars as needed. For convenience, there are some useful command line arguments that let you edit your plot without editing the script. 

"-e" or "--exclude" will take one or more text strings you provide and omit any wells that include that text from consideration. For example, I have four data fields: Glucose, Mannose, Xylose, and Blank. If I run `python plot_plate_data.py -e Blank` the resultant plot will not inlcude the data for the Blank. This works for substrings as well. If I run `python plot_plate_data.py --exclude ose` then the plot will exlude Glucose, Mannose, and Xylose, since they all share that substring. Multiple arguments are accepted as well. `python plot_plate_data.py -e Blank Glu` would exclude both the Blank and the Glucose readings. This can be useful if one reading is on a different scale than the others and it is compressing your axes.

"-t" or "--title" allows you to pass in a title for the plot, especially useful if you intend to save the plot directly. Spaces can be included in the title if you surround it with quotation marks, eg. `python plot_plate_data.py -t "Sugar Data No Glucose"`

"-s" or "--save", if used, will bring up a prompt to save your plot before displaying it.

"-r" or "--regression" will fit a function to each of your data conditions and print the fit parameters to the console. Current options for regression type are linear and logistic. As an example, if I run `python plot_plate_data.py -r linear` on my data set that has 12 different headings, e.g. "3333-Glu125", then the console will include one line for each in the format `'3333-Glu125': linear_regression_fit(slope=9.518535916369622, intercept=8259.112158935726)` A future update will give the option of printing in a more concise format, e.g. `'3333-Glu125: linear_regression_fit(m=9.518535916369622, b=8259.112158935726)`.