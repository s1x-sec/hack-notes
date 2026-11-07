---
tags: [tool, nmap, recon, network]
status: done
---

# nmap

> Escáner de redes y puertos.

---

## Hosts vivos

```bash
sudo nmap -sn 192.168.188.0/24 -oN redexterna.txt
```

## Sistema operativo de las IPs

```bash
sudo nmap -O -iL IPs_Externas_Vivas.txt
```

## Detectar SO por TTL (oneliner)

```bash
while read -r ip; do
  ttl=$(ping -c 1 -W 1 "$ip" 2>/dev/null | grep -oP 'ttl=\K\d+')
  if [ -z "$ttl" ]; then
    echo "$ip: Inalcanzable"
  elif [ "$ttl" -le 64 ]; then
    echo "$ip: Linux (TTL=$ttl)"
  else
    echo "$ip: Windows (TTL=$ttl)"
  fi
done < IPs_Externas_Vivas.txt
```

---

## Escaneo de puertos completo

```bash
# Top 1000 puertos TCP rápido
nmap -sV -sC -T4 -oN scan.txt <IP>

# Todos los puertos
nmap -p- --min-rate 5000 -T4 <IP> -oN allports.txt

# UDP
sudo nmap -sU --top-ports 100 <IP>
```
