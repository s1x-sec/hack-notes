---
tags: [privesc, linux, shell]
---

# Shell Restrictiva

Las shells restrictivas más comunes: **RBASH**, **RKSH**, **RZSH**.

## Escapes

**Command Injection:**
```bash
ls -l `pwd`   # ejecuta pwd dentro de ls
```

**Command Substitution:**
```bash
ls `comando_no_permitido`
```

**Command Chaining:**
```bash
comando_permitido ; comando_no_permitido
comando_permitido | comando_no_permitido
```

**Variables de entorno:** modificar PATH, HOME u otras variables que usa la shell para ejecutar comandos.

**Funciones de shell:** si permite definir funciones, crear una que ejecute el comando restringido y llamarla.

