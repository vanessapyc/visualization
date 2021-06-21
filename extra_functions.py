from functions import *
import matplotlib.pyplot as plt
import plotly.express as px
import datapane as dp


def parse_args():
    parser = argparse.ArgumentParser(
        description='Takes data from QC and creates stacked bar plots')
    parser.add_argument('--outputfile', type=str, default='./',
                        help='Name the output file')
    parser.add_argument('--figsize', type=str, default='15x8',
                        help='Size of Pandas plot widthxheight')
    parser.add_argument('--outputdpi', type=int, default=300,
                        help='DPI of Pandas output file')
    return parser.parse_args()


# using matplotlib
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


# 1 stacked bar chart
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
        yaxis=dict(dtick=10),
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


'''
if __name__ == '__main__':
    df = pd.read_csv(args.inputfile)
    html = create_html_table(df)
    df = read_data(df)
    fig = plotly_stacked_bar(df)

    write_html_file(df, fig, html)
'''


# 2 columns, 100 samples/graph
def create_subplots_2cols(df5):
    # define variables
    limit = 100
    start = 0
    end = limit
    row_num = 1
    lnd = True
    loop = True
    col_num = 1

    # number of rows (one graph per row)
    if len(df5.index) % limit <= 40 and len(df5.index) > (limit*2):
        calc_rows = int(round((len(df5.index) / (limit*2))))
    else:
        calc_rows = math.ceil((len(df5.index)) / (limit*2))

    fig = make_subplots(rows=calc_rows, cols=2, horizontal_spacing=0.050)
    # x_title='<b>Sample</b>', y_title='<b>Percent</b>',
    # vertical_spacing=0.009

    while loop:
        if end == (len(df5.index) - len(df5.index) % limit):
            if (len(df5.index) % limit) <= 40:
                end += len(df5.index) % limit
                loop = False
        elif end > (len(df5.index) - len(df5.index) % limit):
            loop = False

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
            col=col_num
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
            col=col_num,
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
            col=col_num,
        )
        # text=df5['Sample'],
        # textposition='auto',
        # textfont=dict(color='black', size=15)

        lnd = False

        fig.update_xaxes(title_text='<b>Sample</b>', row=row_num, col=col_num,
                         tickmode='linear', tickfont=dict(size=10),
                         tickangle=90)
        # tickmode = 'linear', tickfont = dict(size=10), tickangle=90
        # showticklabels=False, tickcolor='white'
        fig.update_yaxes(title_text='<b>Percent</b>', row=row_num, col=col_num,
                         dtick=10)

        if col_num == 2:
            col_num = 1
            row_num += 1
        else:
            col_num = 2

        start += limit
        end += limit

    fig.update_layout(barmode='stack',
                      legend_title='',
                      template='simple_white',
                      hoverlabel_font_color='black',
                      hoverlabel_bordercolor='white',
                      legend_font_size=13,
                      width=2700,
                      height=750*calc_rows
                      )
# legend=dict(
#  orientation='h',
# yanchor='bottom',
# y=1.02,
# xanchor='left')

    fig.update_traces(hovertemplate='<b>%{data.name}</b><br>' +
                                    'Sample=%{x}<br>' +
                                    'Percent=%{y}%<extra></extra>'
                      )

    return fig


'''
if __name__ == '__main__':
    df = pd.read_csv(args.inputfile)
    html = create_html_table(df)
    df = read_data(df)
    fig = create_subplots_2cols(df)

    write_html_file(df, fig, html)

    fig.show()
'''


# HTML table with colors for PASS/Warning
def create_html_table_colour(df5, df6):
    new_df = df5.copy()
    new_df['FLAG'] = ""

    n = 0
    for row in df6['Percent poor quality reads filtered']:
        if df6["Percent poor quality reads filtered"][n] > 10:
            new_df.loc[n, 'FLAG'] = 'Warning'
        else:
            new_df.loc[n, 'FLAG'] = 'PASS'
        n += 1

    def table_colour(val):
        if val == 'Warning':
            color = '#A30000'
        elif val == 'PASS':
            color = '#007500'
        else:
            color = 'black'
        return 'color: %s' % color

    styler = new_df.style.applymap(table_colour)

    # Template handling
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=''))
    template = env.get_template('graph_data_report.html')

    html = template.render(my_table=styler.render())

    return html


'''
if __name__ == '__main__':
    df = pd.read_csv(args.inputfile)
    df2 = read_data(df)
    html = create_html_table_colour(df, df2)
    fig = create_subplots(df2)
    write_html_file(df2, fig, html)
'''


# datapane report with subplots and interactive table
def create_html_table3(df5, df6):
    new_df = df5.copy()
    new_df['FLAG'] = ""

    n = 0
    for row in df6['Percent poor quality reads filtered']:
        if df6["Percent poor quality reads filtered"][n] > 10:
            new_df.loc[n, 'FLAG'] = 'Warning'
        else:
            new_df.loc[n, 'FLAG'] = 'PASS'
        n += 1

    header = "<h1>QC Visualization Report</h1>"
    body = "This is a dehosted QC report for %i samples.<br><br> Note: " \
           "Hover over each bar to see the sample names and the exact " \
           "percentages. <br>" \
           "To remove a variable, click on the variable name in the " \
           "legend. <br>" \
           "To only show one variable, double click on the variable name " \
           "in the legend." % len(df5.index)

    table = dp.DataTable(new_df)
    fig = create_subplots(df6)

    report = dp.Report(header, body, fig, table)
    report.save(
        path='/Users/Vanessa/Desktop/visualization/QC_data_report.html')


'''
if __name__ == '__main__':
    df = pd.read_csv(args.inputfile)
    df2 = read_data(df)
    create_html_table3(df, df2)
'''