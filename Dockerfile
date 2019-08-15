FROM python:3.7.4-alpine

RUN adduser -D bs

WORKDIR /home/bs

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app

COPY bs.py boot.sh ./
RUN chmod +x boot.sh



ENV FLASK_APP bs.py

RUN chown -R bs:bs ./
USER bs

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]