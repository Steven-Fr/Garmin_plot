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

df = df[['distance', 'enhanced_speed']]
df['pace'] = 3600/df['enhanced_speed']

parametro1 = df['distance']
parametro2 = df['pace']

parametro2[parametro2 > 480] = 480
# Inizializza l'app Dash
app = dash.Dash(__name__)

# Layout dell'app
app.layout = html.Div(children=[
    html.H1(children='Grafico by Steven'),

    dcc.Graph(
        id='line-plot',
        figure={
            'data': [
                {
                    'x': parametro1,
                    'y': parametro2,
                    'mode': 'lines',
                    'type': 'scatter',
                    'name': 'Passo al km'
                }
            ],
            'layout': {
                'title': 'Grafico Passo sec/km',
                'xaxis': {'title': 'Distanza Km'},
                'yaxis': {'title': 'Passo', 'autorange': 'reversed'}
            }
        }
    ),
    html.Div(id='hover-data')
])


# Callback per aggiornare le informazioni sulla posizione del mouse
@app.callback(
    Output('hover-data', 'children'),
    [Input('line-plot', 'hoverData')]
)
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