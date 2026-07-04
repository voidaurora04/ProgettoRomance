import os                       # Gestione di file, cartelle e percorsi del sistema operativo
import requests                 # Invio di richieste HTTP per scaricare dati o testi da internet
import pandas as pd             # Gestione e analisi di dati tabellari (es. leggere/scrivere file CSV)
import matplotlib.pyplot as plt # Creazione di grafici e visualizzazioni statistiche
import nltk                     # Elaborazione e analisi del linguaggio naturale (testo umano)
from collections import Counter # Conteggio rapido ed efficiente degli elementi in una lista
import re                       # Ricerca e pulizia del testo tramite espressioni regolari (pattern)
from dotenv import load_dotenv  # Caricamento sicuro di chiavi segrete e password da file .env

# Carica la chiave API dal file KEY.env
load_dotenv('KEY.env')

# Scarica le risorse necessarie per l'analisi linguistica italiana
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

def estrai_dati_da_api(query):
    """Esegue la chiamata all'API di Google Books."""
    api_key = os.getenv('API_KEY')
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {'q': query, 'maxResults': 10,'printType': 'books', 'inpublisher': '2025', 'langRestrict': 'it', 'orderBy': 'relevance', 'key': api_key}
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        # Se la risposta è positiva, estraiamo gli elementi (libri)
        return response.json().get('items', [])
    else:
        print(f"Errore API: {response.status_code}")
        return []

def elabora_dati(items):
    """Trasforma i dati JSON e filtra i libri nell'intervallo 2020-2030."""
    lista_libri = []
    tutte_le_trame = ""
    
    for item in items:
        info = item.get('volumeInfo', {})
        sale = item.get('saleInfo', {})
        
        # 1. Estrazione anno e gestione errori
        data_pub = info.get('publishedDate', '0000')
        anno = int(data_pub[:4]) if data_pub[:4].isdigit() else 0
        
        # 2. FILTRO TEMPORALE (2025 +/- 5 anni)
        if not (2020 <= anno):
            continue  # Salta i libri fuori dall'intervallo
        
        # Recupera la trama
        trama = info.get('description', '')
        if trama:
            tutte_le_trame += " " + trama
        
        # Recupera le categorie
        categorie = info.get('categories', ['N/A'])
        genere = categorie[0] if categorie else 'N/A'
        
        lista_libri.append({
            'Titolo': info.get('title', 'N/A'),
            'Genere': genere,
            'Autore': ", ".join(info.get('authors', ['N/A'])),
            'Anno di pubblicazione': str(anno),
            'Prezzo': sale.get('listPrice', {}).get('amount', 'N/A'),
            'Trama': trama
        })
    return lista_libri, tutte_le_trame

def genera_grafico_parole(testo):
    """Analizza il testo e salva un grafico a barre delle parole più comuni."""
    # Pulizia: estrai solo le parole (escludendo simboli/punteggiatura)
    parole = re.findall(r'\w+', testo.lower())
    stop_words = set(stopwords.words('italian'))
    
    # Filtro: escludi stop words, parole molto corte o numeri
    filtrate = [p for p in parole if p not in stop_words and len(p) > 3 and not p.isdigit()]
    conteggio = Counter(filtrate).most_common(10)
    
    # Creazione grafico con Matplotlib
    df_parole = pd.DataFrame(conteggio, columns=['Parola', 'Frequenza'])
    plt.figure(figsize=(10, 6))
    plt.bar(df_parole['Parola'], df_parole['Frequenza'], color='salmon')
    plt.title("Top 10 Parole Chiave nelle Trame: Romance 2025")
    plt.xlabel("Parola")
    plt.ylabel("Frequenza")
    plt.savefig("grafico_parole_romance_2025.png")
    print("Grafico delle parole chiave salvato correttamente!")

if __name__ == "__main__":
    # Avvio della pipeline
    print("Inizio estrazione dati (Romance 2025)...")
    
    dati = estrai_dati_da_api("subject:romance 2025")
    
    if dati:
        # Elaborazione
        libri, testo_trame = elabora_dati(dati)
        df = pd.DataFrame(libri)
        
        # Salvataggio CSV (separato da punto e virgola per Excel italiano)
        df.to_csv("libri_romance_2025.csv", index=False, sep=';', encoding='utf-8-sig')
        print("Dati salvati correttamente!")
        
        # Generazione grafico
        genera_grafico_parole(testo_trame)
    else:
        print("Nessun libro trovato o errore di connessione.")