import pandas as pd
import os

def crea_html():
    # 1. Caricamento dati
    df2000 = pd.read_csv("libri_romance_2000.csv", sep=';')
    df2025 = pd.read_csv("libri_romance_2025.csv", sep=';')

    # 2. Struttura HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <title>Report Analisi Romance</title>
        <style>
            body {{ font-family: 'Times New Roman', serif; line-height: 1.6; max-width: 800px; margin: auto; padding: 20px; color: #333; }}
            h1 {{ text-align: center; color: #d63384; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; font-size: 0.9em; }}
            th {{ background-color: #f8f9fa; }}
            img {{ width: 100%; height: auto; margin-bottom: 10px; border: 1px solid #eee; }}
            .analysis {{ background-color: #fff5f8; padding: 15px; border-left: 5px solid #d63384; margin-bottom: 30px; font-style: italic; }}
        </style>
    </head>
    <body>
        <h1>Cuori nel Tempo: Venticinque Anni di Evoluzione del Romance</h1>
        <p>Questo progetto analizza l'evoluzione diacronica del genere <i>Romance</i>, prendendo in esame due segmenti temporali: l'anno 2000 e l'anno 2025. 
            Utilizzando l'API di Google Books come risorsa digitale principale, abbiamo selezionato un campione significativo di 10 titoli per ciascuna annata. 
            L'analisi si è concentrata sulla decostruzione dei metadati (sottogeneri e categorie), sull'analisi semantica delle trame tramite estrazione di parole chiave, 
            e su una valutazione visiva delle tendenze editoriali, per comprendere come sia cambiato — o rimasto immutato — il gusto del pubblico e la proposta narrativa in questo quarto di secolo.</p>

        <section>
            <h2>Tabelle a Confronto</h2>
            <h3>Libri Romance 2000</h3>
            {df2000.to_html(index=False)}
            <h3>Libri Romance 2025</h3>
            {df2025.to_html(index=False)}
        </section>

        <section>
            <h2>Grafici Analitici</h2>
            <h3>Analisi Parole Chiave 2000</h3>
            <img src="grafico_parole_romance_2000.png" alt="Parole Chiave 2000">
            
            <h3>Analisi Parole Chiave 2025</h3>
            <img src="grafico_parole_romance_2025.png" alt="Parole Chiave 2025">
            
            <h3>Confronto Parole Chiave 2000 vs 2025</h3>
            <img src="grafico_confronto_finale.png" alt="Confronto Finale">
            <div class="analysis">
                <p><strong>Nota sull'evoluzione lessicale:</strong> Dall'analisi del confronto emerge un mutamento semantico significativo. Nelle trame del 2025, le parole chiave riflettono una dimensione del desiderio amoroso più esplicita, pragmatica e assertiva (es. <em>"Have", "Want", "More"</em>), suggerendo una narrativa focalizzata sulla conquista e sull'urgenza del sentimento. Al contrario, nel 2000, il lessico era orientato verso una sfera emotiva più astratta, improntata alla speranza e alla linearità dell'attesa (es. <em>"Hope", "With"</em>).</p>
            </div>
            
            <h3>Distribuzione Sottogeneri 2000</h3>
            <img src="torta_romance_2000.png" alt="Torta 2000">
            
            <h3>Distribuzione Sottogeneri 2025</h3>
            <img src="torta_romance_2025.png" alt="Torta 2025">
            <div class="analysis">
                <p><strong>Evoluzione delle Categorie:</strong> La trasformazione dei sottogeneri evidenzia come il <i>Romance</i> abbia oggi assorbito nuove etichette editoriali. Se nel 2000 dominavano le categorie generiche di <i>Fiction</i> e <i>Romance</i>, nel 2025 assistiamo a una frammentazione verso lo <i>Young Adult</i> e il <i>Juvenile Fiction</i>.</p>
                <p>È utile distinguere questi termini: la <em>Fiction</em> è la narrativa di pura invenzione, mentre il <em>Romance</em> si focalizza sulla relazione sentimentale. Lo <em>Young Adult (YA)</em> si rivolge a lettori dai 12 ai 18 anni, esplorando l'identità e la crescita; la <em>Juvenile Fiction</em> (o narrativa per l'infanzia) copre invece fasce d'età più giovani, con tematiche più orientate all'avventura e alla formazione elementare. Questa migrazione indica che il desiderio amoroso è diventato il motore centrale anche per il mercato dei giovani lettori.</p>
            </div>
        </section>
    </body>
    </html>
    """

    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Report aggiornato correttamente: 'report.html'")

if __name__ == "__main__":
    crea_html()