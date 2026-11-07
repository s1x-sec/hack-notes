---
tags: [recon, osint]
status: wip
---

# RECON

> Mapear la superficie de ataque antes de interactuar con el objetivo.

---

## Índice

| Técnica |
| --- |
| [[Subdomain Enum]]|
| [[Port Scanning]]|
| [[Web Fingerprinting]]|
| [[OSINT]]|
| [[AD Recon Externo]]|
| [[JavaScript Recon]]|

---

## Flujo

```
Objetivo
  │
  ├── Passivo (sin tocar el objetivo)
  │     ├── OSINT — LinkedIn, Shodan, certs
  │     ├── DNS bruteforce — amass, subfinder
  │     └── GitHub leaks — trufflehog, gitleaks
  │
  └── Activo (tráfico hacia el objetivo)
        ├── Port scan — nmap, masscan
        ├── Web enum — gobuster, feroxbuster
        └── Tech fingerprinting — whatweb
```

---

## Subdomain Discovery

```bash
# Pasivo
subfinder -d target.com -o subs.txt
amass enum -passive -d target.com

# Activo
amass enum -active -d target.com -o subs.txt
gobuster dns -d target.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
```

---

## Port Scanning

```bash
# Top ports — rápido
nmap -sV -sC --top-ports 1000 -oA scan_top target.com

# Completo
nmap -p- -T4 -oA scan_full target.com

# UDP selectivo
nmap -sU -sV --top-ports 100 target.com
```

---

## Web Enumeration

```bash
# Directories
feroxbuster -u https://target.com -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt

# Files
gobuster dir -u https://target.com \
  -w /usr/share/seclists/Discovery/Web-Content/raft-medium-files.txt \
  -x php,txt,html,bak
```

---

## JavaScript Recon

→ Ver [[JavaScript Recon]] para workflow completo.

```bash
# Rápido
gau target.com | grep "\.js" | sort -u | tee js_urls.txt
nuclei -t ~/nuclei-templates/exposures/tokens/ -l js_urls.txt
```

