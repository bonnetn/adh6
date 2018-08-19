FROM python:3.7-slim-stretch

# Install uwsgi dep
RUN apt update \
    && apt install -y \
	build-essential \
	python3-dev \
	libpcre3 \
	libpcre3-dev \
	libssl-dev \
    && useradd uwsgi

EXPOSE 443

# Make TLS self-signed certificate
RUN openssl genrsa -out /etc/ssl/private/adh6.key 2048 \
    && openssl req -new -key /etc/ssl/private/adh6.key -out /tmp/adh6.csr -subj "/C=FR/ST=Essonne/O=MiNET/CN=authentification_server" \
    && openssl x509 -req -days 365 -in /tmp/adh6.csr -signkey /etc/ssl/private/adh6.key -out /etc/ssl/certs/adh6.crt

# Install Authlib dep
RUN apt install -y libsasl2-dev libldap2-dev

WORKDIR /adh6/authentication_server

# Install python requirements
COPY authentication_server/requirements.txt ./
RUN pip3 install -r requirements.txt

COPY openapi/spec.yaml ../openapi/
COPY authentication_server/ ./

CMD ["uwsgi", "--ini", "adh6-authent.ini"]
