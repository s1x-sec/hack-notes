---
tags: [lateral-movement]
status: done
---

# LATERAL MOVEMENT

---

## User Impersonation

| Técnica | Nota |
|---------|------|
| Índice User Impersonation | [[04-lateral-movement/user-impersonation\|User Impersonation]] |
| Pass the Hash | [[04-lateral-movement/user-impersonation/pass-the-hash\|Pass the Hash]] |
| Pass The Ticket | [[04-lateral-movement/user-impersonation/pass-the-ticket\|Pass The Ticket]] |
| Token Impersonation | [[04-lateral-movement/user-impersonation/token-impersonation\|Token Impersonation]] |

---

## Técnicas de Movimiento Lateral

| Técnica | Nota |
|---------|------|
| Jump / Remote-Exec (WinRM, WMI, PsExec) | [[04-lateral-movement/tecnicas/jump-y-remote-exec\|Jump y Remote-Exec]] |
| PsExec | [[04-lateral-movement/tecnicas/psexec\|PsExec]] |
| Windows Remote Management | [[04-lateral-movement/tecnicas/windows-remote-management\|Windows Remote Management]] |
| LOLBAS (MavInject) | [[04-lateral-movement/tecnicas/lolbas\|LOLBAS]] |
| Custom Techniques (SCShell) | [[04-lateral-movement/tecnicas/custom-techniques\|Custom Techniques]] |
| Security Logon Types / Double Hop | [[04-lateral-movement/tecnicas/security-logon-types\|Security Logon Types]] |

---

## Pivoting & Tunneling

| Técnica | Nota |
|---------|------|
| Pivoting (general) | [[04-lateral-movement/tecnicas/pivoting\|Pivoting]] |
| Pivoting con Cobalt Strike (SOCKS) | [[04-lateral-movement/tecnicas/pivoting-con-cobalt\|Pivoting con Cobalt]] |
| Reverse Port Forward Cobalt Strike (SOCKS) | [[04-lateral-movement/tecnicas/reverse-port-forward-cobalt-strike\|Reverse Port Forward Cobalt Strike]] |
| Ligolo-ng | [[04-lateral-movement/tecnicas/ligolo-ng\|Ligolo-ng]] |
| Port Forwarding SSH | [[04-lateral-movement/tecnicas/port-forwarding---ssh\|Port Forwarding - SSH]] |

---

## Credential Access (Lateral)

| Técnica | Nota |
|---------|------|
| Credentials from Web Browsers | [[04-lateral-movement/credential-access/credentials-from-web-browsers\|Credentials from Web Browsers]] |
| Windows Credential Manager | [[04-lateral-movement/credential-access/windows-credential-manager\|Windows Credential Manager]] |

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
> → [[04-lateral-movement/tecnicas/security-logon-types|Security Logon Types]] para el análisis completo.
