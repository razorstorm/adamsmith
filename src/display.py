import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, output_file, show
from bokeh.transform import linear_cmap
import random

output_file("varea_stack.html")
SAMPLE_SIZE = 158
SAMPLE_NUM_PEOPLE = 521

df = pd.read_csv('output/out.tsv', sep='\t', header=0, index_col=0)

# print(df)
df.index = pd.to_datetime(df.index)

normalized = df.sum(axis=1)
date_column = df.index.tolist()

df = df.divide(normalized, axis=0).fillna(0)

df.to_csv('data/out_normalized.tsv', encoding='utf-8', sep='\t')

raw_data = dict(
    # x=list(range(0, SAMPLE_SIZE))
    x = date_column
)

colors = []
y_lines = []

for (columnName, columnData) in df.iteritems():
   print('Colunm Name : ', columnName)
   y_lines.append(columnName)
   colors.append((random.randint(1,255), random.randint(1,255), random.randint(1,255)))
   raw_data[columnName] = columnData.values
   print('Column Contents : ', columnData.values)
   
source = ColumnDataSource(data=raw_data)

TOOLTIPS = [
    ("index", "$index"),
    ("(x,y)", "($x, $y)")
]
p = figure(plot_width=1500, plot_height=400, tools="reset,wheel_zoom", tooltips=TOOLTIPS, x_axis_type="datetime")

p.varea_stack(y_lines, x='x', color=colors, source=source)

show(p)
