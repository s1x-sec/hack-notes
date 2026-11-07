---
title: Cobalt Strike — Registro de Windows
tags: [cobalt-strike, post-ex, registry]
---

# Registro de Windows

## Consultar una clave

```
beacon> reg query x64 HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion
```

## Consultar un valor específico

```
beacon> reg queryv x64 HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion ProductName
```

## Parámetros

| Parámetro | Valores |
|-----------|---------|
| Arquitectura | `x64` o `x86` |
| Hive | `HKLM`, `HKCU`, `HKCR`, `HKU`, `HKCC` |

## Escribir valores (persistencia)

```
beacon> reg_set HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run Updater REG_SZ C:\Users\user\AppData\updater.exe
```

> [!tip] Para persistencia, preferir `HKCU` (no requiere privilegios elevados).
