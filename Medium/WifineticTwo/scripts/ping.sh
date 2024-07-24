#!/bin/bash

MAX_PROCS=100

ping_ip() {
    local ip=$1
    if ping -c 1 -W 1 $ip &> /dev/null; then
        echo "$ip is reachable"
    fi
}

# Rango de IPs
for i in {0..255}; do
    for j in {1..255}; do
        ip="192.168.$i.$j"
        ping_ip $ip &
        while [ $(jobs | wc -l) -ge $MAX_PROCS ]; do
            sleep 0.1
        done
    done
done

wait

echo "Ping test completed."