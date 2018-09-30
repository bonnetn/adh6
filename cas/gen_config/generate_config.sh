#!/bin/sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
CONFIG_FILE="$DIR/../OAuthService-123.json"

cp "$DIR/OAuthService-123.json.template" "$CONFIG_FILE"
sed -i "s#{{ ADH6_BASE_URL }}#${ADH6_BASE_URL}#g" $CONFIG_FILE

