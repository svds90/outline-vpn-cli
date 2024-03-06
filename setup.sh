#!/bin/bash

docker pull svds90/outline-vpn-cli:latest
docker run -dit --restart always --name outline-vpn-cli svds90/outline-vpn-cli

OUTLINE_SCRIPT="/usr/local/bin/outline"

cat <<EOF > $OUTLINE_SCRIPT
docker exec outline-vpn-cli python main.py "\$@"
EOF

chmod +x $OUTLINE_SCRIPT