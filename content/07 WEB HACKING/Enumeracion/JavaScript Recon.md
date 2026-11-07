---
tags: [web, recon, javascript, secrets]
status: done
---

# JavaScript Recon

> Extraer endpoints, secrets y lógica de aplicación desde archivos JS.

---

## Recolección de URLs JS

```bash
# Extraer todas las URLs históricas + filtrar JS
gau target.com | grep "\.js" | sort -u | tee js_urls.txt

# Descubrir JS activo en el sitio
subjs -i subdomains.txt -o js_urls.txt
```

---

## Descarga y Análisis Local

```bash
# Descargar todos los JS
mkdir js_files && cd js_files
wget -i ../js_urls.txt -q

# Buscar endpoints/rutas en los JS descargados
grep -roP '(?<=["\`])\/[a-zA-Z0-9_\-\/\.]+(?=["\`])' . | sort -u

# Con ripgrep (más rápido)
rg -o '["\`]/[a-zA-Z0-9_\-/\.]{5,}["\`]' . | sort -u
```

---

## LinkFinder — Endpoints desde JS

```bash
# Analizar un archivo JS
python3 linkfinder.py -i target_file.js -o results.html

# Analizar una URL directamente
python3 linkfinder.py -i https://target.com/app.js -o results.html

# Recursivo desde una URL base
python3 linkfinder.py -i https://target.com -d -o results.html
```

---

## Búsqueda de Secrets / Tokens

```bash
# Nuclei — templates de exposición de secrets
nuclei -t ~/nuclei-templates/exposures/tokens/ -l js_urls.txt

# TruffleHog — secrets en código
trufflehog filesystem js_files/

# Búsqueda manual con ripgrep
rg -i "(api.?key|secret|password|token|auth)" js_files/
rg -i "https?://[a-zA-Z0-9\-\.]+\.[a-z]{2,}" js_files/ | grep -v "\.js"
```

---

## Patrones Interesantes a Buscar

```bash
# AWS keys
rg "AKIA[0-9A-Z]{16}" js_files/

# JWT tokens hardcodeados
rg "eyJ[a-zA-Z0-9+/]+" js_files/

# Credenciales en variables
rg -i "(username|user|pass(word)?|pwd)\s*[:=]\s*['\"][^'\"]{3,}" js_files/

# IPs internas
rg "10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(1[6-9]|2[0-9]|3[01])\.\d+" js_files/
```

