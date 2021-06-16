from functions import *

if __name__ == '__main__':
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