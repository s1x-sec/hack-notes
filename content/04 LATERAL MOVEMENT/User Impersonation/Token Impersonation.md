---
tags: [lateral-movement, token, impersonation, cobalt-strike]
status: done
platform: windows
---

# Token Impersonation

> Robar o crear tokens de Windows para actuar como otro usuario sin conocer su contraseña.

---

## make_token

Crea un token de red para un usuario usando sus credenciales. **No verifica** la contraseña localmente — la verificación ocurre en el servidor remoto al autenticarse.

```
beacon> make_token DOMAIN\usuario contraseña
```

**Cuándo usar:** Tienes credenciales en texto plano y quieres autenticarte en red sin levantar alertas de logon interactivo.
**Quid:** El proceso beacon sigue siendo el mismo, solo cambia el token para operaciones de red.

---

## steal_token

Roba el token de acceso de un proceso existente. Requiere que ese proceso tenga un token con las credenciales que necesitamos (el usuario está logueado localmente).

```
beacon> steal_token <PID>
```

**Cadena de APIs internas:**
1. `OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, PID)` → handle al proceso
2. `OpenProcessToken(handle, TOKEN_DUPLICATE)` → handle al token
3. `DuplicateTokenEx(token, SecurityImpersonation)` → duplicar token
4. `ImpersonateLoggedOnUser(duplicated_token)` → asumir la identidad

```
# Revertir impersonación
beacon> rev2self
```

---

## token-store

Almacena tokens para reutilización posterior sin necesidad de mantener el proceso fuente activo.

```
beacon> token-store steal <PID>     # Guardar token del PID
beacon> token-store use <ID>        # Usar token guardado
beacon> token-store show            # Ver tokens almacenados
beacon> token-store remove <ID>     # Eliminar token
```

**Caso de uso:** Comprometer una sesión de un usuario con privilegios, guardar su token, y luego usar ese token en cualquier momento aunque el proceso original haya muerto.

---

## OPSEC

> Steal_token genera: `OpenProcess` + `OpenProcessToken` + `DuplicateTokenEx` — visible para EDRs que monitoricen acceso a procesos privilegiados.
> make_token es más limpio: solo crea un nuevo token localmente, sin acceder a otros procesos.

