from functions import *


if __name__ == '__main__':
    df = pd.read_csv(args.inputfile)
    df = read_data(df)
    fig = create_subplots(df)
    html = create_html_table(df)
    write_html_file(df, fig, html)