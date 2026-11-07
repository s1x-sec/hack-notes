---
tags: [recon, web, javascript, secrets]
---

# JavaScript Recon

---

## 1. Descubrimiento y Recopilación de URLs JS

**Filtrar archivos `.js` desde URLs históricas (gau):**

```bash
cat gau_urls.txt | grep -E "\.js(\?[^/]*)?$" | sort -u > js_urls.txt
```

**Extraer enlaces JS directamente de hosts vivos con subjs:**

```bash
cat live_hosts.txt | subjs -c 40 > js_urls.txt
```

---

## 2. Descarga Local de Archivos JS

```bash
mkdir -p downloaded_js && wget -i js_urls.txt -P downloaded_js/ --timeout=5 --tries=2 -q
```

---

## 3. Extracción de Endpoints y Rutas Ocultas

**Análisis con LinkFinder:**

```bash
python3 linkfinder.py -i "https://target.com/assets/main.js" -o cli
```

**Búsqueda rápida de rutas con ripgrep:**

```bash
rg -o "['\"\/][a-zA-Z0-9_\-\/]{3,}(\/?[a-zA-Z0-9_\-\/]*)*['\"]" downloaded_js/
```

---

## 4. Secrets Hunting

**Patrones sensibles comunes:**

```bash
rg -iE "(api[_-]?key|access[_-]?token|authorization|bearer|client[_-]?secret|password|passwd)" downloaded_js/
```

**Escaneo automatizado con Nuclei:**

```bash
nuclei -list js_urls.txt -tags token,exposure,config -o js_secrets.txt
```

---

> [!tip]
> Muchos archivos JS están minificados. Usar `js-beautify` o extensiones del navegador para estructurarlos antes de revisión manual.

