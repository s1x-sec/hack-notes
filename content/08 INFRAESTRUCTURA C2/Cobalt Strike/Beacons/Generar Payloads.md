---
title: Cobalt Strike — Generar Payloads
tags: [cobalt-strike, payloads, stageless, syscalls, code-signing]
---

# Generar Payloads en Cobalt Strike

## Tipos de Payload

| Tipo | Comando CS | Descripción |
|------|-----------|-------------|
| HTA | Attacks → Web Drive-by → Scripted Web Delivery | HTML Application |
| Macro | Attacks → Packages → MS Office Macro | VBA macro |
| Stager (staged) | Attacks → Packages → Payload Generator | Shellcode que descarga el Beacon |
| Stageless | Attacks → Packages → Windows Stageless Payload | Beacon completo embebido |

## Staged vs Stageless

| | Staged | Stageless |
|--|--------|-----------|
| Tamaño | Pequeño (~5KB) | Grande (~250KB) |
| Detección | Más fácil (tráfico stage visible) | Más difícil |
| Recomendación | Inicial Access (AV evasion) | Post-ex, lateral movement |

## Opciones de payload al generar

### Exit Function

| Opción | Comportamiento |
|--------|---------------|
| `ExitProcess` | Mata el proceso entero al terminar |
| `ExitThread` | Solo termina el thread actual (más silencioso) |

> [!important] Siempre usar `ExitThread` en shellcode que se inyecta en procesos ajenos.

## Syscalls

| Tipo | Descripción | OPSEC |
|------|-------------|-------|
| `None` | Win32 API normal | Bajo |
| `Direct` | Instrucción `syscall` desde el beacon | Medio (call stack anómalo) |
| `Indirect` | JMP a `syscall` en ntdll.dll | Alto |

## Tipos de archivo generados

| Formato | Uso |
|---------|-----|
| Windows EXE | Ejecutable standalone |
| Windows Service EXE | Para crear servicios (SCM) |
| DLL | Para sideloading |
| Raw shellcode | Para inyectar en otro proceso/loader |

## Code Signing

```
# Opciones en Cobalt Strike
Attacks → Packages → [payload] → Code Signing Certificate
```

Firmar con certificado (aunque sea autofirmado) ayuda a bypassear ciertos AVs.

## Generate All

`Attacks → Packages → Generate All` — genera todos los formatos de una vez.

## Ver también
- [[Interactuar con Beacons]]
- [[Fork & Run Commands]]
- [[Funcionamiento de EDR]]
