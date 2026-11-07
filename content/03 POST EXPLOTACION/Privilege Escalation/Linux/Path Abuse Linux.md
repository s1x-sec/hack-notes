---
tags: [privesc, linux, path]
---

# Path Abuse — Linux

> [!note]
> La escalada por **PATH abuse** ocurre cuando un programa con altos privilegios (como `root`) intenta ejecutar un comando del sistema de forma insegura, permitiendo engañarlo para que ejecute un archivo malicioso en su lugar.

```bash
PATH=.:${PATH}
export PATH
```

Si hay un script SUID que llama a un binario sin ruta absoluta (ej. `ls` en vez de `/bin/ls`), se puede crear un `ls` malicioso en el directorio actual y añadirlo al PATH para que se ejecute como root.

