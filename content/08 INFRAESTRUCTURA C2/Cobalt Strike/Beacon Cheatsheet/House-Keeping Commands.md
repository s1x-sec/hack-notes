---
title: Cobalt Strike — House-Keeping Commands
tags: [cobalt-strike, beacon, cheatsheet]
---

# House-Keeping Commands

Comandos de gestión general del Beacon.

| Comando | Descripción |
|---------|-------------|
| `help` | Mostrar ayuda |
| `help <cmd>` | Ayuda de un comando específico |
| `checkin` | Forzar check-in con el C2 (útil en DNS) |
| `sleep <segundos> [jitter%]` | Cambiar sleep interval |
| `clear` | Limpiar cola de tareas pendientes |
| `downloads` | Ver descargas pendientes |
| `cancel <*\|file>` | Cancelar descarga |
| `jobs` | Ver jobs en ejecución |
| `note <texto>` | Añadir nota al Beacon (visible en CS) |
| `powershell-import <script.ps1>` | Importar script PS en memoria |
| `ppid <PID>` | Cambiar PPID para nuevos procesos (PPID spoofing) |
| `spawnto x64 <path>` | Cambiar proceso sacrificial |

## Sleep con Jitter

```
beacon> sleep 60 20
```
Duerme 60 segundos ± 20% de variación aleatoria.

> [!tip] Un buen `sleep` + `jitter` es la medida OPSEC más importante. Beacons con sleep < 10s son muy fáciles de detectar.
