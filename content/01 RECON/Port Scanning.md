---
tags: [recon, nmap, port-scanning]
---

# Port Scanning

## Hosts Vivos

```bash
sudo nmap -sn 192.168.188.0/24 -oN redexterna.txt
```

Detectar SO por TTL (one-liner):

```bash
while read -r ip; do
  ttl=$(ping -c 1 -W 1 "$ip" 2>/dev/null | grep -oP 'ttl=\K\d+')
  if [ -z "$ttl" ]; then echo "$ip: Inalcanzable"
  elif [ "$ttl" -le 64 ]; then echo "$ip: Linux (TTL=$ttl)"
  else echo "$ip: Windows (TTL=$ttl)"
  fi
done < IPs_Externas_Vivas.txt
```

---

## Escaneo de Puertos

```bash
# Todos los puertos rápido
sudo nmap -p- --open --min-rate 5000 -n -Pn <IP> -oN allports.txt

# Detección de versiones en puertos encontrados
sudo nmap -p <PUERTOS> -sV -sC <IP> -oN targeted.txt

# SO
sudo nmap -O -iL IPs_Externas_Vivas.txt
```

---

## Escaneos Específicos

```bash
# Scripts de vulnerabilidades
sudo nmap -p <PUERTOS> --script vuln <IP>

# Escaneo UDP (SNMP, DNS...)
sudo nmap -sU -p 161,53,123 <IP>

# Escaneo sigiloso (SYN)
sudo nmap -sS -p- <IP>
```

---

## Output

```bash
# Guardar en todos los formatos
sudo nmap -p- -sV <IP> -oA scan_completo

# Leer nmap en grepable
grep "open" scan_completo.gnmap
```

