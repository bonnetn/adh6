FROM python:3.7-slim-stretch

ARG APPLICATION_ROOT="/api"
ARG CAS_PROFILE_URL="https://cas.minet.net/"

EXPOSE 443

# Install uwsgi dep
    RUN apt update \
      && apt install -y \
      build-essential \
      python3-dev \
      libpcre3 \
      libpcre3-dev \
      libssl-dev \
      && useradd uwsgi
# Make TLS self-signed certificate
RUN openssl genrsa -out /etc/ssl/private/adh6.key 2048 \
    && openssl req -new -key /etc/ssl/private/adh6.key -out /tmp/adh6.csr -subj "/C=FR/ST=Essonne/O=MiNET/CN=api_server" \
    && openssl x509 -req -days 365 -in /tmp/adh6.csr -signkey /etc/ssl/private/adh6.key -out /etc/ssl/certs/adh6.crt

# Install SQLAlchemy dep
RUN apt install -y libmariadbclient-dev

WORKDIR /adh6/api_server

# Install python requirements
COPY api_server/requirements.txt ./
RUN pip3 install -r ./requirements.txt

# Copy source files
COPY ./openapi/spec.yaml ../openapi/
COPY ./api_server ./

# Generate necessary config file
ENV APPLICATION_ROOT=$APPLICATION_ROOT
ENV CAS_PROFILE_URL=$CAS_PROFILE_URL

RUN /bin/bash ./gen_config/generate_config.sh && rm -rf ./gen_config

# Launch the app 
ENV ENVIRONMENT=testing
CMD ["uwsgi", "--ini", "uwsgi.ini"]
