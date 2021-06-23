from functions import *
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description='Takes data from QC and creates stacked bar plots')
    parser.add_argument('--inputfile', type=str,
                        default='~/Desktop/datafile.csv',
                        help='Input file name, including directory')
    parser.add_argument('--htmlfile', type=str, default='QC_data_report.html',
                        help='File name for HTML file')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    df = pd.read_csv(args.inputfile)
    html = create_html_table(df)
    df = read_data(df)
    fig = create_subplots(df)

    write_html_file(args, df, fig, html)