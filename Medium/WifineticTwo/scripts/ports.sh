#!/bin/bash

if [ -z "$1" ]; then
    echo "Uso: $0 <IP>"
    exit 1
fi

IP=$1

scan_port() {
    local ip=$1
    local port=$2
    nc -z -w 1 $ip $port &> /dev/null
    if [ $? -eq 0 ]; then
        echo "Puerto $port está abierto en $ip"
    fi
}

export -f scan_port
seq 1 65535 | xargs -I{} -P 100 bash -c 'scan_port '"$IP"' {}'

echo "Escaneo de puertos completado."