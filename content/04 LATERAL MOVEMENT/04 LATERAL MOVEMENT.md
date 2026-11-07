---
tags: [lateral-movement]
status: done
---

# LATERAL MOVEMENT

---

## User Impersonation

| Técnica | Nota |
|---------|------|
| Índice User Impersonation | [[User Impersonation/User Impersonation]] |
| Pass the Hash | [[User Impersonation/Pass the Hash]] |
| Pass The Ticket | [[User Impersonation/Pass The Ticket]] |
| Token Impersonation | [[User Impersonation/Token Impersonation]] |

---

## Técnicas de Movimiento Lateral

| Técnica | Nota |
|---------|------|
| Jump / Remote-Exec (WinRM, WMI, PsExec) | [[Tecnicas/Jump y Remote-Exec]] |
| PsExec | [[Tecnicas/PsExec]] |
| Windows Remote Management | [[Tecnicas/Windows Remote Management]] |
| LOLBAS (MavInject) | [[Tecnicas/LOLBAS]] |
| Custom Techniques (SCShell) | [[Tecnicas/Custom Techniques]] |
| Security Logon Types / Double Hop | [[Tecnicas/Security Logon Types]] |

---

## Pivoting & Tunneling

| Técnica | Nota |
|---------|------|
| Pivoting (general) | [[Tecnicas/Pivoting]] |
| Pivoting con Cobalt Strike (SOCKS) | [[Tecnicas/Pivoting con Cobalt]] |
| Reverse Port Forward Cobalt Strike (SOCKS) | [[Reverse Port Forward Cobalt Strike]] |
| Ligolo-ng | [[Tecnicas/Ligolo-ng]] |
| Port Forwarding SSH | [[Tecnicas/Port Forwarding - SSH]] |

---

## Credential Access (Lateral)

| Técnica | Nota |
|---------|------|
| Credentials from Web Browsers | [[Credential Access/Credentials from Web Browsers]] |
| Windows Credential Manager | [[Credential Access/Windows Credential Manager]] |

---

## Flujo Decisional

```
¿Qué tienes?
│
├── Hash NTLM        → [[User Impersonation/Pass the Hash]]
├── Ticket Kerberos  → [[User Impersonation/Pass The Ticket]]
├── Usuario + pass   → make_token + jump
└── Token de proceso → [[User Impersonation/Token Impersonation]] → steal_token <PID>
```

> [!warning] Double Hop
> WinRM y PsExec usan **Logon Type 3 (Network)** — las credenciales **no** se delegan al destino.
> → [[Tecnicas/Security Logon Types]] para el análisis completo.
