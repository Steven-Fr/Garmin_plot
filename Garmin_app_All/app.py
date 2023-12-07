from dash.dependencies import Input, Output
from dash import html,dcc
import dash   #problem 1
import plotly.express as px
from datetime import date, datetime
from tqdm import tqdm
import pandas as pd
import webbrowser
import threading
import logging
import time
import sys
import os
import Convertitore_fit_csv
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
import glob



VERSION = '3.0'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=False)

logging.basicConfig(format='[%(levelname)s][%(asctime)s]: %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S',
                    filename=".logfile.log",
                    level=logging.DEBUG
                    )
logging.info('\n------------- Avvio programma')



def tab_to_df(filename):
    cartella = 'file_fit_csv'
    file = glob.glob(os.path.join(cartella, '**', '*.csv'), recursive = True)

    df = pd.read_csv(file[0])

    df = df[['distance', 'enhanced_speed']]
    df['enhanced_speed'] = 3600 / df['enhanced_speed']
    return df


def start_webpage():
    address = 8051
    time.sleep(3)
    webbrowser.open('http://127.0.0.1:' + str(address) + '/', new=0)


def start_window():
    time.sleep(3)
    app = QApplication(sys.argv)
    web = QWebEngineView()
    web.load(QUrl("http://127.0.0.1:8051"))
    web.show()
    sys.exit(app.exec())


def start_dash():
    app.run_server(debug=False, port=8051)


def create_data():
    path = os.getcwd() + '/file_fit_csv/'
    path_dest = path+'csv/'
    dataDict = {}
    if os.path.isdir(path_dest):
        for filename in os.listdir(path_dest):
            print(filename)
            print(path_dest)
            df = pd.read_csv(path_dest +filename)
            try:
                df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S%z')
                df.set_index('timestamp', drop = True, inplace = True)
            except:
                df['timestamp'] = pd.to_datetime(df['timestamp'], format = '%Y-%m-%d %H:%M:%S%z')
                df.set_index('timestamp', drop=True, inplace=True)

            dataDict[filename] = df
    else:
        logging.debug('Creo i file csv')
        for filename in os.listdir(path):
            if filename.endswith('.csv'):

                df = tab_to_df(path + filename)
                df.sort_index(inplace=True)
                dataDict[filename] = df
                df.to_csv(path_dest + filename, index=True)
        logging.debug('File .csv creati in : ' + str(round(((time.process_time() - start) / 60), 2)) + ' minuti')

    return dataDict


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Grafici Tabelle")
        self.setMinimumSize(QSize(1700, 1000))
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:8051/"))
        self.setCentralWidget(self.browser)
        self.show()


dataDict = create_data()

app.layout = html.Div(
    [
        html.Div(
            [
                # --- TITOLO PAGINA
                html.Div(
                    [
                        html.H1(
                            children='Grafici Tabelle (v{})'.format(VERSION),
                            style={
                                # 'height': '3%',
                                'margin-top':    '20px',
                                'textAlign':     'center',
                                'verticalAlign': 'bottom',
                                'margin-bottom': '10px'}
                        )

                        # html.Hr()
                    ],
                    className='title',
                    style={
                        'border-width': '10px',
                        'border-color': 'black'
                    }
                ),

                # --- OPZIONI PAGINA
                html.Div(
                    [
                        html.Div(
                            [
                                'Tabella:',
                                dcc.Dropdown(
                                    id          ='tab_name',
                                    className   ='product',
                                    options     =[{'label': i, 'value': i} for i in dataDict],
                                    value       =next(iter(dataDict)),
                                    clearable   =False
                                ),

                                dcc.Checklist(
                                    id='checklist-item',
                                    options=[{
                                        'label': 'Punti',
                                        'value': 'mk'
                                    }]
                                )
                            ],
                            className='product',
                            style={'width':        '15%',
                                   'display':      'inline-block',
                                   "margin-left":  "50px",
                                   "margin-right": "50px"}
                        ),

                        html.Div(
                            [
                                'Timeframe:',
                                dcc.Dropdown(
                                    id='tf_value',
                                    options=[
                                        {'label': 'Dati grezzi', 'value': 'None'},
                                        {'label': '1 minuti',   'value': '1T'},
                                        {'label': '5 minuti',       'value': '5T'},
                                        {'label': '10 minuti',       'value': '10T'},
                                        {'label': '15 minuti',       'value': '15T'},
                                        {'label': '20 minuti',       'value': '20T'},
                                        {'label': '30 minuti',      'value': '30T'},
                                        {'label': '1 ora',    'value': '1H'}],
                                    value='None',
                                    clearable=False
                                )
                            ],
                            className='product',
                            style={'width': '15%',
                                   'display': 'inline-block',
                                   "margin-right": "50px",
                                   "verticalAlign": "top"}
                        ),

                        dcc.Store(id='output-container-date-picker-range'),

                        html.Div(
                            [
                                'Intervallo Date',
                                dcc.DatePickerRange(
                                    id='my-date-picker-range',
                                    clearable=True,
                                    display_format='DD-MM-YYYY',
                                    start_date_placeholder_text='DD-MM-YYYY',
                                    number_of_months_shown=1,
                                    day_size=50,
                                    # end_date                    =date.today(),
                                    # with_portal                 =True
                                )
                            ],
                            className='product',
                            style={'width': '18%',
                                   'display': 'inline-block',
                                   "verticalAlign": "top"}
                        ),

                        # --- INFO TABELLA
                        html.Div(
                            [
                                html.H5("Info Tabella:"),
                                html.P(id='info-range'),
                                html.P(id='info-points')
                            ],
                            className="info_tab",
                            style={'width': '25%',
                                   'margin-right': '30px',
                                   'float': 'right',
                                   'display': 'inline-block',
                                   "verticalAlign": "top",
                                   'orizontalAlign': 'center'}
                        )
                    ],
                    className='options',
                    style={'margin-top': '20px'}
                )
            ]),

        html.Div(
            [
                # --- GRAFICO
                dcc.Graph(
                    id='indicator-graphic',
                    #responsive=True,
                    config={"displayModeBar": True},
                    figure=dict(
                        layout={
                            'plot_bgcolor': "#1A3E4C",
                            'paper_bgcolor': "#67AFCB"}
                    )
                )

            ],
            style={
                "margin-top": "40px",
                "verticalAlign": "down"},
            className='graph'
        )

    ])


@app.callback(
    Output('indicator-graphic',                 'figure'),
    Output('my-date-picker-range',              'min_date_allowed'),
    Output('my-date-picker-range',              'max_date_allowed'),
    Output('my-date-picker-range',              'initial_visible_month'),
    Output('my-date-picker-range',              'end_date'),
    Output('info-range',                        'children'),
    Output('info-points',                       'children'),
    Input('tab_name',                           'value'),
    Input('tf_value',                           'value'),
    Input('output-container-date-picker-range', 'data'),
    Input('checklist-item',                     'value'))
def update_graph(tab_name, tf_value, data_range, checklist):
    logging.debug('Tabella selezionata: ' + tab_name)

    df = dataDict[tab_name]
    if tf_value != 'None':
        df = df.resample(tf_value).mean()
        logging.debug('Timeframe cambiato: ' + tf_value)

    # mi salvo la data di inizio e quella di fine
    time_start = (str(df.index.min()))[:10]
    time_end = (str(df.index.max()))[:10]

    # se viene selezionato un range di date taglio il dataframe
    if data_range:
        df = df.loc[data_range[0]:data_range[1]]
        logging.debug('Range date cambiato: ' + data_range[0] + '-' + data_range[1])

    fig = px.line(df, render_mode='webgl', height=670)  # , width=1600, height=700)

    if checklist is None or checklist == []:
        # --- aggiungo i pallini per vedere quando sono state rilevate le temperature
        fig.update_traces(mode='lines')
        logging.debug('Markers disattivato')
    else:
        fig.update_traces(mode='markers+lines')
        logging.debug('Markers attivato')

    if 'air_cons' in tab_name:
        fig = px.bar(df)  # , log_y=True)

    fig.update_layout(
        title=tab_name,
        xaxis_title="Time",
        yaxis_title="Value",
        legend_title="Parametri:",
        font=dict(
            size=16,
            color='black'
        ),
        paper_bgcolor="#67AFCB",
        plot_bgcolor="#1A3E4C",
        legend=dict(
            bgcolor='#1A3E4C'
        ),
        legend_font=dict(
            color='#67AFCB'
        )
    )
    fig.update_xaxes(
        showspikes = True,
        spikecolor = "black",
        spikesnap = "cursor",
        spikemode = "across",
        spikedash = "solid",
    )

    fig.update_xaxes(showline=False, linewidth=1, linecolor='black', gridcolor='#67AFCB')
    fig.update_yaxes(showline=False, linewidth=1, linecolor='black', gridcolor='#67AFCB')

    return (
        fig,
        time_start,
        time_end,
        time_start,
        time_end,
        'Intervallo tabella: dal ' + datetime.strptime(time_start, '%Y-%m-%d').strftime('%d/%m/%y')
        + ' al ' + datetime.strptime(time_end, '%Y-%m-%d').strftime('%d/%m/%y'),
        'Numero punti: ' + str(len(df))
    )


@app.callback(
    dash.dependencies.Output('output-container-date-picker-range', 'data'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
    if start_date is None or end_date is None:
        return False
    else:
        return [start_date_object, end_date_object]


if __name__ == '__main__':

    try:
        if dataDict != {}:
            t = threading.Thread(target=start_dash)
            # set thread as Daemon così viene ucciso se il thread principale termina
            t.setDaemon(True)
            t.start()

            time.sleep(3)

            app = QApplication(sys.argv)
            window = MainWindow()

            sys.exit(app.exec())
        else:
            logging.error('Nessuna tabella trovata')
            sys.exit()
    except:
        logging.info('Error: {}. {}, line: {}'.format(sys.exc_info()[0],
                                                      sys.exc_info()[1],
                                                      sys.exc_info()[2].tb_lineno))

