# First stage: generate API files...
FROM openjdk:8-jre-alpine
ARG PUBLIC_HOSTNAME="adh6.minet.net"

WORKDIR /tmp

# Do not use ADD here, we don't want to redownload the jar every time...
RUN wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.3.1/swagger-codegen-cli-2.3.1.jar -O swagger-codegen-cli.jar


COPY openapi/spec.yaml ./swagger.yaml
RUN sed -i "s/adh6.minet.net/$PUBLIC_HOSTNAME/g" swagger.yaml
RUN java -jar swagger-codegen-cli.jar generate -i "./swagger.yaml" -l typescript-angular -o "./api" --additional-properties ngVersion=6

# 2nd stage, launch the app
FROM node:carbon-slim
ARG PUBLIC_HOSTNAME="adh6.minet.net"

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


USER angular

WORKDIR /adh6/frontend_angular

# Install packages
COPY frontend_angular/package*.json ./
RUN sed -i 's/adh6.minet.net/localhost/g' package.json
RUN npm install

# Copy automatically generated files from previous stage
COPY --from=0 /tmp/api src/app/api


# Copy source code
COPY frontend_angular/ ./

# TODO: Remove that!
USER root
RUN sed -i 's/adh6.minet.net/localhost/g' src/app/http-interceptor/notif-interceptor.ts
RUN sed -i 's/adh6.minet.net/localhost/g' src/app/http-interceptor/auth-interceptor.ts
RUN sed -i 's/PUT_YOUR_SSO_URL_HERE/localhost:8443\/cas/g' src/app/auth.config.ts
RUN sed -i 's/PUT_ADH6_URL_HERE/localhost/g' src/app/auth.config.ts

USER angular

CMD ["npm", "start"]
