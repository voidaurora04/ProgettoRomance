import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def genera_grafico_torta(file_csv, titolo, nome_file_output):
    """Legge il CSV, conta i generi e genera un grafico a torta in tonalità rosa."""
    df = pd.read_csv(file_csv, sep=';', encoding='utf-8-sig')
    
    # Conta le occorrenze per ogni genere
    conteggio_generi = df['Genere'].value_counts()
    
    # Genera colori in scala di rosa (dal rosa chiaro al magenta)
    num_generi = len(conteggio_generi)
    colori = plt.cm.RdPu(np.linspace(0.3, 0.8, num_generi))
    
    # Creazione grafico
    plt.figure(figsize=(10, 7))
    plt.pie(
        conteggio_generi, 
        labels=None, # Rimuoviamo le label interne per pulizia
        autopct='%1.1f%%', 
        colors=colori, 
        startangle=140
    )
    
    plt.title(titolo)
    # Legenda a destra
    plt.legend(conteggio_generi.index, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.tight_layout()
    plt.savefig(nome_file_output)
    print(f"Grafico salvato come '{nome_file_output}'")

# Generazione dei due grafici
genera_grafico_torta("libri_romance_2000.csv", "Tipologie di Romance 2000", "torta_romance_2000.png")
genera_grafico_torta("libri_romance_2025.csv", "Tipologie di Romance 2025", "torta_romance_2025.png")