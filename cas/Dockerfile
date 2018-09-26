FROM apereo/cas:v5.3.2

# Add OAuth2 dep & rebuild
COPY ./pom.xml /cas-overlay/pom.xml
RUN ./mvnw clean package -T 10 -Dcas.version=5.3.2

# Create some certificates (mandatory)
RUN keytool -genkey -keyalg RSA -alias cas -keystore /etc/cas/thekeystore -storepass changeit -validity 9999 -keysize 2048 -dname "cn=localhost, ou=MyOU, o=MyCompany, c=FR, st=Nord, l=MyCity"
RUN keytool -genkey -keyalg RSA -alias cas -keystore $JAVA_HOME/lib/security/cacerts -storepass changeit -validity 9999 -keysize 2048 -dname "cn=localhost, ou=MyOU, o=MyCompany, c=FR, st=Nord, l=MyCity"
RUN keytool -export -keystore /etc/cas/thekeystore -alias cas -file /tmp/cas.crt
RUN keytool -import -keystore $JAVA_HOME/lib/security/cacerts -file /tmp/cas.crt -alias cas_ca -storepass changeit -noprompt

# Configure CAS
RUN mkdir /etc/cas/config
COPY ./cas.properties /etc/cas/config/

# Add a service
RUN mkdir -p /etc/cas/services
COPY ./OAuthService-123.json /etc/cas/services/

CMD ["/cas-overlay/bin/run-cas.sh"]
