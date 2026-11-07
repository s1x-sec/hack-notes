---
tags: [web]
status: done
---

# WEB HACKING

---

## Índice

| Técnica | Nota |
|---------|------|
| SQL Injection | [[07-web-hacking/sql-injection|SQL Injection]] |
| XSS | [[07-web-hacking/xss|XSS]] |
| SSRF | [[07-web-hacking/ssrf|SSRF]] |
| XXE | [[07-web-hacking/xxe|XXE]] |
| SSTI | [[07-web-hacking/ssti|SSTI]] |
| File Upload | [[07-web-hacking/file-upload|File Upload]] |
| Path Traversal | [[07-web-hacking/path-traversal|Path Traversal]] |
| OAuth / JWT | [[07-web-hacking/oauth-y-jwt|OAuth y JWT]] |
| API Hacking | [[07-web-hacking/api-hacking|API Hacking]] |
| GraphQL | [[07-web-hacking/graphql|GraphQL]] |
| Deserialización | [[07-web-hacking/deserializacion|Deserializacion]] |
| HTTP Host Header | [[07-web-hacking/ataques/http-host-header-attacks|HTTP Host Header Attacks]] |
| JavaScript Recon | [[07-web-hacking/enumeracion/javascript-recon|JavaScript Recon]] |
| WAF Bypass | [[07-web-hacking/waf-bypass|WAF Bypass]] |

---

## Flujo de Reconocimiento Web

```
1. Tech stack   → Wappalyzer, whatweb, headers (X-Powered-By, Server)
2. Endpoints    → ffuf, gobuster, katana (crawl)
3. Parámetros   → arjun, param-miner (Burp Extension)
4. Auth flow    → login / register / reset pass / OAuth tokens
5. File upload  → si existe → [[07-web-hacking/file-upload|File Upload]]
6. APIs         → /api/, /v1/, /graphql → [[07-web-hacking/api-hacking|API Hacking]] [[07-web-hacking/graphql|GraphQL]]
7. JS files     → [[07-web-hacking/enumeracion/javascript-recon|JavaScript Recon]] → endpoints ocultos, secrets
```

---

## Vectores por Input

> [!tip] Qué probar según el contexto
> 
> - **Input reflejado en HTML** → [[07-web-hacking/xss|XSS]]
> - **Input en query SQL** → [[07-web-hacking/sql-injection|SQL Injection]]
> - **Input en URL/ruta** → [[07-web-hacking/ssrf|SSRF]] / [[07-web-hacking/path-traversal|Path Traversal]]
> - **XML en body** → [[07-web-hacking/xxe|XXE]]
> - **Template engine** → [[07-web-hacking/ssti|SSTI]]
> - **Subida de ficheros** → [[07-web-hacking/file-upload|File Upload]]
> - **Token JWT** → [[07-web-hacking/oauth-y-jwt|OAuth y JWT]]
> - **Objeto serializado** → [[07-web-hacking/deserializacion|Deserializacion]]

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
| Subdominios | [[07-web-hacking/enumeracion/subdominios|Subdominios]] |
| Filtrado de hosts vivos | [[07-web-hacking/enumeracion/filtrado|Filtrado]] |
| JavaScript Recon | [[07-web-hacking/enumeracion/javascript-recon|JavaScript Recon]] |

## Herramientas de Fuzzing / Crawl

| Herramienta | Nota |
|-------------|------|
| Katana (crawl) | [[07-web-hacking/herramientas/katana|Katana]] |
| feroxbuster (dirs) | [[07-web-hacking/herramientas/feroxbuster|feroxbuster]] |
| Arjun (parámetros) | [[07-web-hacking/herramientas/arjun|Arjun]] |
| SQLMap | [[07-web-hacking/herramientas/sqlmap|SQLMap]] |
| Dalfox | [[07-web-hacking/herramientas/dalfox|Dalfox]] |

## Reverse Shell desde RCE

→ [[07-web-hacking/enumeracion/rev-shell|Rev Shell]]
