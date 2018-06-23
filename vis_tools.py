import pandas as pd
from collections import defaultdict as dd
from itertools import product
from math import pi
from bokeh.models import LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
# use the same color palette
from bokeh.palettes import Category20b as colorp

# global dataframe / columndatasource
emperors_df = pd.DataFrame.from_csv('/home/gcmerz/mysite/emperors.csv')
cd_source = ColumnDataSource(emperors_df)

'''
	function: rise_fall_heatmap
	behavior: extracts information from emperors dataframe
		to creat a heatmap showing how many emperors who
		rose in a certain way fell in a certain way
	returns: seaborn figure
'''
def rise_fall_heatmap():
	# extract unique causes of deaths + means
	# of rising
	deaths = set(emperors_df.cause.values)
	rises = set(emperors_df.rise.values)
	counts = dd(lambda: dd(lambda: 0))

	# extract the counts for each rise + death cause
	for rise, cause in product(rises, deaths):
	    counts[rise][cause] = 0
	for _, row in emperors_df.iterrows():
	    counts[row['rise']][row['cause']] += 1

	# create a correctly formatted dataframe from counts for heatmap
	counts_df = pd.DataFrame.from_dict(counts)
	counts_df.columns.name = 'Rise'
	counts_df.index.name = 'Fall'
	rise = list(counts_df.columns)
	fall= list(counts_df.index)
	counts_df = pd.DataFrame(counts_df.stack()).reset_index()
	counts_df.columns =['Fall', 'Rise', 'Count']

	# set the color-map and available tools
	colors = colorp[max(counts_df['Count'])]
	mapper = LinearColorMapper(palette=colors,
	                            low=counts_df.Count.min(),
	                            high=counts_df.Count.max())
	TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

	# create figure with ecessary settings
	p = figure(title="",
	           x_range=fall,
	           y_range=rise,
	           x_axis_location="above",
	           plot_width=900,
	           plot_height=400,
	           tools=TOOLS,
	           toolbar_location='below',
	           tooltips=[('Rise to Power, Cause of Fall', '@Rise, @Fall'), ('Count', '@Count')])
	p.grid.grid_line_color = None
	p.axis.axis_line_color = None
	p.axis.major_tick_line_color = None
	p.axis.major_label_text_font_size = "8pt"
	p.xaxis.major_label_orientation = pi / 3
	p.xaxis.axis_label = 'Cause of Death'
	p.yaxis.axis_label = 'Means of Rising to Power'
	p.toolbar.logo = None
	p.toolbar_location = None

	# fill the figure with information from the dataframe
	p.rect(x="Fall", y="Rise", width=1, height=1,
	       source=counts_df,
	       fill_color={'field': 'Count', 'transform': mapper},
	       line_color=None)

	# color and return
	color_bar = ColorBar(color_mapper=mapper,
	                     major_label_text_font_size="8pt",
	                     ticker=BasicTicker(desired_num_ticks=len(colors)),
	                     title='Count',
	                     formatter=PrintfTickFormatter(format="%d"),
	                     label_standoff=6, border_line_color=None, location=(0, 0))
	p.add_layout(color_bar, 'right')

	return p


