---
tags: [privesc, windows, uac]
---

# UAC Bypass — Cobalt Strike

Cobalt Strike proporciona dos comandos para ejecutar código en contexto elevado: **elevate** y **runasadmin**.

## elevate

```bash
elevate [exploit] [listener]
```

## runasadmin

```bash
runasadmin [exploit] [command] [args]
```


---

## Teoría: MIC y UAC

En Windows, tener privilegios de Administrador no significa tener control total de forma inmediata. El sistema operativo divide el acceso en dos barreras de seguridad principales: **MIC** y **UAC**.

### 1. Mandatory Integrity Control (MIC)

Es el mecanismo subyacente que controla el acceso a objetos securizables (procesos, archivos, registros). La regla de oro del MIC es: **Ningún usuario/proceso puede modificar un objeto que tenga un nivel de integridad superior al suyo.**

Existen 4 niveles principales de integridad:

| Nivel | Descripción |
|-------|-------------|
| **Low (Bajo)** | Procesos muy restringidos (ej. navegadores en modo seguro) |
| **Medium (Medio)** | Nivel **por defecto** para todos los usuarios. Incluso si estás en el grupo de Administradores Locales, tus consolas (`cmd.exe`) nacerán en nivel Medio. Acciones críticas (como crear un usuario local) fallarán con *Access Denied* |
| **High (Alto)** | Contexto de Administrador elevado. Permite cambios profundos en el sistema |
| **System (Sistema)** | Nivel máximo, reservado para el núcleo del SO y servicios críticos (`NT AUTHORITY\SYSTEM`) |

### 2. User Account Control (UAC)

UAC actúa como el **guardián (gatekeeper)** del MIC. Es una característica de defensa en profundidad (*defence-in-depth*).

- **El Bloqueo:** Su propósito es evitar que el malware se ejecute en el contexto de un administrador y modifique el sistema de forma silenciosa.
- **La Elevación:** Para pasar de un nivel de integridad *Medium* a *High*, un usuario administrador debe solicitar explícitamente la elevación del proceso (ej. "Ejecutar como Administrador").
- **El Prompt:** UAC intercepta esta petición y lanza una ventana emergente en el escritorio del usuario solicitando consentimiento (click en "Sí") o pidiendo credenciales.

> [!tip] Nota Operativa (UAC Bypasses — T1548.002)
> Como operadores de Red Team, si obtenemos una sesión (Beacon) en el contexto de un usuario Administrador, nuestra terminal estará en nivel *Medium*. Dado que no podemos hacer click físicamente en la ventana de confirmación de UAC en el escritorio del usuario (eso nos delataría), debemos usar técnicas de **UAC Bypass**. Estas técnicas abusan de binarios legítimos de Windows que se auto-elevan silenciosamente o secuestran procesos de alta integridad para conseguir nuestro Beacon en nivel *High* sin lanzar la ventana emergente al usuario.
