FROM alpine:3.6
EXPOSE 8888
RUN apk add --no-cache python3
RUN pip3 install django==1.8.18 werkzeug gunicorn python-dateutil cinp
COPY src /opt/demo/src
RUN mkdir -p /opt/demo/db ; /opt/demo/src/manage.py migrate
CMD /opt/demo/src/start.py
