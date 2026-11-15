---
tags: [privesc, windows, uac]
---

# MIC y UAC

En Windows, tener privilegios de Administrador no significa tener control total de forma inmediata. El sistema divide el acceso en dos barreras: **MIC** y **UAC**.

## Mandatory Integrity Control (MIC)

Controla el acceso a objetos securizables (procesos, archivos, registro). Regla: ningún proceso puede modificar un objeto con nivel de integridad superior al suyo.

| Nivel | Descripción |
|-------|-------------|
| Low | Procesos muy restringidos (navegadores en modo seguro) |
| Medium | Nivel por defecto para todos los usuarios, incluso Administradores locales. `cmd.exe` nace en Medium — acciones críticas fallan con *Access Denied* |
| High | Contexto de Administrador elevado |
| System | Nivel máximo, reservado para el núcleo del SO y servicios críticos (`NT AUTHORITY\SYSTEM`) |

## User Account Control (UAC)

Actúa como gatekeeper del salto Medium → High. Defensa en profundidad: evita que malware se ejecute como administrador y modifique el sistema en silencio.

- Para pasar de Medium a High, el usuario debe solicitar elevación explícita ("Ejecutar como Administrador")
- UAC intercepta la petición y pide consentimiento (click en "Sí") o credenciales

Un atacante con sesión en contexto Administrador pero integridad Medium no puede hacer click físicamente en el prompt sin delatarse. Para subir a High sin que salga el prompt hace falta **[[03-post-explotacion/privilege-escalation/windows/uac-bypass|UAC Bypass]]**.

## Ver también

- [[03-post-explotacion/privilege-escalation/windows/uac-bypass|UAC Bypass]]
- [[03-post-explotacion/privilege-escalation/windows/privilegios/privilegios-windows|Privilegios Windows]]
