FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt .
COPY opensense_exporter.py .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "opensense_exporter.py"]
