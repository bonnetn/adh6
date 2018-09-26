FROM apereo/cas:v5.3.2
RUN keytool -genkey -keyalg RSA -alias cas -keystore /etc/cas/thekeystore -storepass changeit -validity 9999 -keysize 2048 -dname "cn=cas.local, ou=MyOU, o=MyCompany, c=FR, st=Nord, l=MyCity" && \
    keytool -genkey -keyalg RSA -alias cas -keystore $JAVA_HOME/lib/security/cacerts -storepass changeit -validity 9999 -keysize 2048 -dname "cn=cas.local, ou=MyOU, o=MyCompany, c=FR, st=Nord, l=MyCity" && \
    mkdir /etc/cas/config

COPY ./cas.properties /etc/cas/config/
