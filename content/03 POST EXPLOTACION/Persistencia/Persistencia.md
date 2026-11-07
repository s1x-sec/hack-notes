---
tags: [persistencia, persistence]
status: wip
platform: windows
---

# Persistencia

> Mantener acceso tras reinicios sin necesidad de re-explotar.

---

## Índice

| Técnica | OPSEC | Nota |
|---------|-------|------|
| Registry Keys & Startup | ⚠️ Monitorizado | [[Registry Keys & Startup Folder]] |
| Logon Scripts | ⚠️ Monitorizado | [[Logon Scripts]] |
| PowerShell Profile | 🟡 Moderado | [[PowerShell Profile]] |
| Scheduled Tasks (CS) | ⚠️ Monitorizado | [[Scheduled Tasks CS]] |
| COM Hijacking | 🟢 Relativamente sigiloso | [[COM Hijacking]] |
| **Persistencia Avanzada** | | |
| Scheduled Task avanzada | 🟡 Moderado | [[Persistencia Avanzada/Scheduled Task]] |
| Windows Service | ⚠️ Alta detección | [[Persistencia Avanzada/Windows Service]] |
| WMI Eventing | 🟢 Sigiloso | [[Persistencia Avanzada/WMI/WMI Eventing]] |
| WMI Queries | — | [[Persistencia Avanzada/WMI/WMI Queries]] |
| WMI Remote Triggers | — | [[Persistencia Avanzada/WMI/WMI Remote Triggers]] |

---

## Consideración General OPSEC

> La persistencia genera artefactos en disco y en el registro que los EDRs monitorizan activamente. En engagements reales de red team, a menudo se prioriza **no usar persistencia** o usarla solo cuando sea absolutamente necesario (riesgo de ser detectado > beneficio operacional).
