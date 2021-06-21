import pandas as pd
import argparse
import jinja2
from plotly.subplots import make_subplots
from plotly import graph_objects as go
import math


def parse_args():
    parser = argparse.ArgumentParser(
        description='Takes data from QC and creates stacked bar plots')
    parser.add_argument('--inputfile', type=str,
                        default='~/Desktop/datafile.csv',
                        help='Input file name, including directory')
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


def create_html_table(df4):
    def table_colour(val):
        if val:
            colour = 'black'
            return 'colour: %s' % colour

    styler = df4.style.applymap(table_colour)

    # Template handling
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=''))
    template = env.get_template('graph_data_report.html')

    html = template.render(my_table=styler.render())

    return html


def write_html_file(df, fig, html_template):
    header = "<h1>QC Visualization Report</h1>"
    body = "This is a dehosted QC report for %i samples.<br><br> Note: " \
           "Hover over each bar to see the sample names and the exact " \
           "percentages. <br>" \
           "To remove a variable, click on the variable name in the " \
           "legend. <br>" \
           "To only show one variable, double click on the variable name " \
           "in the legend." % len(df.index)
    with open(args.htmlfile, 'w') as f:
        f.write(header)
        f.write(body)
        f.write(fig.to_html())
        f.write(html_template)


def create_subplots(df5):
    # define variables
    limit = 50
    start = 0
    end = limit
    row_num = 1
    lnd = True
    loop = True

    # number of rows (one graph per row)
    if len(df5.index) % limit <= 25 and len(df5.index) > limit:
        calc_rows = int((len(df5.index)) / limit)
    else:
        calc_rows = math.ceil((len(df5.index)) / limit)

    fig = make_subplots(rows=calc_rows, cols=1)

    while loop:
        if (row_num + 1) > calc_rows:
            loop = False
            end += len(df5.index) % limit

        fig.add_trace(
            go.Bar(
                name='Percent human reads filtered',
                x=df5[start:end]["Sample"],
                y=df5[start:end]['Percent human reads filtered'],
                legendgroup='group1',
                showlegend=lnd,
                marker=dict(color="#FF934F")
            ),
            row=row_num,
            col=1
        )

        fig.add_trace(
            go.Bar(
                name='Percent poor quality reads filtered',
                x=df5[start:end]["Sample"],
                y=df5[start:end]['Percent poor quality reads filtered'],
                legendgroup='group2',
                showlegend=lnd,
                marker=dict(color='#CC2D35')
            ),
            row=row_num,
            col=1,
        )

        fig.add_trace(
            go.Bar(
                name='Percent paired reads kept',
                x=df5[start:end]["Sample"],
                y=df5[start:end]['Percent paired reads kept'],
                legendgroup='group3',
                showlegend=lnd,
                marker=dict(color='#058ED9')
            ),
            row=row_num,
            col=1,
        )
        # text=df5['Sample'],
        # textposition='auto',
        # textfont=dict(color='black', size=15)

        lnd = False

        fig.update_xaxes(title_text='<b>Sample</b>', row=row_num, col=1,
                         tickmode='linear', tickfont=dict(size=10),
                         tickangle=90)
        # tickmode = 'linear', tickfont = dict(size=10), tickangle=90
        # showticklabels=False, tickcolor='white'
        fig.update_yaxes(title_text='<b>Percent</b>', row=row_num, col=1,
                         dtick=10)

        row_num += 1
        start += limit
        end += limit

    fig.update_layout(barmode='stack',
                      legend_title='',
                      template='simple_white',
                      hoverlabel_font_color='black',
                      hoverlabel_bordercolor='white',
                      legend_font_size=13,
                      height=725 * calc_rows,
                      legend=dict(y=1-(1/(calc_rows*2)), yanchor="bottom")
                      )

    fig.update_traces(hovertemplate='<b>%{data.name}</b><br>' +
                                    'Sample=%{x}<br>' +
                                    'Percent=%{y}%<extra></extra>',
                      marker_line_color='#696462'
                      )

    return fig