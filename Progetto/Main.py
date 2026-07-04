# file Main per eseguire entrambi i codici tramite un solo comando
import sys
import subprocess

try:
    
    # Esegue il primo file e si ferma se fallisce
    risultato_romance00 = subprocess.run([sys.executable, "Romance_00.py"], check=True)
    
    # Esegue il secondo file e si ferma se fallisce
    risultato_romance25 = subprocess.run([sys.executable, "Romance_25.py"], check=True)
    
    # Esegue il terzo file e si ferma se fallisce
    risultato_confronto = subprocess.run([sys.executable, "Confronto.py"], check=True)

    # Esegue il quarto file e si ferma se fallisce
    risultato_torta = subprocess.run([sys.executable, "GenerazioneTorta.py"], check=True)

    # Esegue il quinto file e si ferma se fallisce
    risultato_genere = subprocess.run([sys.executable, "Genere.py"], check=True)

    # Esegue il sesto file e si ferma se fallisce
    risultato_sintesi = subprocess.run([sys.executable, "Sintesi.py"], check=True)

    # Se il codice arriva qui, significa che tutti sono terminati con successo (returncode = 0)
    print("\n[OK] Tutti i file sono stati eseguiti correttamente!")

except subprocess.CalledProcessError as e:
    # Questo blocco intercetta l'errore se uno dei due file fallisce
    print(f"\n[ERRORE] L'esecuzione si è interrotta. Il file {e.cmd[1]} ha riscontrato un problema.")