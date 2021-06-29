import pandas as pd
import jinja2
from plotly.subplots import make_subplots
from plotly import graph_objects as go
import math


def read_data(df1):
    df_new = pd.DataFrame()
    tot_reads = df1.iloc[0:len(df1.index), 1] \
        + df1.iloc[0:len(df1.index), 2] \
        + df1.iloc[0:len(df1.index), 3]

    df_new["Sample"] = df1.iloc[0:len(df1.index), 0]
    df_new["Percent host reads filtered"] = df1.iloc[0:len(df1.index), 1] \
        / tot_reads * 100
    df_new["Percent poor quality reads filtered"] = \
        df1.iloc[0:len(df1.index), 2] / tot_reads * 100
    df_new["Percent paired reads kept"] = df1.iloc[0:len(df1.index), 3] \
        / tot_reads * 100
    return df_new


def create_html_table(df2, df3):
    df2['Summary'] = ""
    n = 0

    while n < len(df3.index):
        if df3.iloc[n, 1] > 5:
            df2.loc[n, 'Summary'] = 'WARNING'
        else:
            df2.loc[n, 'Summary'] = 'PASS'
        n += 1

    def table_colour(val):
        if val == 'WARNING':
            color = '#A30000'
        elif val == 'PASS':
            color = '#007500'
        else:
            color = 'black'
        return 'color: %s' % color

    styler = df2.style.applymap(table_colour)

    # template handling
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=''))
    template = env.get_template("table_template.html")

    html = template.render(my_table=styler.render())

    return html


def create_subplots(df4):
    # define variables
    limit = 50
    start = 0
    end = limit
    row_num = 1
    lnd = True
    loop = True

    # determine number of rows (one graph per row)
    if len(df4.index) % limit <= 25 and len(df4.index) > limit:
        calc_rows = int((len(df4.index)) / limit)
    else:
        calc_rows = math.ceil((len(df4.index)) / limit)

    fig = make_subplots(rows=calc_rows, cols=1)

    # add traces
    while loop:
        if (row_num + 1) > calc_rows:
            loop = False
            end += len(df4.index) % limit

        fig.add_trace(
            go.Bar(
                name=df4.columns[2],
                x=df4.iloc[start:end, 0],
                y=df4.iloc[start:end, 2],
                legendgroup='group1',
                showlegend=lnd,
                marker=dict(color='#FF934F')
            ),
            row=row_num,
            col=1,
        )

        fig.add_trace(
            go.Bar(
                name=df4.columns[1],
                x=df4.iloc[start:end, 0],
                y=df4.iloc[start:end, 1],
                legendgroup='group2',
                showlegend=lnd,
                marker=dict(color='#CC2D35')
            ),
            row=row_num,
            col=1
        )

        fig.add_trace(
            go.Bar(
                name=df4.columns[3],
                x=df4.iloc[start:end, 0],
                y=df4.iloc[start:end, 3],
                legendgroup='group3',
                showlegend=lnd,
                marker=dict(color='#058ED9')
            ),
            row=row_num,
            col=1,
        )

        lnd = False
        row_num += 1
        start += limit
        end += limit

    # update figure properties
    fig.update_xaxes(title_text="<b>Sample Names</b>", tickmode='linear',
                     tickfont=dict(size=10), tickangle=90)

    fig.update_yaxes(title_text="<b>Percent Reads</b>", nticks=15)

    fig.update_layout(barmode='stack',
                      legend_title='',
                      template='simple_white',
                      hovermode='x unified',
                      hoverlabel_font_color='black',
                      hoverlabel_bordercolor='#575452',
                      height=725 * calc_rows,
                      legend=dict(y=1-(1/(calc_rows*2)), font_size=14,
                                  yanchor='bottom', traceorder='reversed')
                      )

    fig.update_traces(hovertemplate='%{data.name}: %{y}%<extra></extra>',
                      marker_line_color='#696462'
                      )

    return fig


def write_html_file(args, df5, fig, html_template):
    header = "<h1>QC Dehosting Visualization Report</h1>"
    body = "This is a dehosted QC report for %i samples.<br><br> " \
           "<b>Guide for reading this report: </b><br>" \
           "1. Hover over each bar to see the sample names and the exact " \
           "percentages. <br>" \
           "2. To remove a variable from each graph, click on the variable " \
           "name in the legend. <br>" \
           "3. To only show one particular variable in each graph, double " \
           "click on the variable name in the legend. <br>" \
           "4. The \"Summary\" column in the table below displays " \
           "\"WARNING\" if the percentage of host reads filtered " \
           "is over 5%%. <br> &nbsp; &nbsp; Otherwise, \"PASS\" is " \
           "displayed." % len(df5.index)

    with open(args.htmlfile, 'w') as f:
        f.write(header)
        f.write(body)
        f.write(fig.to_html())
        f.write(html_template)