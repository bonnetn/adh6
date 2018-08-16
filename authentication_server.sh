#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd $DIR

# Build the docker image
docker build -f "authentication_server/Dockerfile" -t adh6_authentication . && \

# Run it
docker run \
	-it \
	--rm \
	--name authentication_server \
	--mount type=bind,source=$(pwd),target=/adh6,readonly \
	adh6_authentication
