#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd $DIR

# Build the docker image
docker build -f "./Dockerfile" -t adh6_api . && \

# Run it
docker run \
	-it \
	--rm \
	--name api_server \
	--mount type=bind,source=$(pwd),target=/adh6,readonly \
	adh6_api
