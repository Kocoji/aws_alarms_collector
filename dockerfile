FROM python:3.10.5-alpine3.16
WORKDIR /usr/src/app
COPY requirements.txt ./
EXPOSE 8899
RUN pip install --no-cache-dir -r requirements.txt
COPY exporter.py .
ENTRYPOINT [ "python", "./exporter.py" ]