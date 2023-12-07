import os
import pandas as pd
import matplotlib.pyplot as plt
import Convertitore_fit_csv
import time
import glob
from tkinter import Tk, StringVar, OptionMenu, Button

def crea_grafico(file_path, colonna_riferimento):
    # Leggi il file CSV usando pandas
    df = pd.read_csv(file_path)

    # Estrai la colonna di riferimento per l'asse X
    x = df[colonna_riferimento]

    # Crea una finestra di grafico
    plt.figure(figsize=(8, 6))

    # Grafica tutte le colonne eccetto quella di riferimento
    for colonna in df.columns:
        if colonna != colonna_riferimento:
            plt.plot(x, df[colonna], label=colonna)

    # Aggiungi legenda, titoli, ecc.
    plt.legend()
    plt.xlabel(colonna_riferimento)
    plt.ylabel("Valori")
    plt.title("Grafico delle colonne")

    # Mostra il grafico
    plt.show()

# Funzione per gestire la selezione delle colonne da Tkinter
def aggiorna_grafico(opzione, file_path, colonna_riferimento):
    # Leggi il file CSV usando pandas
    df = pd.read_csv(file_path)

    # Estrai la colonna di riferimento per l'asse X
    x = df[colonna_riferimento]

    # Crea una finestra di grafico
    plt.figure(figsize=(8, 6))

    # Grafica solo la colonna selezionata
    plt.plot(x, df[opzione.get()], label=opzione.get())

    # Aggiungi legenda, titoli, ecc.
    plt.legend()
    plt.xlabel(colonna_riferimento)
    plt.ylabel("Valori")
    plt.title(f"Grafico della colonna {opzione.get()}")

    # Mostra il grafico
    plt.show()

# Funzione principale
def main():
    # File CSV di esempio e colonna di riferimento
    file_path = r'file_fit_csv\test.csv'
    colonna_riferimento = 'distance'

    '''Convertitore_fit_csv.main()
    time.sleep(1)
    cartella = 'file_fit_csv'
    file = glob.glob(os.path.join(cartella, '**', '*.csv'), recursive=True)
    df = pd.read_csv(file[0])'''

    # Creazione della finestra Tkinter
    root = Tk()
    root.title("Seleziona la colonna da visualizzare")

    # Opzioni per il menu a discesa
    opzioni = pd.read_csv(file_path).columns.tolist()

    # Variabile di controllo per il menu a discesa
    opzione_selezionata = StringVar(root)
    opzione_selezionata.set(opzioni[0])  # Imposta il valore predefinito

    # Menu a discesa
    menu = OptionMenu(root, opzione_selezionata, *opzioni)
    menu.pack()

    # Bottone per aggiornare il grafico
    aggiorna_grafico_btn = Button(root, text="Aggiorna Grafico", command=lambda: aggiorna_grafico(opzione_selezionata, file_path, colonna_riferimento))
    aggiorna_grafico_btn.pack()

    # Bottone per chiudere la finestra
    chiudi_btn = Button(root, text="Chiudi", command=root.destroy)
    chiudi_btn.pack()

    # Mostra la finestra Tkinter
    root.mainloop()

# Esegui il programma principale
if __name__ == "__main__":
    main()
