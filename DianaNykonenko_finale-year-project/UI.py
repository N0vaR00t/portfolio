"""
Get a link as the output and paste into a browser
Plots a graph with historical data for manual analysis
Folling window allows to adjust the amount of details and smoothness of the data
"""

from dash import Dash, dcc, html, Input, Output, State
import yfinance as yf
import pandas as pd
import plotly.express as px

app = Dash(__name__)
server = app.server

app.layout = html.Div([                                                                            # layout: windows, input, butons
    html.H2("Stock Price, Historical Data"),
    
    html.Div([
        html.Label("Enter Stock Symbol:"),
        dcc.Input(id="stock-input", type="text", placeholder="AAPL", debounce=True),
        html.Label("Rolling Window Size:"),
        dcc.Input(id="window-size", type="number", value=5, min=1, step=1),
        html.Button("Fetch & Plot", id="fetch-button", n_clicks=0),
    ], style={'margin-bottom': '20px'}),

    html.Div(id="error-message", style={"color": "red"}),
    dcc.Graph(id="rolling-graph")
])

@app.callback(
    Output("rolling-graph", "figure"),
    Output("error-message", "children"),
    Input("fetch-button", "n_clicks"),
    State("stock-input", "value"),
    State("window-size", "value")
)
def update_graph(n_clicks, symbol, window):                                                        # plot the data for the chosen time period
    if n_clicks == 0 or not symbol:
        return px.scatter(), ""

    try:
        df = yf.download(symbol, start="2020-01-01", end="2025-01-01", progress=False)

        if df.empty:
            return px.scatter(), f"No data returned for: {symbol}"

        df = df[['Close']].copy() 
        df.columns = ['ClosePrice']  
        df = df.reset_index() 

        fig = px.scatter(df, x="Date", y="ClosePrice", 
                         trendline="rolling", 
                         trendline_options=dict(window=window),
                         title=f"{symbol.upper()} Close Price with {window}-Point Rolling Average")

        fig.data = [t for t in fig.data if t.mode == "lines"]
        fig.update_traces(showlegend=True)

        fig.update_layout(template="plotly_white", xaxis_title="Date", yaxis_title="Close Price")

        return fig, ""

    except Exception as e:
        return px.scatter(), f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)