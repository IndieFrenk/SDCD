# Dockerfile per la funzione di conversione Excel → CSV
FROM python:3.9

# Installa pandas e openpyxl per leggere Excel
RUN pip install pandas openpyxl

WORKDIR /app
COPY converter.py ./

CMD ["python", "converter.py"]
