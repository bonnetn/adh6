FROM python:3.7-slim-stretch

# Make TLS self-signed certificate
RUN openssl genrsa -out /etc/ssl/private/adh6.key 2048 \
    && openssl req -new -key /etc/ssl/private/adh6.key -out /tmp/adh6.csr -subj "/C=FR/ST=Test/L=Test/O=MiNET/CN=localhost" \
    && openssl x509 -req -days 365 -in /tmp/adh6.csr -signkey /etc/ssl/private/adh6.key -out /etc/ssl/certs/adh6.crt

# Install uwsgi dep
    RUN apt update \
      && apt install -y \
      build-essential \
      python3-dev \
      libpcre3 \
      libpcre3-dev \
      libssl-dev \
      && useradd uwsgi

# Install SQLAlchemy dep
RUN apt install -y libmariadbclient-dev

WORKDIR /adh6/api_server

# Install python requirements
COPY api_server/requirements.txt ./
RUN pip3 install -r ./requirements.txt

EXPOSE 443

COPY ./api_server ./
COPY ./openapi/spec.yaml ../openapi/

#CMD ["uwsgi", "--ini", "adh6-api.ini"]
CMD ["/bin/bash"]
