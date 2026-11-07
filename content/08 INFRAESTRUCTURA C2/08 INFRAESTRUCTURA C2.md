---
tags: [c2, cobalt-strike, infraestructura]
status: done
---

# INFRAESTRUCTURA C2

---

## Cobalt Strike

| Tema | Nota |
|------|------|
| Listeners | [[Listeners/Listeners]] |
| Beacons (overview) | [[Cobalt Strike/Beacons]] |
| Generar Payloads | [[Cobalt Strike/Beacons/Generar Payloads]] |
| Interactuar con Beacons | [[Cobalt Strike/Beacons/Interactuar con Beacons]] |
| Malleable C2 | [[Cobalt Strike/Malleable C2]] |
| Fork & Run vs BOF | [[Cobalt Strike/Fork & Run vs BOF]] |

---

## Beacon Cheatsheet

| Categoría | Nota |
|-----------|------|
| API-Only Commands | [[Cobalt Strike/Beacon Cheatsheet/API-Only Commands]] |
| Fork & Run Commands | [[Cobalt Strike/Beacon Cheatsheet/Fork & Run Commands]] |
| Inline Commands (BOF) | [[Cobalt Strike/Beacon Cheatsheet/Inline Commands (BOF)]] |
| Process Execution Commands | [[Cobalt Strike/Beacon Cheatsheet/Process Execution Commands]] |
| House-Keeping Commands | [[Cobalt Strike/Beacon Cheatsheet/House-Keeping Commands]] |
| Service Creations | [[Cobalt Strike/Beacon Cheatsheet/Service Creations]] |

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
> → [[Cobalt Strike/Fork & Run vs BOF]] para la config completa del bloque `process-inject`.

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
