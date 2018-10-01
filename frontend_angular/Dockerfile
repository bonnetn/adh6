###############################################################################
# First stage: generate API files...
###############################################################################
FROM openjdk:8-jre-alpine
ARG BASE_ADH6_URL="adh6.minet.net"

WORKDIR /tmp

# Do not use ADD here, we don't want to redownload the jar every time...
RUN wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.3.1/swagger-codegen-cli-2.3.1.jar -O swagger-codegen-cli.jar


COPY openapi/spec.yaml ./swagger.yaml
RUN sed -i "s#adh6.minet.net#$BASE_ADH6_URL#g" swagger.yaml
RUN java -jar swagger-codegen-cli.jar generate -i "./swagger.yaml" -l typescript-angular -o "./api" --additional-properties ngVersion=6


###############################################################################
# 2nd stage, launch the app
###############################################################################
FROM node:carbon-slim

ARG BASE_ADH6_URL="adh6.minet.net"
ARG SSO_LOGOUT="cas.minet.net/logout"
ARG SSO_AUTHORIZE="cas.minet.net/oauth2.0/authorize"

EXPOSE 8443

# Make TLS self-signed certificate
RUN openssl genrsa -out /etc/ssl/private/adh6.key 2048 \
    && openssl req -new -key /etc/ssl/private/adh6.key -out /tmp/adh6.csr -subj "/C=FR/ST=Essonne/O=MiNET/CN=frontend" \
    && openssl x509 -req -days 365 -in /tmp/adh6.csr -signkey /etc/ssl/private/adh6.key -out /etc/ssl/certs/adh6.crt

# Install angular system-wide
RUN npm install -g @angular/cli

# Create an angular user
RUN groupadd -r angular && useradd --no-log-init -r -m -g angular angular && \
    chmod 600 /etc/ssl/private/adh6.key &&\
    chmod 600 /etc/ssl/certs/adh6.crt &&\
    chown angular:angular /etc/ssl/private/adh6.key &&\
    chown angular:angular /etc/ssl/certs/adh6.crt &&\
    mkdir -p /adh6/frontend_angular &&\
    chown angular:angular /adh6/frontend_angular

WORKDIR /adh6/frontend_angular

# Install packages
COPY frontend_angular/package*.json ./

# Need angular user to install package
USER angular
RUN npm install
USER root

# Copy automatically generated files from previous stage
COPY --from=0 /tmp/api src/app/api

# Generate necessary config file
ENV SSO_LOGOUT=$SSO_LOGOUT
ENV SSO_AUTHORIZE=$SSO_AUTHORIZE
ENV BASE_ADH6_URL=${BASE_ADH6_URL}
COPY frontend_angular/gen_config ./gen_config
RUN mkdir -p ./src/app/config && /bin/bash ./gen_config/generate_config.sh && rm -rf ./gen_config

# Copy source code
COPY frontend_angular/*.json ./
COPY frontend_angular/src ./src

USER angular
# We use /bin/sh to be able to use ENV vars...
CMD ["/bin/sh", "-c", "ng serve --public-host ${BASE_ADH6_URL}"]
