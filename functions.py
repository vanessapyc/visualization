import pandas as pd
import matplotlib.pyplot as plt
import argparse
import plotly.express as px
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
                    'Percent human reads filtered': '#FF934F',
                    'Percent poor quality reads filtered': '#CC2D35',
                    'Percent paired reads kept': '#058ED9'},
                 barmode='stack')

    fig.update_layout(
        yaxis_title='<b>Percent</b>',
        xaxis_title='<b>Sample</b>',
        legend_title='',
        template='simple_white',
        yaxis=dict(dtick=10, range=[0, 100]),
        hoverlabel_font_color='black',
        hoverlabel_bordercolor='white',
        legend_font_size=13,
        legend=dict(y=0.5, yanchor="middle")
        # xaxis_showticklabels=False,
        # xaxis_tickcolor='white'
        # xaxis = dict(tickmode = 'linear')
        )

    fig.update_traces(hovertemplate='<b>%{data.name}</b><br>' +
                                    'Sample=%{x}<br>' +
                                    'Percent=%{y}%<extra></extra>'
                      )
    # marker_line_color='black'
    return fig


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
    limit = 100
    start = 0
    end = limit
    row_num = 1
    lnd = True
    loop = True

    # number of rows (one graph per row)
    if len(df5.index) % limit < 40 and len(df5.index) > 100:
        calc_rows = int((len(df5.index)) / limit)
    else:
        calc_rows = math.ceil((len(df5.index)) / limit)

    fig = make_subplots(rows=calc_rows, cols=1)
    # x_title='<b>Sample</b>', y_title='<b>Percent</b>',
    # vertical_spacing=0.009

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
        fig.update_layout(barmode='stack',
                          legend_title='',
                          template='simple_white',
                          hoverlabel_font_color='black',
                          hoverlabel_bordercolor='white',
                          legend_font_size=13,
                          height=700 * calc_rows
                          )

        fig.update_xaxes(title_text='<b>Sample</b>', row=row_num, col=1,
                         tickmode='linear', tickfont=dict(size=10),
                         tickangle=90)
        # tickmode = 'linear', tickfont = dict(size=10), tickangle=90
        # showticklabels=False, tickcolor='white'
        fig.update_yaxes(title_text='<b>Percent</b>', row=row_num, col=1,
                         dtick=10)

        fig.update_traces(hovertemplate='<b>%{data.name}</b><br>' +
                                        'Sample=%{x}<br>' +
                                        'Percent=%{y}%<extra></extra>'
                          )
        row_num += 1
        start += limit
        end += limit

    return fig