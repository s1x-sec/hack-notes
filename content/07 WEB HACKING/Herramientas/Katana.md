---
tags: [web, recon, crawling, katana]
status: done
---

# Katana — Crawler Web

> Crawlea una aplicación web extrayendo endpoints, formularios y archivos JS.

---

## Crawl básico

```bash
katana --list urls.txt -d 5 -jc -ef css,png,jpg,jpeg,svg,gif,woff,woff2,ttf,ico \
  -H "Cookie: PHPSESSID=f2hp9iqe3dtt55v1c19rbhiplu" \
  -o Crawl_output.txt
```

**Flags:**
- `-d 5` — profundidad máxima 5
- `-jc` — incluye crawl de JavaScript
- `-ef` — excluir extensiones (estáticos irrelevantes)
- `-H` — headers personalizados (útil para autenticación)

---

## Limpiar resultados

```bash
# Quitar archivos JS del crawl (para tenerlos separados)
grep -v -E "\.js(\?|$)" Crawl_output.txt > Crawl_sin_js.txt

# Filtrar solo URLs en scope
grep "target\.domain" Crawl_output.txt > endpoints_scope.txt
```

---

## Extraer parámetros existentes

```bash
# Limpiar params de las URLs
sed 's/\?.*//' solo_urls.txt | sort -u > base_urls.txt
```

```python
# Extraer parámetros que ya venían en las URLs del crawl
import sys
from urllib.parse import urlparse, parse_qs

urls_con_params = set()
with open("solo_urls.txt", "r") as f:
    for line in f:
        line = line.strip()
        if "?" in line:
            parsed = urlparse(line)
            base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            query_params = parse_qs(parsed.query)
            for param in query_params.keys():
                urls_con_params.add(f"{base_url}?{param}=")

with open("params_existentes.txt", "w") as out:
    for item in sorted(urls_con_params):
        out.write(item + "\n")
```

---

## URLs históricas (gau)

```bash
cat all_subs.txt | gau --providers wayback,commoncrawl,otx,urlscan > gau_urls.txt
```
