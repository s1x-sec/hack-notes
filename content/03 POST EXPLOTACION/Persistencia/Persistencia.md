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
| Registry Keys & Startup | ⚠️ Monitorizado | [[03-post-explotacion/persistencia/registry-keys--and--startup-folder\|Registry Keys & Startup Folder]] |
| Logon Scripts | ⚠️ Monitorizado | [[03-post-explotacion/persistencia/logon-scripts\|Logon Scripts]] |
| PowerShell Profile | 🟡 Moderado | [[03-post-explotacion/persistencia/powershell-profile\|PowerShell Profile]] |
| Scheduled Tasks (CS) | ⚠️ Monitorizado | [[03-post-explotacion/persistencia/scheduled-tasks-cs\|Scheduled Tasks CS]] |
| COM Hijacking | 🟢 Relativamente sigiloso | [[03-post-explotacion/persistencia/com-hijacking\|COM Hijacking]] |
| **Persistencia Avanzada** | | |
| Scheduled Task avanzada | 🟡 Moderado | [[03-post-explotacion/persistencia/persistencia-avanzada/scheduled-task\|Scheduled Task]] |
| Windows Service | ⚠️ Alta detección | [[03-post-explotacion/persistencia/persistencia-avanzada/windows-service\|Windows Service]] |
| WMI Eventing | 🟢 Sigiloso | [[03-post-explotacion/persistencia/persistencia-avanzada/wmi/wmi-eventing\|WMI Eventing]] |
| WMI Queries | — | [[03-post-explotacion/persistencia/persistencia-avanzada/wmi/wmi-queries\|WMI Queries]] |
| WMI Remote Triggers | — | [[03-post-explotacion/persistencia/persistencia-avanzada/wmi/wmi-remote-triggers\|WMI Remote Triggers]] |

---

## Consideración General OPSEC

> La persistencia genera artefactos en disco y en el registro que los EDRs monitorizan activamente. En engagements reales de red team, a menudo se prioriza **no usar persistencia** o usarla solo cuando sea absolutamente necesario (riesgo de ser detectado > beneficio operacional).
