FROM tiangolo/uwsgi-nginx-flask:python3.7

ENV LISTEN_PORT 8000
ENV PYTHONPATH=/
ENV FLASK_DEBUG 1

EXPOSE 8000

COPY src/requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

COPY src/ /app/
WORKDIR /app