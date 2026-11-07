---
title: Cobalt Strike — API-Only Commands
tags: [cobalt-strike, beacon, cheatsheet, api, opsec]
---

# API-Only Commands

Los comandos API-Only usan las **Windows APIs directamente** desde el Beacon. No crean procesos, no inyectan — máximo OPSEC.

| Comando | Descripción |
|---------|-------------|
| `pwd` | Directorio actual |
| `cd <path>` | Cambiar directorio |
| `download <file>` | Descargar archivo |
| `upload <file>` | Subir archivo |
| `ls [path]` | Listar directorio |
| `getuid` | Usuario actual |
| `make_token DOMAIN\user pass` | Crear token de acceso |
| `steal_token <PID>` | Robar token de un proceso |
| `rev2self` | Revertir al token original |
| `kill <PID>` | Matar proceso |
| `exit` | Terminar el Beacon |

> [!tip] Preferir siempre estos sobre `shell whoami`, `shell dir`, etc.

> [!important] Son los comandos más silenciosos — no generan eventos de creación de proceso.
