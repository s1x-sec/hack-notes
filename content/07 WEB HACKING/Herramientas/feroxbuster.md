---
tags: [web, recon, directorios, feroxbuster, fuzzing]
status: done
---

# feroxbuster — Fuerza Bruta de Directorios

> Fuzzing recursivo de directorios y archivos en aplicaciones web.

---

## Comando estándar

```bash
feroxbuster -u https://target.com \
  -w /usr/share/wordlists/dirb/common.txt \
  -x php,bak,config,env,old,sql,txt,zip,json \
  -t 50 \
  -C 404 \
  --extract-links \
  --depth 3
```

**Flags clave:**
- `-C 404` — filtrar respuestas 404 (ruido)
- `--extract-links` — analiza HTML/JS de las páginas encontradas para extraer más URLs
- `--depth 3` — profundidad máxima de recursión
- `-t 50` — 50 hilos

---

## Con autenticación

```bash
# Cookies
feroxbuster -u https://target.com -w wordlist.txt \
  -b "PHPSESSID=tu_valor; security=low"

# Token Bearer
feroxbuster -u https://target.com -w wordlist.txt \
  -H "Authorization: Bearer eyJhbGciOi..."

# Autenticación HTTP básica
feroxbuster -u https://target.com -w wordlist.txt -u user -p pass
```

---

## A través de Burp Suite

```bash
feroxbuster -u https://target.com -w wordlist.txt --burp
```

---

## Seguir redirects + SSL autofirmado

```bash
feroxbuster -u https://target.com/path/ \
  -w ~/tools/SecLists/Discovery/Web-Content/raft-medium-directories-lowercase.txt \
  -x php,bak,config,env,old,sql,txt,zip,json \
  -t 50 -C 404 --extract-links --depth 3 --burp -r -k
```

---

## Guardar output JSON y filtrar

```bash
feroxbuster -u https://target.com/ \
  -w ~/tools/SecLists/Discovery/Web-Content/raft-medium-directories-lowercase.txt \
  -x php,bak,config,env,old,sql,txt,zip,json \
  -t 50 -C 404 --extract-links --depth 3 -r -k \
  --json --output ferox_urls.json
```
