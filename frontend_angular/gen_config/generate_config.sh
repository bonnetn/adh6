#!/bin/sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
CONFIG_FILE="$DIR/../src/app/config/auth.config.ts"

cp "$DIR/auth.config.ts.template" "$CONFIG_FILE"
sed -i "s#{{ SSO_LOGOUT }}#${SSO_LOGOUT}#g" $CONFIG_FILE
sed -i "s#{{ SSO_AUTHORIZE }}#${SSO_AUTHORIZE}#g" $CONFIG_FILE
sed -i "s#{{ BASE_ADH6_URL }}#${BASE_ADH6_URL}#g" $CONFIG_FILE

