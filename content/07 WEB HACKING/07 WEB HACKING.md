---
tags: [web]
status: done
---

# WEB HACKING

---

## Índice

| Técnica | Nota |
|---------|------|
| SQL Injection | [[SQL Injection]] |
| XSS | [[XSS]] |
| SSRF | [[SSRF]] |
| XXE | [[XXE]] |
| SSTI | [[SSTI]] |
| File Upload | [[File Upload]] |
| Path Traversal | [[Path Traversal]] |
| OAuth / JWT | [[OAuth y JWT]] |
| API Hacking | [[API Hacking]] |
| GraphQL | [[GraphQL]] |
| Deserialización | [[Deserializacion]] |
| HTTP Host Header | [[HTTP Host Header Attacks]] |
| JavaScript Recon | [[JavaScript Recon]] |
| WAF Bypass | [[WAF Bypass]] |

---

## Flujo de Reconocimiento Web

```
1. Tech stack   → Wappalyzer, whatweb, headers (X-Powered-By, Server)
2. Endpoints    → ffuf, gobuster, katana (crawl)
3. Parámetros   → arjun, param-miner (Burp Extension)
4. Auth flow    → login / register / reset pass / OAuth tokens
5. File upload  → si existe → [[File Upload]]
6. APIs         → /api/, /v1/, /graphql → [[API Hacking]] [[GraphQL]]
7. JS files     → [[JavaScript Recon]] → endpoints ocultos, secrets
```

---

## Vectores por Input

> [!tip] Qué probar según el contexto
> 
> - **Input reflejado en HTML** → [[XSS]]
> - **Input en query SQL** → [[SQL Injection]]
> - **Input en URL/ruta** → [[SSRF]] / [[Path Traversal]]
> - **XML en body** → [[XXE]]
> - **Template engine** → [[SSTI]]
> - **Subida de ficheros** → [[File Upload]]
> - **Token JWT** → [[OAuth y JWT]]
> - **Objeto serializado** → [[Deserializacion]]

---

## Herramientas Rápidas

| Herramienta | Uso |
|-------------|-----|
| `ffuf` | Fuzzing dirs, params, vhosts |
| `sqlmap` | SQLi automatizado |
| `dalfox` | XSS scanning |
| `nuclei` | Templates de vulns conocidas |
| `katana` | Crawling de endpoints |
| `arjun` | Descubrimiento de parámetros |
| `wafw00f` | Identificar WAF |
| Burp Suite | Proxy, repeater, intruder, scanner |


---

## Enumeración

| Técnica | Nota |
|---------|------|
| Subdominios | [[Subdominios]] |
| Filtrado de hosts vivos | [[Filtrado]] |
| JavaScript Recon | [[JavaScript Recon]] |

## Herramientas de Fuzzing / Crawl

| Herramienta | Nota |
|-------------|------|
| Katana (crawl) | [[Katana]] |
| feroxbuster (dirs) | [[feroxbuster]] |
| Arjun (parámetros) | [[Arjun]] |
| SQLMap | [[SQLMap]] |
| Dalfox | [[Dalfox]] |

## Reverse Shell desde RCE

→ [[Rev Shell]]
