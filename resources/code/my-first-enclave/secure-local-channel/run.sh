#!/bin/sh

# Assign an IP address to local loopback 
ip addr add 127.0.0.1/32 dev lo

ip link set dev lo up

# Add a hosts record, pointing target site calls to local loopback
echo "127.0.0.1   pro-openapi.debank.com" >> /etc/hosts
echo "127.0.0.1   3.129.1.135" >> /etc/hosts

touch /app/libnsm.so

# Run traffic forwarder in background and start the server
python3 /app/traffic_forwarder.py 127.0.0.1 443 3 8001 &
python3 /app/traffic_forwarder.py 127.0.0.1 5433 3 8002 &
python3 /app/server.py server 5005
