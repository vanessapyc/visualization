from functions import *

if __name__ == '__main__':
    df = pd.read_csv(args.inputfile)
    html = create_html_table(df)
    df = read_data(df)
    fig = plotly_stacked_bar(df)

    header = "<h1>QC Visualization Report</h1>"

    write_html_file(header, fig, html)