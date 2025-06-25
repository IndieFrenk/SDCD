import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Questa funzione viene chiamata quando si crea un nuovo file nella dir osservata
        if event.is_directory:
            return
        filepath = event.src_path
        filename = os.path.basename(filepath)
        if filepath.endswith(".xlsx"):
            print(f"[Trigger] File Excel rilevato: {filename}. Converto in CSV...")
            subprocess.run([
                "docker", "run", "--rm",
                "-v", f"{os.getcwd()}/data:/data",
                "ml-pipeline-converter"  # nome immagine del convertitore
            ], check=True)
            filename = "OnlineRetail.csv"  # dopo la conversione, è questo il nome da usare
    
        if filepath.endswith(".csv"):
                print(f"[Trigger] Nuovo file dataset rilevato: {filename}")
                # Fase 2: avvia il container Docker per il data cleaning
                subprocess.run([
                    "docker", "run", "--rm",
                    "-v", f"{os.getcwd()}/data:/data",           # monta la cartella data/ nel container
                    "-e", f"DATASET_FILE={filename}",            # passa il nome del file dataset come variabile d'ambiente
                    "ml-pipeline-cleaning"                       # nome dell'immagine Docker della funzione di cleaning
                ], check=True)
                print("[Pipeline] Dataset pulito generato, avvio training ML...")
                # Fase 3: avvia il container Docker per il training del modello
                subprocess.run([
                    "docker", "run", "--rm",
                    "-v", f"{os.getcwd()}/data:/data",
                    "ml-pipeline-training"                       # nome dell'immagine Docker della funzione di training
                ], check=True)
                print("[Pipeline] Modello addestrato e salvato, avvio servizio inferenza...")
                # Fase 4: avvia il container Docker per il servizio di inferenza (in background)
                subprocess.run([
                    "docker", "run", "-d", "--name", "ml_inference_service",
                    "-v", f"{os.getcwd()}/data:/data",
                    "-p", "5000:5000",                           # espone la porta 5000 per l'API HTTP
                    "ml-pipeline-inference"                      # nome dell'immagine Docker del servizio di inferenza
                ], check=True)
                print("[Pipeline] Servizio di inferenza avviato (in ascolto su porta 5000).")

if __name__ == "__main__":
    path_to_watch = os.path.join(os.getcwd(), "data/raw")
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=False)
    observer.start()
    try:
        print(f"[*] Monitoraggio avviato sulla cartella {path_to_watch}. In attesa di file...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
