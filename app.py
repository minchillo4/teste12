import pymongo
import dash
import plotly.express as px
import pymongo
import pandas as pd
import plotly.graph_objects as go
import numpy as np

client = pymongo.MongoClient(
    "mongodb://mongo:JX2D3ZJTYtjenJfbxSnl@containers-us-west-70.railway.app:5645"
)

app = dash.Dash(__name__)

app.layout = dash.html.Div(
    [
        dash.html.H1("Crypto Heatmap"),
        dash.dcc.Dropdown(
            id="currency-dropdown",
            options=[
                {"label": "BTC", "value": "BTC"},
                {"label": "ETH", "value": "ETH"},
                {"label": "BNB", "value": "BNB"}
                # Add other currencies here
            ],
            value="BTC",
        ),
        dash.dcc.Dropdown(
            id="timeframe-dropdown",
            options=[
                {"label": "1 Hour", "value": "1hour"},
                {"label": "4 Hours", "value": "4hour"},
                {"label": "1 Day", "value": "daily"},
            ],
            value="daily",
        ),
        dash.dcc.Graph(id="heatmap"),
    ]
)


@app.callback(
    dash.Output("heatmap", "figure"),
    dash.Input("currency-dropdown", "value"),
    dash.Input("timeframe-dropdown", "value"),
)
def update_heatmap(selected_currency, selected_timeframe):
    # Construct the collection name based on selected_currency and selected_timeframe
    collection_name = f"{selected_currency}_{selected_timeframe}"

    # Query MongoDB to retrieve data from the selected collection
    db = client.test  # Replace 'mydatabase' with your actual database name
    collection = db[collection_name]
    data = list(collection.find())
    z = np.array(data[0]["z"])
    x = np.array(data[0]["x"])
    y = np.array(data[0]["y"])
    df_ = data[0]["df"]
    df = pd.DataFrame.from_dict(df_)
    heatmap_trace = go.Heatmap(
        z=z,
        x=x,
        y=y,
        colorscale="blues",
    )

    candlestick_trace = go.Candlestick(
        x=df["Date"],
        open=df["Open"],
        high=df["High"],
        close=df["Close"],
    )
    fig = go.Figure(data=[heatmap_trace])
    fig.add_trace(
        go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
        )
    )
    # Convert the data to a Dat

    # Create the heatmap using Plotly Express

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
