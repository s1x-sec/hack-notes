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
| Introducción | [[Introducción]] |
| **Delivery / Phishing** | |
| Delivery (cloning, HTML smuggling, SVG) | [[Técnicas/Delivery]] |
| Containers — MotW bypass | [[Containers/Containers]] |
| Triggers (.bat, .lnk, .msc) | [[Triggers/Triggers]] |
| **Payloads** | |
| Payloads (overview) | [[Payloads/Payloads]] |
| Payloads Avanzados (DLL, MSI, AppDomain) | [[Payloads/Payloads Avanzados]] |
| Droppers (C# + GadgetToJScript) | [[Técnicas/Droppers]] |

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
