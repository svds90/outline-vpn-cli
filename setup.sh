#!/bin/bash

docker pull svds90/outline-vpn-cli:latest
docker run -dit --name outline-vpn-cli svds90/outline-vpn-cli

UNIT_FILE="/etc/systemd/system/outline-vpn-cli.service"
OUTLINE_SCRIPT="/usr/local/bin/outline"

cat <<EOF > $OUTLINE_SCRIPT
docker exec outline-vpn-cli python main.py "\$@"
EOF

chmod +x $OUTLINE_SCRIPT

cat <<EOF > $UNIT_FILE
[Unit]
Description=Outline VPN CLI
Requires=docker.service
After=docker.service

[Service]
ExecReload=/usr/bin/docker restart -t 1 outline-vpn-cli
ExecStart=/usr/bin/docker start outline-vpn-cli
ExecStop=/usr/bin/docker stop -t 2 outline-vpn-cli

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable outline-vpn-cli