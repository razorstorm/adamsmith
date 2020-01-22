import json
# Import required packages
import datetime
import pandas as pd
import sys


WRITE_TO_DISK = True

def slice_list(list, column_name, func=lambda x: x):
    return [func(e[column_name]) for e in list]


def padded_list(list, value, column_name):
    output = []
    for e in list:
        if e[column_name] == value:
            output.append(1)
        else:
            output.append(0)

    return output


def convert_data():
    data = open('output/fb/output.json', 'r').read()
    messages = json.loads(data)['messages']

    friends = list(set([m['friend_display_name'] for m in messages]))

    # Create an empty dataframe
    df = pd.DataFrame()
    df['time_stamp'] = slice_list(messages, 'time_stamp', func=lambda x: datetime.datetime.fromtimestamp(x/1000.0))

    # Convert that column into a datetime datatype
    df.index = pd.to_datetime(df['time_stamp'])
    df['time_stamp'] = pd.to_datetime(df['time_stamp'])

    index = 0
    num_friends = len(friends)
    for friend in friends:
        df[friend] = padded_list(messages, friend, 'friend_display_name')
        index+=1
        print(index, '/', num_friends, end="\r")

    pd.options.display.float_format = '{:,.0f}'.format
    try:
        converted_output = df.resample('1D').sum().fillna(0)
        if WRITE_TO_DISK:
            converted_output.to_csv('output/out.tsv', encoding='utf-8', sep='\t')
        # data_to_graph(converted_data)
    except Exception:
        import ipdb; ipdb.set_trace()


def data_to_graph(df = None):
    import pandas as pd

    if df is None:
        df = pd.read_csv('output/out.tsv', sep='\t', header=0, index_col=0)

    print(df)
    df.index = pd.to_datetime(df.index)

    # df = df.resample('D').mean()

    normalized = df.sum(axis=1)

    print(normalized)

    df = df.divide(normalized, axis=0).fillna(0)

    # df.to_csv('output/out_normalized.tsv', encoding='utf-8', sep='\t')

    print(df)
    # ax = df.plot(kind='area', stacked=True, title='100 % stacked area chart')
    #
    # ax.set_ylabel('Percent (%)')
    # ax.margins(0, 0)  # Set margins to avoid "whitespace"
    #
    #
    # plt.show()


# only_convert_to_data = bool(sys.argv[1])

convert_data()
