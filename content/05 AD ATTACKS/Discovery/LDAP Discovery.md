---
title: LDAP Discovery
tags: [ad, ldap, discovery, enumeration]
---

# LDAP Discovery

LDAP (puertos 389/636/3268/3269) es el protocolo para acceder a información del dominio desde el DC.

## Object Classes principales

| Clase | Descripción |
|-------|-------------|
| `computer` | Cuenta de equipo en el dominio |
| `domain` | Información del dominio |
| `group` | Lista de usuarios para aplicar SPs |
| `person` | Información de usuario |
| `groupPolicyContainer` | Almacena GPOs |
| `organizationalUnit` | Contenedor de usuarios/equipos |
| `trustedDomain` | Relación de confianza entre dominios |

## Queries LDAP con ldapsearch

```bash
# Enumeración básica sin creds (null session)
ldapsearch -x -H ldap://192.168.1.10 -b "DC=domain,DC=com"

# Con credenciales
ldapsearch -x -H ldap://192.168.1.10 -D "CN=user,DC=domain,DC=com" -w password -b "DC=domain,DC=com" "(objectClass=user)"

# Buscar usuarios con SPN (Kerberoasting)
ldapsearch -x -H ldap://192.168.1.10 -D "user@domain.com" -w password -b "DC=domain,DC=com" "(&(objectClass=user)(servicePrincipalName=*))" sAMAccountName servicePrincipalName
```

## Ver también
- [[12-tools--and--referencia/ports/389-ldap|389 LDAP]] (puerto)
- [[05-ad-attacks/discovery/bofhound|BOFHound]]
- [[05-ad-attacks/kerberos/kerberoasting|Kerberoasting]]
