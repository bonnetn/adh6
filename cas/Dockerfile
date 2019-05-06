FROM apereo/cas:v5.3.2

ARG ADH6_BASE_URL="adh6.minet.net/"
ARG CAS_HOST="cas.minet.net"

EXPOSE 8443

# Add OAuth2 dep & rebuild
COPY ./pom.xml /cas-overlay/pom.xml
RUN ./mvnw clean package -T 10 -Dcas.version=5.3.2

# Create some certificates (mandatory)
ENV CAS_HOST=$CAS_HOST
RUN keytool -genkey -keyalg RSA -alias cas -keystore /etc/cas/thekeystore-storepass changeit -validity 9999 -keysize 2048 -dname "cn=$CAS_HOST, ou=MyOU, o=MyCompany, c=FR, st=Nord, l=MyCity"
RUN keytool -genkey -keyalg RSA -alias cas -keystore $JAVA_HOME/lib/security/cacerts -storepass changeit -validity 9999 -keysize 2048 -dname "cn=$CAS_HOST, ou=MyOU, o=MyCompany, c=FR, st=Nord, l=MyCity"
RUN keytool -export -keystore /etc/cas/thekeystore -alias cas -file /tmp/cas.crt
RUN keytool -import -keystore $JAVA_HOME/lib/security/cacerts -file /tmp/cas.crt -alias cas_ca -storepass changeit -noprompt

# Configure CAS
RUN mkdir /etc/cas/config
COPY ./cas.properties /etc/cas/config/

# Generate necessary config file
ENV ADH6_BASE_URL=$ADH6_BASE_URL
RUN sed -i "s#{{ CAS_HOST }}#$CAS_HOST#g" "/etc/cas/config/cas.properties"

COPY ./gen_config ./gen_config
RUN /bin/bash ./gen_config/generate_config.sh && \
    mkdir -p /etc/cas/services && \
    mv ./OAuthService-123.json /etc/cas/services && \
    rm -rf ./gen_config/

# Launch the app
CMD ["/cas-overlay/bin/run-cas.sh"]
