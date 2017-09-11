import pandas as pd
# import matplotlib.pyplot as plt

df = pd.DataFrame.from_csv('output/out.tsv', sep='\t')

df = df.divide(df.sum(axis=1), axis=0).fillna(0)

df.to_csv('output/out_normalized.tsv', encoding='utf-8', sep='\t')

print df
# ax = df.plot(kind='area', stacked=True, title='100 % stacked area chart')
#
# ax.set_ylabel('Percent (%)')
# ax.margins(0, 0)  # Set margins to avoid "whitespace"
#
#
# plt.show()
