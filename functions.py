import pandas as pd
import matplotlib.pyplot as plt
import argparse
import plotly.express as px
import jinja2


def parse_args():
    parser = argparse.ArgumentParser(
        description='Takes data from QC and creates stacked bar plots')
    parser.add_argument('--inputfile', type=str,
                        default='~/Desktop/datafile.csv',
                        help='Input file name, including directory')
    parser.add_argument('--outputfile', type=str, default='./',
                        help='Name the output file')
    parser.add_argument('--figsize', type=str, default='15x8',
                        help='Size of Pandas plot widthxheight')
    parser.add_argument('--outputdpi', type=int, default=300,
                        help='DPI of Pandas output file')
    parser.add_argument('--htmlfile', type=str, default='QC_data_report.html',
                        help='File name for HTML file')
    return parser.parse_args()


args = parse_args()


def read_data(df1):
    df_new = pd.DataFrame()
    tot_reads = df1["human_reads_filtered"] \
        + df1["poor_quality_reads_filtered"] \
        + df1["paired_reads_kept"]

    df_new["Sample"] = df1["sample"]
    df_new["Percent human reads filtered"] = df1["human_reads_filtered"] \
        / tot_reads * 100
    df_new["Percent poor quality reads filtered"] = \
        df1["poor_quality_reads_filtered"] / tot_reads * 100
    df_new["Percent paired reads kept"] = df1["paired_reads_kept"] \
        / tot_reads * 100
    return df_new


def stacked_bar_chart(df2):
    fig_size = args.figsize.split('x')
    ax = df2.plot(kind="bar", x="Sample", stacked=True, figsize=(
        float(fig_size[0]), float(fig_size[1])))
    ax.set_ylabel("Percent")

    # Move legend to the right
    ax.legend(bbox_to_anchor=(1.0, 0.5))

    plt.tight_layout()
    plt.savefig(args.outputfile, dpi=args.outputdpi)
    plt.show()
    return ax


def plotly_stacked_bar(df3):
    fig = px.bar(df3,
                 x='Sample',
                 y=['Percent human reads filtered',
                    'Percent poor quality reads filtered',
                    'Percent paired reads kept'],
                 color_discrete_map={
                    'Percent human reads filtered': '#FFCCB6',
                    'Percent poor quality reads filtered': '#CBAACB',
                    'Percent paired reads kept': '#ABDEE6'},
                 barmode='stack')

    fig.update_layout(
        yaxis_title="Percent",
        legend_title=""
        # xaxis = dict(tickmode = 'linear')
        )

    fig.update_traces(hovertemplate='<b>%{data.name}</b><br>' +
                                    'Sample=%{x}<br>' +
                                    'Percent=%{y}%<extra></extra>')
    return fig


def create_html_table(df4):
    def table_colour(val):
        colour = 'black'
        return f'colour: {colour}'

    styler = df4.style.applymap(table_colour)

    # Template handling
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=''))
    template = env.get_template('graph_data_report.html')

    html = template.render(my_table=styler.render())

    return html


def write_html_file(title, fig, html_template):
    with open(args.htmlfile, 'w') as f:
        f.write(title)
        f.write(fig.to_html())
        f.write(html_template)