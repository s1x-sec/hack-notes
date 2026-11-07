---
title: Cobalt Strike — Comandos de Ejecución
tags: [cobalt-strike, post-ex, shell, run, opsec]
---

# Comandos de Ejecución

| Comando | Descripción | OPSEC |
|---------|-------------|-------|
| `shell <cmd>` | Ejecuta via `cmd.exe /C` | ⚠️ Crea proceso cmd.exe |
| `run <cmd>` | Ejecuta directamente sin cmd.exe | ✅ Mejor |

## Ejemplos

```
beacon> shell whoami
beacon> run whoami
```

## Recomendación OPSEC

Preferir los built-ins del Beacon sobre `shell`:

| Evitar | Usar en su lugar |
|--------|-----------------|
| `shell dir` | `ls` |
| `shell whoami` | `getuid` |
| `shell ipconfig` | `ipconfig` (built-in) |
| `shell net user` | `net user` (built-in) |

> [!warning] `shell` genera eventos de creación de proceso para `cmd.exe` que los EDR monitorizan activamente.
