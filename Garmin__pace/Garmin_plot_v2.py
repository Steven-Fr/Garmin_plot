import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import webbrowser
import threading
import Convertitore_fit_csv
import time
import glob

Convertitore_fit_csv.main()
time.sleep(3)
def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')

# Carica il dataframe

cartella = 'file_fit_csv'
file = glob.glob(os.path.join(cartella, '**', '*.csv'), recursive = True)

df = pd.read_csv(file[0])

df = df[ ['timestamp','position_lat','position_long', 'distance',
          'enhanced_altitude', 'altitude','enhanced_speed','speed',
          'heart_rate','temperature','cadence','fractional_cadence']]


# Crea l'app Dash
app = dash.Dash(__name__)

# Layout dell'app
app.layout = html.Div([
    # Grafico
    dcc.Graph(id='grafico'),

    # Checkboxes per selezionare i parametri
    html.Div([
        dcc.Checklist(
            id='parametri-checkbox',
            options=[{'label': col, 'value': col} for col in df.columns[1:]],
            value=df.columns[1:].tolist(),
            inline=True
        )
    ], style={'margin-top': '20px'})
])



@app.callback(
    Output('grafico', 'figure'),
    [Input('parametri-checkbox', 'value')]
)
def update_graph(selected_params):
    traces = []
    for param in selected_params:
        traces.append(dict(
            x=df['distance'],
            y=df[param],
            mode='lines',
            name=param
        ))

    layout = dict(title='Grafico dati CSV',
                  xaxis=dict(title='distance'),
                  yaxis=dict(title='Valore'))

    return {'distance': traces, 'layout': layout}
def display_hover_data(hover_data):
    if hover_data is None:
        return 'Posizione del mouse: N/D'

    # Estrai informazioni sulla posizione del mouse
    x_value = hover_data['points'][0]['x']
    y_value = hover_data['points'][0]['y']

    return f'Value: Km = {x_value}, passo sec/km = {y_value}'


# Esegui l'app Dash
if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run_server(debug=False)