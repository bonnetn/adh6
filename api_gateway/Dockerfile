FROM python:3.7-slim-stretch
EXPOSE 443

# Install dependencies
RUN apt-get update \
  && apt-get install -y \
  build-essential \
  python3-dev \
  libpcre3 \
  libpcre3-dev \
  libssl-dev \
  && useradd uwsgi



RUN pip install uwsgi

WORKDIR /adh6/api_gateway

# python-ldap requirements
RUN apt-get install -y libsasl2-dev python3-dev libldap2-dev libssl-dev

# Install python requirements
COPY api_gateway/requirements.txt ./
RUN pip3 install -r ./requirements.txt

# Copy source files
COPY ./api_gateway ./

# Launch the app 
CMD ["uwsgi", "--ini", "uwsgi.ini"]
