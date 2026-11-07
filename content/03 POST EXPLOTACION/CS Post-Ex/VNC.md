---
title: Cobalt Strike — VNC (Desktop Remoto)
tags: [cobalt-strike, post-ex, vnc, desktop]
---

# VNC — Desktop Remoto

## Abrir VNC viewer

```
beacon> desktop
```

O desde el menú: **Explore → Desktop (VNC)**

## Características

- Muestra el escritorio del usuario objetivo en tiempo real
- Permite interacción (clic, teclado)
- Corre como post-ex job inyectado

> [!warning] VNC genera bastante tráfico de red. Usar solo cuando sea necesario y cerrar el job una vez terminado.

```
beacon> jobs          # Ver que el desktop job está activo
beacon> jobskill <id> # Cerrar cuando termines
```
