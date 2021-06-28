# QC Dehosting Visualization Report

Using QC dehosting data from a CSV file, create an HTML file that contains stacked bar plots to visualize the data and a table that includes both the data from the CSV file and a summary column that indicates which samples contain more than 5% of host reads filtered.

----------
File List
----------
- dehost_report.py <br>
- functions.py <br>
- table_template.html <br>

--------------
Packages Used
--------------
- pandas <br>
- jinja2 <br>
- plotly <br>

----------------------------
How to Run dehost_report.py
----------------------------
In the terminal, type the following, replacing the filepaths, as well as the names of the input and output files: <br>
Python /.../dehost_report.py --inputfile /../input_filename.csv --htmlfile /.../output_filename.html

--------------
Collaborators
--------------
- Vanessa Cheung https://github.com/vanessapyc
- Zohaib Anwar https://github.com/anwarMZ
