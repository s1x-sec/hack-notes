---
tags: [privesc, windows, privileges]
---

# Privilegios de Token — Windows

Un privilegio otorga a una security principal el derecho de realizar operaciones de sistema. Deben habilitarse con `AdjustTokenPrivileges` antes de usarse.

Privilegios con impacto total en el sistema:
- **`SeDebugPrivilege`** — handles R/W a cualquier proceso, incluyendo SYSTEM
- **`SeTakeOwnershipPrivilege`** — tomar posesión de cualquier objeto
- **`SeRestorePrivilege`** — reemplazar cualquier archivo
- **`SeLoadDriverPrivilege`** — cargar driver en el kernel
- **`SeCreateTokenPrivilege`** — crear tokens de acceso arbitrarios

| Privilegio | Nota |
|-----------|------|
| SeImpersonatePriv | [[03-post-explotacion/privilege-escalation/windows/privilegios/seimpersonatepriv|SeImpersonatePriv]] |
| SeBackUpPriv | [[03-post-explotacion/privilege-escalation/windows/privilegios/sebackuppriv|SeBackUpPriv]] |
| SeRestorePriv | [[03-post-explotacion/privilege-escalation/windows/privilegios/serestorepriv|SeRestorePriv]] |
| SeManageVolumePriv | [[03-post-explotacion/privilege-escalation/windows/privilegios/semanagevolumepriv|SeManageVolumePriv]] |
