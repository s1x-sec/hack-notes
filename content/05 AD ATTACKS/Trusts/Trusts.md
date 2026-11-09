---
tags: [ad, trusts, forest, domain]
status: pendiente
---

# Forest & Domain Trusts

---
# Forest & Domain Trusts 

> Los trusts permiten que usuarios de un dominio/forest accedan a recursos de otro. La frontera de seguridad real en AD es el **forest**, no el dominio — un DA en un dominio hijo puede escalar a Enterprise Admin del forest raíz.

## Tipos de Trust (detalle)

| Tipo | Descripción | Transitividad | Dirección |
|------|-------------|---------------|-----------|
| **Parent-Child** | Automático al crear subdominio | Transitivo | Bidireccional |
| **Tree-Root** | Automático al agregar árbol al forest | Transitivo | Bidireccional |
| **External** | Dominio externo (otro forest) | No transitivo | 1-way o 2-way |
| **Forest Trust** | Entre root domains de forests distintos | Transitivo (dentro del forest) | 1-way o 2-way |

## Trusted Domain Objects (TDO)

Los trusts se representan como objetos `trustedDomain` en AD.

```
beacon> ldapsearch (objectClass=trustedDomain) --attributes cn,flatName,trustDirection,trustAttributes,securityIdentifier
```

### trustDirection

| Valor | Significado |
|-------|-------------|
| 0 | Disabled |
| 1 | Inbound (el dominio local confía en el externo) |
| 2 | Outbound (el dominio externo confía en el local) |
| 3 | Bidireccional |

### trustAttributes (flags)

| Bit | Nombre | Descripción |
|-----|--------|-------------|
| 1 | NON_TRANSITIVE | No transitivo |
| 4 | QUARANTINED_DOMAIN | SID filtering activo |
| 8 | FOREST_TRANSITIVE | Forest trust |
| 32 | WITHIN_FOREST | Mismo forest |
| 64 | TREAT_AS_EXTERNAL | SID filtering implícito |

## Frontera de Seguridad

> **IMPORTANTE**: La frontera de seguridad en AD es el **forest**, NO el dominio.

- Los trusts dentro del mismo forest comparten la misma inter-realm key
- Los trusts entre forests distintos tienen keys únicas por trust

## Ver también

- [[05-ad-attacks/trusts/inter-realm-tickets|Inter-Realm Tickets]] — mecanismo Kerberos que hace posible el acceso cross-domain
- [[05-ad-attacks/trusts/parent-child-trusts|Parent-Child Trusts]] — escalada a Enterprise Admin via SID History
- [[05-ad-attacks/trusts/inbound-trusts|Inbound Trusts]] — movimiento lateral cuando el dominio local confía en el externo
- [[05-ad-attacks/trusts/outbound-trusts|Outbound Trusts]] — movimiento lateral cuando el externo confía en el local

## Referencias

- [HackTricks Forest Trusts](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/domain-trust-abuse)
