---
title: Cobalt Strike — Capturas de Pantalla
tags: [cobalt-strike, post-ex, screenshot]
---

# Capturas de Pantalla

## Métodos disponibles

| Comando | Método | Ventaja |
|---------|--------|---------|
| `printscreen` | BitBlt via clipboard | Rápido, no requiere job |
| `screenshot` | Post-ex DLL inyectada | No toca el portapapeles |
| `screenwatch` | Capturas automáticas | Monitorización continua |

## Uso

```
beacon> printscreen
beacon> screenshot
beacon> screenwatch
```

## Ver capturas

**View → Screenshots**

> [!tip] `screenshot` y `screenwatch` son mejores para OPSEC ya que no interfieren con el portapapeles del usuario.

> [!warning] `screenwatch` genera múltiples capturas según el `sleep` interval — puede generar mucho tráfico.
