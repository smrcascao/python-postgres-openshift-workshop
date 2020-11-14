FROM python:3.6.6-alpine3.8

LABEL maintainer="smrcascao@gmail.com"

RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev

COPY requirements.txt /requirements.txt

RUN pip3 --no-cache-dir install -r /requirements.txt

ENV APP_ROOT '/application'
RUN mkdir -p $APP_ROOT

WORKDIR $APP_ROOT
COPY . $APP_ROOT

EXPOSE 5000

CMD ["python","-t", "app.py"]