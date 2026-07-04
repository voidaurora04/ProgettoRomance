import pandas as pd
import matplotlib.pyplot as plt
import nltk
from collections import Counter
import re
from nltk.corpus import stopwords

# Scarica le risorse se non le hai già
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('italian'))
# Aggiungiamo le parole da escludere al set delle stop words
parole_da_escludere = {'released', 'available', 'purchase'}
stop_words.update(parole_da_escludere)

def pulisci_e_conta(file_csv):
    """Legge il CSV, estrae le trame e conta le parole escludendo quelle specificate."""
    df = pd.read_csv(file_csv, sep=';', encoding='utf-8-sig')
    # Unisce tutte le trame in una sola stringa
    testo = " ".join(df['Trama'].dropna().astype(str))
    parole = re.findall(r'\w+', testo.lower())
    
    # Il filtro ora usa l'insieme aggiornato (incluso released, available, purchase)
    filtrate = [p for p in parole if p not in stop_words and len(p) > 3 and not p.isdigit()]
    return Counter(filtrate).most_common(10)

# 1. Carica e processa i dati dai due file esistenti
cont_2000 = dict(pulisci_e_conta("libri_romance_2000.csv"))
cont_2025 = dict(pulisci_e_conta("libri_romance_2025.csv"))

# 2. Crea un DataFrame unico per il confronto
df_confronto = pd.DataFrame([cont_2000, cont_2025], index=['2000', '2025']).T
df_confronto.fillna(0, inplace=True)

# 3. Genera il grafico a barre raggruppate
df_confronto.plot(kind='bar', figsize=(12, 6), color=['skyblue', 'salmon'])
plt.title("Confronto Parole Chiave: Romance 2000 vs 2025")
plt.ylabel("Frequenza")
plt.xlabel("Parole")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("grafico_confronto_finale.png")
print("Grafico di confronto salvato come 'grafico_confronto_finale.png'")