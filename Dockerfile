FROM python:3.7-alpine
RUN apk add --update build-base python3-dev libffi-dev libxml2 libxml2-dev libxslt-dev openssl-dev libxslt

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000
ENV GUNICORN_CMD_ARGS="--bind=0.0.0:8000 --workers=3" 
#ENTRYPOINT ["gunicorn", "app:app"]
ENTRYPOINT ["python", "app.py"]
#ENTRYPOINT ["/bin/sh"]

