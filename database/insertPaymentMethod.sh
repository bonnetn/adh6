#! /bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 IP_address payment_method_name_to_insert"
    exit 1
fi

mysql -u adh6 -h $1 -p << EOF

USE adh6;
INSERT INTO payment_method (name) VALUES ('$2');

EOF

