# Garmin_plot
Programmi per graficare i dati di Garmin:

1) Garmin_plot_v1.py
Dentro Garmin__pace c'è il programma Garmin_plot_v1.py
eseguendo questo programma, controlla se nella cartella file_fit_csv è presente un file .fit (ottenibile scaricandolo la nostra attiva dal sito garmin),
se non c'è nessun file .csv corrispettivo crea il file convertendo il .fit
Una volta convertito è possibile avere il grafico del passo sec/km sulla distanza percorsa

2) App.py
Dentro la cartella Garmin_app_All c'è il programma app.py
All'avvio controlla se nella cartella file_fit_csv\csv  è presente almeno un file csv, se non è presente prova converte il file .fit presente in file_fit_csv.
In questa versione abbiamo la presentazione grafica di tutti i dati presenti nell'attività senza trasformazioni sul tempo trascorso dell'attivià, 
possiamo scegliere: 
	-quale file visualiazzare
	-visualizzare i singoli punti oltre alla lingea
	-l'intervallo di tempo ogni dato oppure un dato ogni tot tempo a scelta finoa 1 ora
	-quale intervallo di data? (da sistemare in orario)
 	-a sinistra della leggenda posso scegliere cliccando quale linea tenere visualizzata quale far sparire

