# Dockerfile per funzione di Model Training (Fase 3)
FROM python:3.9

# Installazione delle librerie necessarie: pandas e scikit-learn (includerà joblib)
RUN pip install pandas scikit-learn

WORKDIR /app
COPY train.py ./

# Esegue lo script di training all'avvio
CMD ["python", "train.py"]
