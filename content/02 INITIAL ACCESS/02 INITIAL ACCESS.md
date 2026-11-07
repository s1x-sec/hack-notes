---
tags: [initial-access]
status: wip
---

# INITIAL ACCESS

> Obtener el primer foothold en el objetivo.

---

## Índice

| Área | Nota |
|------|------|
| Introducción | [[02-initial-access/introducción\|Introducción]] |
| **Delivery / Phishing** | |
| Delivery (cloning, HTML smuggling, SVG) | [[02-initial-access/técnicas/delivery\|Delivery]] |
| Containers — MotW bypass | [[02-initial-access/containers\|Containers]] |
| Triggers (.bat, .lnk, .msc) | [[02-initial-access/triggers\|Triggers]] |
| **Payloads** | |
| Payloads (overview) | [[02-initial-access/payloads\|Payloads]] |
| Payloads Avanzados (DLL, MSI, AppDomain) | [[02-initial-access/payloads/payloads-avanzados\|Payloads Avanzados]] |
| Droppers (C# + GadgetToJScript) | [[02-initial-access/técnicas/droppers\|Droppers]] |

---

## Decision Tree

```
¿Qué vector tienes disponible?
│
├── Email / Phishing → [[Técnicas/Delivery]]
│     ├── HTML Smuggling
│     ├── SVG Smuggling
│     └── Site Cloning (CS)
│
├── Archivo a entregar
│     ├── MotW bloqueando macros → [[Containers/Containers]]
│     ├── Trigger (.lnk/.bat) → [[Triggers/Triggers]]
│     └── Dropper C# / JS → [[Técnicas/Droppers]]
│
├── Web App
│     ├── File Upload RCE
│     └── SQLi / SSRF → [[07 WEB HACKING/07 WEB HACKING]]
│
└── Usuario en red (assumed breach)
      └── Ir directo a [[03 POST EXPLOTACION/03 POST EXPLOTACION]]
```
