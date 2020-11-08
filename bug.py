from datetime import datetime

import pandas as pd

import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

df = pd.read_pickle("./appl_bug.pkl")

start_date = df.index.min()
end_date = df.index.max()

def get_figure(df, start_date, end_date):
    mask = (df.index >= start_date) & (df.index <= end_date)
    df_filt = df[mask]

    data = go.Candlestick(x=df_filt.index,
                    open=df_filt['Open'],
                    high=df_filt['High'],
                    low=df_filt['Low'],
                    close=df_filt['Close'])
    
    return go.Figure(data=data)

app = dash.Dash()
app.layout = html.Div([
    dcc.DatePickerRange(
        id="ohlc-dates",
        start_date=start_date,
        end_date=end_date,
        display_format='M-D-Y',
    ),
    dcc.Graph(
        id="ohlc", 
        figure=get_figure(df, start_date, end_date),
    )
])

@app.callback(
    Output("ohlc", "figure"),
    [Input("ohlc-dates", "start_date"),
    Input("ohlc-dates", "end_date")]
)
def update_dates(start_date, end_date):
    global df
    return get_figure(df, start_date, end_date)

app.run_server(debug=True)