FROM python:3.11-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt && rm -rf /root/.cache

COPY . .

CMD ["python", "app.py"]
