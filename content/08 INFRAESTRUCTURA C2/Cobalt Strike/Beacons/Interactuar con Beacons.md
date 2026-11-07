---
title: Cobalt Strike — Interactuar con Beacons
tags: [cobalt-strike, beacons, metadata, event-log, dns]
---

# Interactuar con Beacons

## Event Log

Ver todas las conexiones de beacons:

```
View → Event Log
```

## Indicadores visuales

| Icono | Significado |
|-------|-------------|
| 🔵 Monitor azul | Beacon con bajos privilegios (user) |
| 🔴 Monitor rojo | Beacon con privilegios elevados (admin/SYSTEM) |

## Metadata del Beacon

Cuando un Beacon hace check-in envía:
- Beacon ID único
- IP interna + IP externa
- Usuario (`DOMAIN\user`)
- Hostname
- Sistema operativo
- **AES session key** (cifrada con la RSA public key del C2)

> [!important] El canal de comunicación es:
> - **HTTP/S**: Beacon envía metadata con el primer check-in
> - **DNS**: El Beacon NO envía metadata por defecto — usar `checkin` para forzarlo

## Beacon DNS — forzar check-in

```
beacon> checkin
```

Fuerza el envío de metadata cuando se usa el canal DNS.

## Interactuar con un Beacon

1. Doble clic en el beacon en la tabla de sesiones
2. O clic derecho → Interact

## Gestión de múltiples beacons

```
View → Beacons     # Ver todos los beacons activos
View → Targets     # Ver hosts comprometidos
```

## Ver también
- [[08-infraestructura-c2/cobalt-strike/beacons/generar-payloads|Generar Payloads]]
- [[08-infraestructura-c2/cobalt-strike/beacon-cheatsheet/house-keeping-commands|House-Keeping Commands]]
