import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import pandas as pd
#from app import data

# Load data
companies = ['AAPL', 'GOOG', 'MSFT', 'AMZN']
data = {}
for comp in companies:
    data[comp] = pd.read_csv(f"data/{comp}_stock_data.csv", parse_dates=['Date'], index_col='Date')

dash.register_page(__name__)

# Calculates moving avgs and daily returns
def preprocess_data(data, ma_day=[10,20,30]):
    processed_data = {}
    for company, df in data.items():
        # calc moving avg
        for ma in ma_day:
            df[f"MA for {ma} days"] = df['Adj Close'].rolling(ma).mean()

        # calc daily returns
        df['Daily Return'] = df['Adj Close'].pct_change()

        processed_data[company] = df
    
    return processed_data

processed_data = preprocess_data(data)

layout = html.Div([
        html.H2("Data Analysis"),
        
        html.Div([
            html.Label("Select Companies:"),
            dcc.Dropdown(
                id='analysis-company-dropdown',
                options=[{'label': comp, 'value': comp} for comp in processed_data.keys()],
                value=list(processed_data.keys()), # default is all companies
                multi=True,
                clearable=False
            )
        ], style={'margin-bottom': '20px'}),

        html.Div([
            html.Label("Select Analysis"),
            dcc.Checklist(
                id='analysis-toggle',
                options=[
                    {'label': 'Moving Averages', 'value': 'MA'},
                    {'label': 'Daily Returns', 'value': 'DR'}
                ],
                value=['MA'],
                inline=True
            )
        ], style={'margin-bottom': '20px'}),

        dcc.Graph(id='analysis-graph')
    ])


@callback(
    Output('analysis-graph', 'figure'),
    [Input('analysis-company-dropdown', 'value'),
     Input('analysis-toggle', 'value')]
)
def update_analysis_graph(selected_companies, selected_analysis):
    if not selected_analysis or not selected_companies:
        # Return empty figure if no options selected
        return go.Figure()
    
    figure = go.Figure()

    for company in selected_companies:
        df = processed_data[company]

        if 'MA' in selected_analysis:
            # Add Moving Averages plot for each company
            figure.add_trace(go.Scatter(
                x=df.index, y=df['Adj Close'],
                mode='lines', name=f"{company} Adj Close"
            ))
            for ma in [10, 20, 30]:
                figure.add_trace(go.Scatter(
                    x=df.index, y=df[f"MA for {ma} days"],
                    mode='lines', name=f"{company} MA {ma} days"
                ))

        if 'DR' in selected_analysis:
            # Add Daily Returns plot for each company
            figure.add_trace(go.Scatter(
                x=df.index, y=df['Daily Return'],
                mode='markers+lines',
                name=f"{company} Daily Return"
            ))
    
    figure.update_layout(
        title="Data Analysis: Moving Averages and Daily Returns",
        xaxis_title="Date",
        yaxis_title="Value ($)",
        legend_title="Legend",
        height=600
    )

    return figure
    