FROM alpine
RUN apk add --update openssl

# Make TLS self-signed certificate
RUN openssl genrsa -out /etc/ssl/private/adh6.key 2048 \
    && openssl req -new -key /etc/ssl/private/adh6.key -out /tmp/adh6.csr -subj "/C=FR/ST=Essonne/O=MiNET/CN=reverse_proxy" \
    && openssl x509 -req -days 365 -in /tmp/adh6.csr -signkey /etc/ssl/private/adh6.key -out /etc/ssl/certs/adh6.crt

FROM nginx

COPY --from=0 /etc/ssl/certs/adh6.crt /etc/ssl/certs/
COPY --from=0 /etc/ssl/private/adh6.key /etc/ssl/private/

COPY adh6.conf /etc/nginx/conf.d/
RUN rm /etc/nginx/conf.d/default.conf

