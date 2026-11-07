---
tags: [c2, cobalt-strike, infraestructura]
status: done
---

# INFRAESTRUCTURA C2

---

## Cobalt Strike

| Tema | Nota |
|------|------|
| Listeners | [[08-infraestructura-c2/listeners|Listeners]] |
| Beacons (overview) | [[08-infraestructura-c2/cobalt-strike/beacons|Beacons]] |
| Generar Payloads | [[08-infraestructura-c2/cobalt-strike/beacons/generar-payloads|Generar Payloads]] |
| Interactuar con Beacons | [[08-infraestructura-c2/cobalt-strike/beacons/interactuar-con-beacons|Interactuar con Beacons]] |
| Malleable C2 | [[08-infraestructura-c2/cobalt-strike/malleable-c2|Malleable C2]] |
| Fork & Run vs BOF | [[08-infraestructura-c2/cobalt-strike/fork--and--run-vs-bof|Fork & Run vs BOF]] |

---

## Beacon Cheatsheet

| Categoría | Nota |
|-----------|------|
| API-Only Commands | [[08-infraestructura-c2/cobalt-strike/beacon-cheatsheet/api-only-commands|API-Only Commands]] |
| Fork & Run Commands | [[08-infraestructura-c2/cobalt-strike/beacon-cheatsheet/fork--and--run-commands|Fork & Run Commands]] |
| Inline Commands (BOF) | [[08-infraestructura-c2/cobalt-strike/beacon-cheatsheet/inline-commands-(bof)|Inline Commands (BOF)]] |
| Process Execution Commands | [[08-infraestructura-c2/cobalt-strike/beacon-cheatsheet/process-execution-commands|Process Execution Commands]] |
| House-Keeping Commands | [[08-infraestructura-c2/cobalt-strike/beacon-cheatsheet/house-keeping-commands|House-Keeping Commands]] |
| Service Creations | [[08-infraestructura-c2/cobalt-strike/beacon-cheatsheet/service-creations|Service Creations]] |

---

## Selección de Beacon

> [!question] ¿Qué beacon usar?
>
> **¿Hay EDR / inspección de proceso?**
> → Sí → **Stomped** (`module-stomping`) o **Prepended** (bypass de firma)
> → No → **Staged** (menor tamaño inicial) o **Stageless** (todo en payload)
>
> **¿Canal de comunicación?**
> → HTTP/S saliente libre → listener HTTPS con perfil Malleable
> → Solo SMB interno → **SMB Beacon** (peer-to-peer)
> → NAT doble / pivoting → **TCP Beacon** con port forward

---

## Decisión: Fork & Run vs BOF

> [!warning] Impacto OPSEC
>
> | Método | Proceso hijo | Artefacto en disco | Detección |
> |--------|-------------|---------------------|-----------|
> | Fork & Run | Sí (sacrificial) | No | Media — fork visible |
> | BOF (in-process) | No | No | Baja — in-beacon |
> | execute-assembly | Sí (CLR en proc) | No | Alta — ETW / CLR events |
>
> → Regla: **BOF siempre que exista**. Fork & Run solo para herramientas sin BOF port.
> → [[08-infraestructura-c2/cobalt-strike/fork--and--run-vs-bof|Fork & Run vs BOF]] para la config completa del bloque `process-inject`.

---

## Checklist Pre-Operación

> [!abstract] Antes de lanzar
>
> - [ ] Perfil Malleable C2 revisado con ThreatCheck
> - [ ] Staging desactivado en producción (stageless)
> - [ ] Redirector HTTP/S delante del teamserver
> - [ ] `sleep` adecuado al objetivo (30-60s en entornos vigilados)
> - [ ] `block_dlls` activado en post-ex block
> - [ ] Listener SMB listo para movimiento lateral sin salida
