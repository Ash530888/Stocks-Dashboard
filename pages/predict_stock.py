import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import pandas as pd

dash.register_page(__name__)

# Load data
companies = ['AAPL', 'GOOG', 'MSFT', 'AMZN']
data = {}
for comp in companies:
    data[comp] = pd.read_csv(f"data/{comp}_stock_data.csv", parse_dates=['Date'], index_col='Date')

layout = html.Div([
        html.H2("Predict Future Stock Prices"),
        html.P("This page could use machine learning models to predict future prices."),
        # Example of placeholder for model predictions
        dcc.Dropdown(
            id='predict-company-dropdown',
            options=[{'label': comp, 'value': comp} for comp in data.keys()],
            value='AAPL',
            clearable=False
        ),
        dcc.Graph(id='predict-graph')
    ])

# Dummy callback for example purposes
@callback(
    Output('predict-graph', 'figure'),
    [Input('predict-company-dropdown', 'value')]
)
def predict_stock_prices(company):
    df = data[company]
    fig = go.Figure(data=go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price'))
    fig.update_layout(title=f"{company} Stock Price Prediction (Dummy Data)", xaxis_title="Date", yaxis_title="Price")
    return fig
