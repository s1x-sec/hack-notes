---
title: Cobalt Strike — Process Execution Commands
tags: [cobalt-strike, beacon, cheatsheet, process, shell, run]
---

# Process Execution Commands

Comandos que ejecutan procesos en el objetivo.

| Comando | Descripción | Usa cmd.exe |
|---------|-------------|-------------|
| `shell <cmd>` | Ejecuta via `cmd.exe /C` | ✅ Sí |
| `run <cmd>` | Ejecuta directo (sin shell) | ❌ No |
| `runas DOMAIN\user pass <cmd>` | Ejecuta como otro usuario | Depende |
| `runu <PID> <cmd>` | Ejecuta con el token de un PID | Depende |
| `execute <cmd>` | Ejecuta sin output | ❌ No |
| `powershell <cmd>` | PowerShell.exe | ❌ (usa PS) |

## OPSEC

> [!warning] `shell` genera eventos de creación de proceso para `cmd.exe`. Muchos EDRs alertan sobre `cmd.exe` siendo hijo del proceso implant.

```
# Malo — genera alerta
beacon> shell whoami

# Bueno — API directa
beacon> getuid

# Malo
beacon> shell dir C:\Users

# Bueno — built-in
beacon> ls C:\Users
```

## Cuándo usar `run`

```
beacon> run net user administrator /domain
beacon> run ipconfig /all
beacon> run systeminfo
```

Mejor que `shell` para comandos que no necesitan la shell de Windows.
