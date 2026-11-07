---
tags: [recon, subdomains, enumeration]
---

# Subdomain Enumeration

_Objetivo: Descubrir la mayor cantidad de subdominios posibles utilizando múltiples fuentes pasivas y agregadores._

---

## Herramientas de Descubrimiento Pasivo

**Subfinder** — fuentes pasivas / APIs:

```bash
subfinder -d target.com -o subfinder.txt
```

**Assetfinder** — búsqueda rápida de activos:

```bash
assetfinder --subs-only target.com > assetfinder.txt
```

**Amass** — enumeración profunda pasiva:

```bash
amass enum -passive -d target.com -o amass.txt
```

**Sublist3r** — motores de búsqueda y fuentes open-source:

```bash
sublist3r -d target.com -o sublist3r.txt
```

**Chaos** — base de datos de ProjectDiscovery:

```bash
chaos -d target.com -silent -o chaos.txt
```

---

## Consolidación y Limpieza

Unir todos los resultados y eliminar duplicados para crear un listado único:

```bash
cat *.txt | sort -u > all_subs.txt
```

---

## Filtrar Hosts Vivos con httpx

```bash
cat all_subs.txt | httpx -silent -status-code -tech-detect -title -o live_hosts.txt
```

```bash
awk '{print $1}' live_hosts.txt > solo_urls.txt
```

---

## URLs Históricas con gau (Wayback Machine)

```bash
cat all_subs.txt | gau --providers wayback,commoncrawl,otx,urlscan > gau_urls.txt
```

---

## VHost / Subdomain Fuzzing con ffuf

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt \
  -u http://192.168.246.229 -H "Host: FUZZ.workaholic.offsec" -ac -k -c
```

