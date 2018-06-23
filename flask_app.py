from flask import Flask
from flask import render_template
from vis_tools import *
from bokeh.embed import components

app = Flask(__name__)

@app.route('/')
def home():
	return render_template("home.html")

# @app.route('/raw_data')
# def raw_data():
# 	# TODO: this is currently very ugly
#     return emperors_df.to_html()

@app.route('/test')
def test():
	return render_template("sample.html")

@app.route('/deaths')
def deaths():
	plot = rise_fall_heatmap()
	script, div = components(plot)
	return render_template("data_display.html",
							script=script,
							div=div)
# @app.route('/explore_by_emperor/<emperor_id>')
# @app.route('/explore_by_reign/<reign_duration>')
# @app.route('/explore_by_rise_to_power/<rise_to_power>')
# @app.route('/explore_by_death/<death>')
# @app.route('/explore_by_dynasty/<dynasty>')
# @app.route('/explore_by_era/<era>')










