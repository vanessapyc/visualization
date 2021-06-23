import pandas as pd
import jinja2
from plotly.subplots import make_subplots
from plotly import graph_objects as go
import math


def create_html_table(df1):
    def table_colour(val):
        if val:
            colour = 'black'
            return 'colour: %s' % colour

    styler = df1.style.applymap(table_colour)

    # Template handling
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=''))
    template = env.get_template("graph_data_report.html")

    html = template.render(my_table=styler.render())

    return html


def read_data(df2):
    df_new = pd.DataFrame()
    tot_reads = df2["human_reads_filtered"] \
        + df2["poor_quality_reads_filtered"] \
        + df2["paired_reads_kept"]

    df_new["Sample"] = df2["sample"]
    df_new["Percent human reads filtered"] = df2["human_reads_filtered"] \
        / tot_reads * 100
    df_new["Percent poor quality reads filtered"] = \
        df2["poor_quality_reads_filtered"] / tot_reads * 100
    df_new["Percent paired reads kept"] = df2["paired_reads_kept"] \
        / tot_reads * 100
    return df_new


def create_subplots(df3):
    # define variables
    limit = 50
    start = 0
    end = limit
    row_num = 1
    lnd = True
    loop = True

    # determine number of rows (one graph per row)
    if len(df3.index) % limit <= 25 and len(df3.index) > limit:
        calc_rows = int((len(df3.index)) / limit)
    else:
        calc_rows = math.ceil((len(df3.index)) / limit)

    fig = make_subplots(rows=calc_rows, cols=1)

    # add traces
    while loop:
        if (row_num + 1) > calc_rows:
            loop = False
            end += len(df3.index) % limit

        fig.add_trace(
            go.Bar(
                name="Percent human reads filtered",
                x=df3[start:end]["Sample"],
                y=df3[start:end]["Percent human reads filtered"],
                legendgroup='group1',
                showlegend=lnd,
                marker=dict(color="#FF934F")
            ),
            row=row_num,
            col=1
        )

        fig.add_trace(
            go.Bar(
                name="Percent poor quality reads filtered",
                x=df3[start:end]["Sample"],
                y=df3[start:end]["Percent poor quality reads filtered"],
                legendgroup='group2',
                showlegend=lnd,
                marker=dict(color='#CC2D35')
            ),
            row=row_num,
            col=1,
        )

        fig.add_trace(
            go.Bar(
                name="Percent paired reads kept",
                x=df3[start:end]["Sample"],
                y=df3[start:end]["Percent paired reads kept"],
                legendgroup='group3',
                showlegend=lnd,
                marker=dict(color='#058ED9')
            ),
            row=row_num,
            col=1,
        )

        fig.update_xaxes(title_text="<b>Sample</b>", row=row_num, col=1,
                         tickmode='linear', tickfont=dict(size=10),
                         tickangle=90)

        fig.update_yaxes(title_text="<b>Percent</b>", row=row_num, col=1,
                         dtick=10)

        lnd = False
        row_num += 1
        start += limit
        end += limit

    # update figure properties
    fig.update_layout(barmode='stack',
                      legend_title='',
                      template='simple_white',
                      hoverlabel_font_color='black',
                      hoverlabel_bordercolor='white',
                      legend_font_size=13,
                      height=725 * calc_rows,
                      legend=dict(y=1-(1/(calc_rows*2)), yanchor='bottom')
                      )

    fig.update_traces(hovertemplate='<b>%{data.name}</b><br>' +
                                    'Sample=%{x}<br>' +
                                    'Percent=%{y}%<extra></extra>',
                      marker_line_color='#696462'
                      )

    return fig


def write_html_file(args, df4, fig, html_template):
    header = "<h1>QC Visualization Report</h1>"
    body = "This is a dehosted QC report for %i samples.<br><br> Note: " \
           "Hover over each bar to see the sample names and the exact " \
           "percentages. <br>" \
           "To remove a variable, click on the variable name in the " \
           "legend. <br>" \
           "To only show one variable, double click on the variable name " \
           "in the legend." % len(df4.index)
    with open(args.htmlfile, 'w') as f:
        f.write(header)
        f.write(body)
        f.write(fig.to_html())
        f.write(html_template)