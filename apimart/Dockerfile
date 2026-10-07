FROM python:3.11-slim
WORKDIR /app
COPY apimart/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY apimart/ .
CMD ["python", "remote_server.py"]
