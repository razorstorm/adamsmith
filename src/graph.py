import pandas as pd
# import matplotlib.pyplot as plt

df = pd.read_csv('output/out.tsv', sep='\t', header=0, index_col=0)

print(df)
df.index = pd.to_datetime(df.index)

# df = df.resample('D').mean()

normalized = df.sum(axis=1)

print(normalized)

df = df.divide(normalized, axis=0).fillna(0)

df.to_csv('data/out_normalized.tsv', encoding='utf-8', sep='\t')

print(df)
# ax = df.plot(kind='area', stacked=True, title='100 % stacked area chart')
#
# ax.set_ylabel('Percent (%)')
# ax.margins(0, 0)  # Set margins to avoid "whitespace"
#
#
# plt.show()
