import pandas as pd 
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import yfinance as yf

style = ['https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/minty/bootstrap.min.css']


app = dash.Dash(__name__, external_stylesheets = style)


app.layout = html.Div([
						html.H1("Stock Price Prediction Using Sentiment Analysis", style={'text-align': 'center', 'color':'Blue'}),
						dcc.Graph(id = 'First', figure = {})
						])


def stock_data(ticker, period, interval):
	x =  yf.Ticker(ticker)

	data = x.history(period = period, interval = interval)
	data = data.reset_index()
	print(list(data))
	print(data)


if __name__ == '__main__':
	# app.run_server(debug = True)
	stock_data('TSLA', '1mo','5m')

