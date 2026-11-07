---
title: HTTP Host Header — Técnicas
tags: [web, host-header, techniques, param-miner]
---

# HTTP Host Header — Técnicas

## 1. Arbitrary Host Header

Cambiar el Host a cualquier valor arbitrario y ver si la aplicación responde normalmente:

```http
GET /index.php HTTP/1.1
Host: evil.attacker.com
```

## 2. Flawed Validation

### Puerto ignorado en validación

```http
Host: legit.com:malicious-stuff
```

Algunas aplicaciones sólo validan la parte del dominio.

### Coincidencia de subdominio

```http
Host: legit.com.attacker.com
```

Puede pasar el filtro `endsWith("legit.com")`.

## 3. Ambiguous Requests

### Duplicate Host headers

```http
GET /index.php HTTP/1.1
Host: legit.com
Host: evil.attacker.com
```

### URL absoluta (override del Host)

```http
GET https://evil.attacker.com/index.php HTTP/1.1
Host: legit.com
```

### Line wrapping

```http
GET /index.php HTTP/1.1
 Host: evil.attacker.com
Host: legit.com
```

## 4. Host Override Headers

Algunos proxies y load balancers respetan estos headers sobre el Host original:

```http
X-Forwarded-Host: evil.attacker.com
X-Host: evil.attacker.com
X-Forwarded-Server: evil.attacker.com
X-HTTP-Host-Override: evil.attacker.com
Forwarded: host=evil.attacker.com
```

> [!tip] Usar la extensión **Param Miner** de Burp para descubrir automáticamente qué headers acepta la aplicación:
> Right-click → Extensions → Param Miner → Guess headers

## Ver también
- [[Metodología Host Header]]
- [[Password Reset Flows]]
- [[Web Cache Poisoning]]
