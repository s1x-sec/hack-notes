---
title: HTTP Host Header Attacks — Metodología
tags: [web, host-header, burp, methodology]
---

# HTTP Host Header Attacks — Metodología

## Concepto clave

El **Host header** define a qué servidor virtual va la petición HTTP. La IP de destino en la capa TCP es diferente al valor del header.

```
GET /index.php HTTP/1.1
Host: www.target.com       ← ESTO puede manipularse
Connection: close
```

> [!important] En Burp Suite puedes modificar el Host header **sin cambiar el destino IP** de la petición. La petición va al mismo servidor pero con un Host diferente.

## Flujo de prueba

1. Enviar la petición a Burp Repeater
2. Modificar el `Host:` header con un valor arbitrario
3. Observar si la aplicación lo refleja o lo usa de alguna forma

## Tipos de validación defectuosa

| Técnica | Descripción |
|---------|-------------|
| Puerto ignorado | `Host: legit.com:1337` — el puerto se ignora en la validación |
| Subdominio matching | `Host: hackdlegit.com` coincide con `*.legit.com` |
| Subdominio comprometido | `Host: evil.legit.com` — tenemos control de ese subdominio |

## Herramientas

- **Burp Suite** — modificar requests manualmente
- **Param Miner** — extensión Burp para descubrir headers ocultos
- **ffuf** — para brute force de virtual hosts

## Ver también
- [[07-web-hacking/ataques/http-host-header/técnicas|Técnicas Host Header]]
- [[07-web-hacking/ataques/http-host-header/escenarios/password-reset-flows|Password Reset Flows]]
