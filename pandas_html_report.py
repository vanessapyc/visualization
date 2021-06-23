from functions import *
from extra_functions import stacked_bar_chart


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

    # Plot
    df = read_data(df)
    ax = stacked_bar_chart(df)
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig('plot.svg')

    # Write the HTML file
    with open(args.htmlfile, 'w') as f:
        f.write(html)