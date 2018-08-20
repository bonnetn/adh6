DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd $DIR

# Build the docker image
docker build -f "Dockerfile" -t nginx_test . && \

# Run it
docker run \
	-it \
	--rm \
        -P \
	--name nginx_test \
	nginx_test

