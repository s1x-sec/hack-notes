---
title: PsExec — Movimiento Lateral
tags: [ad, lateral-movement, psexec, cobalt-strike, beacon]
---

# PsExec — Movimiento Lateral

Herramienta de Sysinternals que ejecuta procesos en un sistema remoto a través del **Service Control Manager (SCM)**.

## Funcionamiento

Es la única técnica que hace **inyección remota por defecto**:
1. Sube el binario al disco de la víctima
2. Crea un nuevo servicio para correrlo
3. El binario del servicio crea un proceso temporal
4. Inyecta el shellcode en el proceso y lo cierra

> [!important] Siempre corre como SYSTEM

## Desde Cobalt Strike

```
beacon> jump psexec64 lon-ws-1 smb
```

> [!warning] OPSEC
> Es **muy ruidoso**. Genera eventos de:
> - Creación de servicio (Event ID 7045)
> - Escritura en disco de binario
> - Named pipe usage

## Ver también
- [[04-lateral-movement/tecnicas/windows-remote-management|Windows Remote Management]]
- [[04-lateral-movement/tecnicas/jump-y-remote-exec|Jump y Remote-Exec]]
- [[04-lateral-movement/tecnicas/custom-techniques|Custom Techniques]]
