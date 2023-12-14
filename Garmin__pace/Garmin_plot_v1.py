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
from datetime import timedelta
import math
import numpy as np


Convertitore_fit_csv.main() #richiamo la libreria che mi crea il file csv se non presente
time.sleep(1)
def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/') #apro la pagina web in automatico

# Carica il dataframe

cartella = 'file_fit_csv'
file = glob.glob(os.path.join(cartella, '**', '*.csv'), recursive = True) #prendo l'elenco dei file con estensione .csv

df = pd.read_csv(file[0])  #prendo il primo file trovato csv
df = df[['distance', 'enhanced_speed']]   #mi ricavo le 2 colonne di dati distanza e velocita
df['pace'] = 3600/df['enhanced_speed']    #trasformo la velocita da km/h a secondi/km

parametro1 = df['distance']
parametro2 = df['pace']
parametro2[parametro2 > 480] = 480       #se il passo è superiore a 8minuti ignoralo e lascia 8




def calcola_distanza_sopra_velocita(distanze, velocita, velocita_limite):
    distanza_percorsa = 0.0

    for distanza, velocita_istante in zip(distanze, velocita):
        if not np.isnan(velocita_istante) and velocita_istante < velocita_limite:
            distanza_percorsa += distanza

    return distanza_percorsa
print(parametro1[:200])
velocita_limite = 180
distanza_sopra_velocita = calcola_distanza_sopra_velocita(parametro1, parametro2, velocita_limite)
print(distanza_sopra_velocita)





# Funzione per formattare i secondi totali come "minuti:secondi"
def format_seconds(seconds):
    return str(timedelta(seconds=seconds))


# Inizializza l'app Dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#creazione framework web
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=False)

# Layout dell'app
app.layout = html.Div(children=[
    html.H1(children='Grafico by Steven'),   #titolo
    dcc.Graph(
        id='line-plot',
        figure={
            'data': [
                {
                    'x': parametro1,
                    'y': parametro2,
                    'mode': 'lines',         #tipo di grafico linea (markers = a punti)
                    'type': 'scatter',
                    'name': 'Passo al km'
                }
            ],
            'layout': {
                'title': 'Grafico Passo sec/km',
                'xaxis': {'title': 'Distanza Km','gridcolor': 'black'},
                'yaxis': {'title': 'Passo', 'gridcolor': 'black','autorange': 'reversed'},   #inverto i dati dell'asse Y
                'plot_bgcolor': "#1A3E4C",
                'paper_bgcolor': "#67AFCB",
                'grid': {'color': 'red'}
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


#funzione per visualizzare il valore passando sopra il mouse
def display_hover_data(hover_data):
    if hover_data is None:
        return 'Posizione del mouse: N/D'
    # Estrai informazioni sulla posizione del mouse
    x_value = hover_data['points'][0]['x']
    y_value = hover_data['points'][0]['y']
    return f'Value: Km = {x_value}, passo sec/km = {format_seconds(y_value)}' #ritorna la stringa con il valore degli assi

# Esegui l'app Dash
if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run_server(debug=False)