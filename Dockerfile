FROM python:3.12-alpine
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/cache/apk/* /tmp/* /var/tmp/*
COPY . .
CMD ["python", "app.py"]
