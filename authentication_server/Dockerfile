FROM python:3.7-slim-stretch

# Make TLS self-signed certificate
RUN openssl genrsa -out /etc/ssl/private/adh6.key 2048 \
    && openssl req -new -key /etc/ssl/private/adh6.key -out /tmp/adh6.csr -subj "/C=FR/ST=Test/L=Test/O=MiNET/CN=localhost" \
    && openssl x509 -req -days 365 -in /tmp/adh6.csr -signkey /etc/ssl/private/adh6.key -out /etc/ssl/certs/adh6.crt

# Install OS dep
RUN apt update \
    && apt install -y \
	build-essential \
	python3-dev \
	libpcre3 \
	libpcre3-dev \
	libssl-dev \
    && useradd uwsgi

RUN apt-get install -y libsasl2-dev libldap2-dev

WORKDIR /adh6/

# Install python requirements
COPY authentication_server/requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt && rm /tmp/requirements.txt

EXPOSE 443

CMD ["uwsgi", "--ini", "authentication_server/adh6-authent.ini"]
