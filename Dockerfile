FROM python:3.8-alpine

RUN apk --update add redis
RUN apk --update add nano supervisor 

ENV HOME=/home/app
RUN mkdir $HOME
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME
# WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
# COPY ./requirements.txt /usr/src/app/web/requirements.txt
COPY ./requirements.txt /home/app/web/requirements.txt
RUN pip install -r /home/app/web/requirements.txt

# COPY ./entrypoint.sh /usr/src/app/web/entrypoint.sh
COPY ./entrypoint.sh /home/app/web/entrypoint.sh
COPY ./entrypoint.sh /home/app/web/bhavcopy/entrypoint.sh

COPY ./bhavcopy $APP_HOME
ADD /supervisor /home/app/web/supervisor

CMD ["supervisord","-c","/home/app/web/supervisor/service_script.conf"]

# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
# ENTRYPOINT ["/home/app/web/entrypoint.sh"]

# CMD gunicorn bhavcopy.wsgi:application --bind 0.0.0.0:$PORT