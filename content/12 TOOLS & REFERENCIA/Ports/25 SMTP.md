---
tags: [ports, smtp]
status: done
---

# 25 — SMTP

---

## Enumeración

```bash
nmap -p 25 <IP> -sV
nmap -p 25 --script smtp-enum-users,smtp-open-relay,smtp-commands <IP>
```

---

## User Enumeration

```bash
# VRFY — verificar si un usuario existe
smtp-user-enum -M VRFY -U users.txt -t <IP>

# RCPT TO — también funciona en muchos servidores
smtp-user-enum -M RCPT -D dominio.com -U users.txt -t <IP>

# Manual telnet
telnet <IP> 25
HELO test
VRFY root
VRFY usuario
```

---

## Open Relay

```bash
# Comprobar si el servidor retransmite correos a cualquier destino
swaks --to victim@externo.com --from attacker@dominio.com --server <IP>
```

---

## Phishing via Open Relay

```bash
swaks --to objetivo@empresa.com \
      --from ceo@empresa.com \
      --server <IP> \
      --header "Subject: Urgente" \
      --body "Haz click aquí: http://attacker.com/malware"
```

