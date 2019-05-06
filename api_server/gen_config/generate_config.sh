#!/bin/sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
CONFIG_FILE="$DIR/../config/CONFIGURATION.py" 

cp "$DIR/CONFIGURATION.template" "$CONFIG_FILE"
sed -i "s#{{ CAS_PROFILE_URL }}#${CAS_PROFILE_URL}#g" $CONFIG_FILE
sed -i "s#{{ APPLICATION_ROOT }}#${APPLICATION_ROOT}#g" $CONFIG_FILE

