---
tags: [ad, trusts, kerberos, inter-realm]
status: completo
---

# Inter-Realm Tickets (Referral Tickets)

> Mecanismo Kerberos para acceder a recursos en dominios de confianza. El KDC local emite un TGT especial cifrado con la inter-realm key compartida.

## Flujo de Autenticación

```
1. Cliente → KDC local: TGS-REQ para servicio en dominio externo
2. KDC local → Cliente: TGS-REP con inter-realm TGT
   - realm = trusted realm
   - sname = krbtgt/TRUSTING_DOMAIN
   - cifrado con la inter-realm key
3. Cliente → KDC externo: TGS-REQ con el inter-realm TGT
4. KDC externo valida el ticket usando la inter-realm key compartida
5. KDC externo → Cliente: Service Ticket para el recurso solicitado
```

## Campos Clave del Inter-Realm TGT

| Campo | Valor |
|-------|-------|
| realm | Dominio de confianza (trusted) |
| sname | krbtgt/TRUSTING_DOMAIN |
| cifrado | Inter-realm key compartida |

## Notas

- Los trusts usan RC4 por defecto para la inter-realm key
- Si se conoce la inter-realm key se puede forjar un referral ticket con Rubeus `silver`
- Para forjar hay que especificar grupos del dominio destino con `/ldap` o manualmente

## Ver también

- [[05-ad-attacks/trusts|Trusts]]
- [[05-ad-attacks/trusts/inbound-trusts|Inbound Trusts]]
- [[05-ad-attacks/trusts/outbound-trusts|Outbound Trusts]]
