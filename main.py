import boto3
import cdata.amazondynamodb as mod
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas
import pandas as pd
import plotly
import plotly.graph_objs as go
from boto3.dynamodb.conditions import Key
from dash.dependencies import Output, Input
import datetime
import time

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=False),
        dcc.Interval(
            id='graph-update',
            interval=1 * 1000,
            n_intervals=0
        ),
    ]
)


@app.callback(Output(component_id='live-graph', component_property='figure'),
              [Input(component_id='graph-update', component_property='n_intervals')])
def update_graph_scatter(sensor_data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ArduinoTable')
    response = table.query(
        KeyConditionExpression=Key('mac_Id').eq('00:00:00:00:00:00')
    )
    items = response['Items']
    # print(items)

    cnxn = mod.connect(
        "AWSAccessKey=AKIA2X5UWMUMDQOG4BXY;AWSSecretKey=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;Domain=amazonaws.com;Region=LONDON;")
    df = pd.read_sql("SELECT * FROM ArduinoTable WHERE mac_Id = '00:00:00:00:00:00'", cnxn)

    result_ms = pandas.to_datetime(df['ts'], unit='ms')
    str(result_ms)

    x = result_ms
    y = df.random_number1

    data = plotly.graph_objs.Scatter(x=x, y=y, name='Scatter', mode='lines+markers')

    # return {'data': [data],
    #         'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
    #                             yaxis=dict(range=[min(Y), max(Y)]),
    #                             title='Sensor 1')}
    return {'data': [data],
            'layout': go.Layout(xaxis=dict(tickformat='%Y-%m-%d %H:%M:%S', tickmode='linear'),
                                title='Sensor 1')}

    #
    # layout = plotly.graph_objs.Layout(xaxis={'type': 'date',
    #                                  'tick0': x[0],
    #                                  'tickmode': 'linear',
    #                                  'dtick': 86400000.0 * 14})  # 14 days


# except Exception as e:
#     with open('errors.txt', 'a') as f:
#         f.write(str(e))
#         f.write('\n')

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)
