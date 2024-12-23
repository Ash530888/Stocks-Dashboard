import dash
from dash import Dash, dcc, html, Input, Output
from dash.exceptions import PreventUpdate
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(__name__, suppress_callback_exceptions=True, use_pages=True)


app.layout = html.Div([
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])



if __name__ == '__main__':
    app.run_server(debug=True)
