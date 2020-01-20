import json
# Import required packages
import datetime
import pandas as pd


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
        df.resample('1D').sum().fillna(0).to_csv('output/out.tsv', encoding='utf-8', sep='\t')
    except Exception:
        import ipdb; ipdb.set_trace()

convert_data()
