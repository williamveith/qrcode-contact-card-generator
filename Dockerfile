FROM python:3.12-alpine
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt && \
    rm -rf /var/cache/apk/* /tmp/* /var/tmp/*
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]