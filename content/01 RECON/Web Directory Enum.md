---
tags: [recon, web, directories, fuzzing]
---

# Web Directory Enumeration

## Crawling con Katana

```bash
katana --list urls.txt -d 5 -jc -ef css,png,jpg,jpeg,svg,gif,woff,woff2,ttf,ico \
  -H "Cookie: PHPSESSID=f2hp9iqe3dtt55v1c19rbhiplu" -o Crawl_output.txt
```

Limpiar resultados:

```bash
# Quitar archivos JS
grep -v -E "\.js(\?|$)" Crawl_output.txt > Crawl_sin_js.txt

# Filtrar solo endpoints en scope
grep "target\.com" Crawl_output.txt > endpoints_scope.txt

# Limpiar parámetros
sed 's/\?.*//' endpoints_scope.txt | sort -u > base_urls.txt
```

---

## Fuzzing de Directorios

**ffuf:**

```bash
ffuf -w /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
  -u http://workaholic.offsec/FUZZ -e php -mc 200,302

ffuf -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt \
  -u http://192.168.213.143:81/FUZZ
```

**feroxbuster:**

```bash
feroxbuster -u https://target.com -w /usr/share/wordlists/dirb/common.txt \
  -x php,bak,config,env,old,sql,txt,zip,json -t 50 -C 404 --extract-links --depth 3

# Con cookies (sesión autenticada)
feroxbuster -u https://target.com -w /usr/share/wordlists/dirb/common.txt \
  -b "PHPSESSID=tu_valor; security=low"

# Con token JWT
feroxbuster -u https://target.com -w /usr/share/wordlists/dirb/common.txt \
  -H "Authorization: Bearer eyJhbGciOi..."

# Salida JSON + burp
feroxbuster -u https://target.com -w wordlist.txt \
  -x php,txt,bak -t 50 -C 404 --extract-links --depth 3 -r -k \
  --json --output ferox_urls.json --burp

# Seguir redirects
feroxbuster -u https://target.com -w wordlist.txt -t 50 -C 404 \
  --extract-links --depth 3 -r -k
```

**gobuster:**

```bash
sudo gobuster dir -w '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt' \
  -u http://$IP:80 -t 42 -b 400,401,403,404 --no-error -x php

gobuster dir -u http://192.168.50.16:5002/users/v1/admin/ \
  -w /usr/share/wordlists/dirb/small.txt
```

---

## URLs Históricas (gau + Wayback)

```bash
cat all_subs.txt | gau --providers wayback,commoncrawl,otx,urlscan > gau_urls.txt
```

---

## Filtrar con httpx

```bash
httpx -l endpoints_scope.txt -status-code -title -o endpoints_vivos.txt
awk '{print $1}' endpoints_vivos.txt > solo_urls.txt
```

