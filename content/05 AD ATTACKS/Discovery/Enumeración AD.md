---
title: AD — Enumeración (nxc + PowerView)
tags: [active-directory, enumeration, nxc, netexec, powerview, recon]
---

# Enumeración AD

## Usuarios y Grupos — PowerView

```powershell
# Usuarios básicos
net user /domain
net user jeffadmin /domain

# PowerView
Get-NetUser
Get-NetUser | select cn
Get-NetUser | select cn,pwdlastset,lastlogon

# Grupos
net group "Sales Department" /domain
net localgroup Administrators
Get-NetGroup | select cn
Get-NetGroup "Sales Department" | select member

# Shares accesibles
Find-DomainShare -CheckShareAccess

# Cuentas con SPN (candidatos a Kerberoast)
Get-NetUser -SPN | select samaccountname,serviceprincipalname

# Cuentas sin preauth (candidatos a AS-REP Roasting)
Get-DomainUser -PreauthNotRequired
```

## Enumeración Externa — NXC (sin autenticación)

```bash
# Listar usuarios via SMB (null session)
nxc smb 10.10.117.152 -u '' -p '' --users

# Exportar usuarios a archivo
nxc smb 10.10.117.152 -u web_svc -p Diamond1 --users-export output.txt

# Con credenciales — listar usuarios via LDAP
nxc ldap 192.168.237.122 -u '' -p '' --users
```

## Ver también
- [[05-ad-attacks/discovery/ldap-discovery|LDAP Discovery]]
- [[05-ad-attacks/kerberos/kerberoasting|Kerberoasting]]
- [[05-ad-attacks/kerberos/as-rep-roasting|AS-REP Roasting]]
- [[05-ad-attacks/discovery/bofhound|BOFHound]]
