import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import json
import os
import numpy as np  # <-- AGGIUNTO

# --- CONFIGURAZIONE ---
NUMERO_RIGHE_LIMIT = 20 
FILE_OUTPUT = "libri_romance_arricchiti.json"

def recupera_pagina_wikipedia(autore):
    # Pulisci il nome autore da eventuali virgole (es: "Riley, Lucinda" -> "Lucinda Riley")
    if ',' in autore:
        parti = autore.split(',')
        autore = f"{parti[1].strip()} {parti[0].strip()}"
        
    nome_url = autore.replace(" ", "_")
    url = f"https://it.wikipedia.org/wiki/{nome_url}"
    
    # Aggiunto User-Agent per evitare il blocco da parte di Wikipedia
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    print(f"DEBUG: Sto cercando su: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=5) # <-- AGGIUNTO headers
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        else:
            print(f"DEBUG: Pagina non trovata (Codice {response.status_code})")
    except Exception as e:
        print(f"Errore: {e}")
    return None

def estrai_genere(soup):
    """Inferisce il genere dalla prima frase della voce Wikipedia."""
    if not soup:
        return None
    
    # Il primo paragrafo contiene solitamente l'incipit biografico
    paragrafo = soup.find('p')
    if paragrafo:
        testo = paragrafo.get_text().lower()
        if "scrittrice" in testo:
            return "F"
        elif "scrittore" in testo:
            return "M"
    return None

def processa_autori(file_input):
    """Legge i file CSV, interroga Wikipedia e arricchisce i dati."""
    # Caricamento e unione dei dati
    df = pd.concat([pd.read_csv(f, sep=';') for f in file_input], ignore_index=True)
    
    # GESTIONE NAN: Sostituisce i valori NaN di pandas con None (compatibile con JSON)
    df = df.replace({np.nan: None}) 
    
    # Applicazione limite se configurato
    if NUMERO_RIGHE_LIMIT:
        df = df.head(NUMERO_RIGHE_LIMIT)
        
    risultati = []
    statistiche = {"risolti": 0, "mancanti": 0, "non_trovati": 0}

    for _, row in df.iterrows():
        autore = row.get('Autore')
        
        # Gestione caso in cui l'autore sia None dopo la pulizia dei nan
        if autore is None:
            print("Autore non presente (NaN), salto.")
            statistiche["non_trovati"] += 1
            risultati.append(row.to_dict())
            continue

        print(f"Elaborazione autore: {autore}...")
        
        soup = recupera_pagina_wikipedia(autore)
        genere = estrai_genere(soup)
        
        # Creazione dizionario riga
        entry = row.to_dict()
        entry['Genere_Biografico'] = genere
        risultati.append(entry)
        
        # Aggiornamento statistiche
        if genere is not None:
            statistiche["risolti"] += 1
        elif soup is None:
            statistiche["non_trovati"] += 1
        else:
            statistiche["mancanti"] += 1
            
        # Pausa di cortesia di 1 secondo
        time.sleep(1)
            
    return risultati, statistiche

def salva_risultati(data, filename):
    """Salva la lista di dizionari in un file JSON."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    file_csv = ["libri_romance_2000.csv", "libri_romance_2025.csv"]
    
    # Verifica esistenza file
    if all(os.path.exists(f) for f in file_csv):
        print("Inizio elaborazione...")
        dati_arricchiti, stats = processa_autori(file_csv)
        salva_risultati(dati_arricchiti, FILE_OUTPUT)
        
        print(f"\n--- Elaborazione completata: {FILE_OUTPUT} ---")
        print(f"Autori risolti (M/F): {stats['risolti']}")
        print(f"Autori con genere non trovato: {stats['mancanti']}")
        print(f"Pagine Wikipedia non esistenti/raggiungibili: {stats['non_trovati']}")
    else:
        print("Errore: Uno o più file CSV mancanti nella cartella.")