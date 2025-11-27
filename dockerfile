FROM python:3.11-slim

WORKDIR /app

COPY requirments.txt .
RUN pip install --no-cache-dir -r requirments.txt

COPY core ./core
COPY run_web.py .
# COPY database.db .

CMD [ "uvicorn", "core.api:app", "--host", "127.0.0.1", "--port", "8000" ]