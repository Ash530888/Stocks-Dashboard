import dash
from dash import dcc, html, Input, Output, callback_context, callback
import plotly.graph_objs as go
import pandas as pd

# Load data
companies = ['AAPL', 'GOOG', 'MSFT', 'AMZN']
data = {}
for comp in companies:
    data[comp] = pd.read_csv(f"data/{comp}_stock_data.csv", parse_dates=['Date'], index_col='Date')

dash.register_page(__name__)

layout = html.Div([
        html.H2("Visualize Stock Data"),
        #dcc.Store(id='data-store', data={key: df.to_dict('records') for key, df in data.items()}),
        dcc.Dropdown(
            id='company-dropdown',
            options=[{'label': 'ALL', 'value': 'ALL'}] + [{'label': comp, 'value': comp} for comp in data.keys()],
            value='AAPL',
            clearable=False
        ),
        dcc.Dropdown(
            id='column-dropdown',
            options=[{'label': col, 'value': col} for col in ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']],
            value='Close',
            clearable=False
        ),
        dcc.Graph(figure={
            'data': [],
            'layout': {
                'title': 'Select options to visualize stock data',
                'xaxis': {'title': 'Date'},
                'yaxis': {'title': 'Value'}
            }
        }, id='stock-graph')
    ])


@callback(
    Output(component_id='stock-graph', component_property='figure'),
    [Input(component_id='column-dropdown', component_property='value'),
    Input(component_id='company-dropdown', component_property='value')]
)
def render_graph(col_chosen, company_chosen):
    print("Callback triggered")
    fig = go.Figure()

    if company_chosen == "ALL":
        for company, df in data.items():
            fig.add_trace(go.Scatter(
                x=pd.to_datetime(df.index), y=df[col_chosen], mode='lines', name=company
            ))
        title = f"{col_chosen} Over Time for All Companies"
    else:
        df = data[company_chosen]
        fig.add_trace(go.Scatter(
            x=pd.to_datetime(df.index), y=df[col_chosen], mode='lines', name=company_chosen
        ))
        title = f"{company_chosen} Stock {col_chosen} Over Time"

    fig.update_layout(title=title, xaxis_title="Date", yaxis_title=col_chosen)
    return fig
