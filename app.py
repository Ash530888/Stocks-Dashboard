from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# initialising the Dash App
app = Dash(__name__)

# load data
companies = ['AAPL', 'GOOG', 'MSFT', 'AMZN']
data = {}
for comp in companies:
    data[comp] = pd.read_csv(f"data/{comp}_stock_data.csv", parse_dates=['Date'], index_col='Date')

# layout of the Dash app
app.layout = html.Div([
    html.H1("Stock Data Dashboard"),

    # dropdown to select the stock
    dcc.Dropdown(
        id = 'company-dropdown',
        options = [{'label': comp, 'value':comp} for comp in companies],
        value='AAPL', # default value
        clearable=False # cannot be empty

    ),

    # Dropdown to select the column to plot
    dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': col, 'value': col} for col in ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']],
        value='Close',
        clearable=False
    ),

    dcc.Graph(figure={}, id='stock-graph')
])

# callback decorator on function
# defines what triggers calling this function: a dropdown value change
# updates the graph accordingly
@callback(
    Output(component_id='stock-graph', component_property='figure'),
    [Input(component_id='column-dropdown', component_property='value'),
     Input(component_id='company-dropdown', component_property='value')]
)
def update_graph(col_chosen, company_chosen):
    # Filter data for the selected company & col
    df = data[company_chosen][col_chosen]

    print(df.describe())
    print(df.head())
    

    # create the timeseries line graph
    fig = go.Figure(
        data = [go.Scatter(x=df.index, y=df, mode='lines', name=col_chosen)],
        layout = go.Layout(
            title = f"{company_chosen} Stock {col_chosen} Over Time",
            xaxis = dict(title="Date"),
            yaxis = dict(title=col_chosen)
        )
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
