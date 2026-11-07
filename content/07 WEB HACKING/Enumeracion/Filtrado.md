---
tags: [web, recon, httpx, filtrado]
status: done
---

# Filtrado de Hosts Vivos

> Identificar qué URLs / subdominios responden a HTTP/HTTPS.

---

## HTTPX

```bash
# Desde lista de endpoints específicos
httpx -l endpoints_scope.txt -status-code -title -o endpoints_vivos.txt

# Extraer solo las URLs limpias
awk '{print $1}' endpoints_vivos.txt > solo_urls.txt
```

## Desde subdominios

```bash
# Con detección de tecnologías
cat all_subs.txt | httpx -silent -status-code -tech-detect -title -o live_hosts.txt
```

---

## Flujo completo

```
all_subs.txt → httpx → live_hosts.txt → katana / feroxbuster
```
