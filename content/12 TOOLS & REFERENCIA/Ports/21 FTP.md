---
tags: [ports, ftp]
status: done
---

# 21 — FTP

---

## Enumeración

```bash
sudo nmap -sC -sV -p 21 <IP>

# Conexión anónima
ftp <IP>
# user: anonymous  pass: anonymous

# Descargar todo (anónimo)
wget -m --no-passive ftp://anonymous:anonymous@<IP>

# Conexión pasiva (bypass firewall)
ftp <IP> -A
```

---

## Fuerza Bruta

```bash
hydra -l user1 -P /usr/share/wordlists/rockyou.txt ftp://<IP>
medusa -u fiona -P /usr/share/wordlists/rockyou.txt -h <IP> -M ftp
```

---

## Bounce Attack

> Escanear la red interna a través del servidor FTP.

```bash
nmap -Pn -v -n -p80 -b anonymous:password@<FTP_IP> <RED_INTERNA>
```

---

## Qué buscar

- Archivos de configuración, backups, .htaccess
- Credenciales en texto plano
- Permisos de escritura → subir webshell
- Versión vulnerable del servidor FTP

