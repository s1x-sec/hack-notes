---
tags: [ports, squid, proxy]
---

# 3128 — Squid Proxy

> [!important]
> Squid actúa como proxy — hay que enumerar qué puerto se encuentra detrás con la herramienta spose

https://github.com/aancw/spose

## Enumeración de Puertos Internos

```bash
python3 spose.py --proxy http://192.168.213.189:3128/ --target 192.168.213.189
```

## Acceso a través del proxy

```bash
# curl forzando el proxy
curl -x http://<IP>:3128 http://127.0.0.1:80/
curl -x http://<IP>:3128 http://127.0.0.1:8080/

# proxychains
# /etc/proxychains.conf → http <IP> 3128
proxychains nmap -sT -Pn 127.0.0.1
proxychains curl http://192.168.1.1/
```

## Autenticación

```bash
# Probar creds por defecto
curl -x http://usuario:contraseña@<IP>:3128 http://google.com
```
