---
title: Cobalt Strike — Procesos
tags: [cobalt-strike, post-ex, processes]
---

# Procesos

## Listar procesos (CLI)

```
beacon> ps
```

## Explorador de procesos (GUI)

```
beacon> process_browser
```

O desde el menú: **Explore → Process List**

## Ver detalles relevantes

La salida de `ps` muestra:
- PID / PPID
- Nombre del proceso
- Arquitectura (x64/x86)
- Usuario / sesión
- Integridad

> [!tip] Identificar procesos de usuario legítimos (Word, Chrome, Outlook) como candidatos para PPID spoofing o inyección.
