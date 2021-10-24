FROM alpine:3.7

WORKDIR /opt/app

COPY requirements.txt /opt/app/requirements.txt

RUN apk update --no-cache \
    && apk add python3 py3-pip \
    && rm -rf /var/cache/apk/*
RUN pip3 install --no-cache-dir -r requirements.txt

COPY coletor /opt/app/

ENTRYPOINT ["python3", "/opt/app/coletor.py"]

EXPOSE 8080