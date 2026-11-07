---
tags: [lateral-movement, scshell, aggressor, custom]
status: done
platform: windows
---

# Custom Lateral Movement Techniques

> Extensiones del framework de CS mediante Aggressor Script.

---

## Extendiendo jump / remote-exec

Cobalt Strike permite registrar nuevas técnicas de movimiento lateral via Aggressor Script usando `beacon_remote_exploit_register`. Esto integra la técnica custom directamente en el comando `jump`.

---

## SCShell

Alternativa sigilosa a PsExec. En lugar de **crear** un nuevo servicio (Event ID 7045, muy monitorizado), **secuestra** un servicio existente legítimo temporalmente.

**Autor:** Charles Hamilton  
**Repositorio:** https://github.com/Mr-Un1k0d3r/SCShell/tree/master/CS-BOF

### Instalación en Cobalt Strike

```
Cobalt Strike → Script Manager → Load scshell.cna
```

### Uso

```
# Una vez cargado el .cna, se integra nativamente en jump
beacon> jump scshell64 <target> smb
```

### Ventaja vs PsExec

| | PsExec | SCShell |
|-|--------|---------|
| Event ID | 7045 (nuevo servicio) | ❌ No genera 7045 |
| Artefacto | Nuevo binario en ADMIN$ | Modifica servicio existente |
| Detección | Alta | Moderada |

---

## Aggressor Script — Skeleton

```coffeescript
# Registrar nueva técnica de lateral movement
beacon_remote_exploit_register("miTecnica", "x64", "Descripción de la técnica", {
    local('$bid $target $listener');
    $bid = $1;
    $target = $2;
    $listener = $3;
    
    # Lógica de la técnica aquí
    btask($bid, "Moviéndome a $target via miTecnica");
});
```

