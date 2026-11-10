---
tags: [cloud, azure, avd, vdi, rdp]
status: wip
---

# Azure Virtual Desktop (AVD)

> Servicio VDI de Azure (antes Windows Virtual Desktop). Despliega escritorios y aplicaciones remotas sobre session hosts Windows en Azure, autenticados contra Entra ID / AD DS.

---

## Arquitectura

```
Usuario → AVD Web/App Client → AVD Gateway (Azure) → RDP Shortpath/Reverse Connect → Session Host (VM)
                                                                                          ↓
                                                                              Azure VNET / AD DS / Entra ID
```

| Componente | Descripción |
|-----------|-------------|
| **Host Pool** | Colección de session hosts (VMs) que sirven escritorios/apps |
| **Session Host** | VM Windows con el rol RDSH. Puede ser single-session (W10/11) o multi-session |
| **Application Group** | Define qué se publica: escritorio completo (Desktop) o apps individuales (RemoteApp) |
| **Workspace** | Agrupa application groups visibles para el usuario |
| **FSLogix** | Contenedores de perfil (VHD/VHDX) montados al inicio de sesión — almacenados en Azure Files o Storage Account |
| **RDP Shortpath** | Conexión UDP directa (si disponible) en lugar del relay por el Gateway |

---

## Superficie de ataque

| Vector | Objetivo |
|--------|----------|
| Credenciales / Entra ID | Acceso inicial al tenant — phishing, password spray, token theft |
| Conditional Access bypass | Evadir políticas de CA que protegen el acceso AVD |
| Session Host compromise | Privesc local + credential harvesting en la VM |
| FSLogix profiles | Persistencia y robo de datos en los contenedores VHD |
| IMDS / Managed Identity | Pivotar desde la VM a recursos Azure via tokens |
| Network pivoting | Lateral movement desde la VNET del host pool |
| AVD breakout | Escapar entornos restringidos (RemoteApp, kiosk) |

---

## Índice

| Nota | Descripción | Estado |
|------|-------------|--------|
| [[09-cloud/azure/avd---enumeración\|AVD - Enumeración]] | Reconocimiento de infraestructura AVD | 🟡 WIP |
| [[09-cloud/azure/avd---acceso-inicial\|AVD - Acceso Inicial]] | Password spray, token theft, Conditional Access bypass | 🟡 WIP |
| [[09-cloud/azure/avd---session-host-attacks\|AVD - Session Host Attacks]] | Privesc, credential harvesting, LSASS en session hosts | 🟡 WIP |
| [[09-cloud/azure/avd---breakout\|AVD - Breakout]] | Escape de RemoteApp, kiosk, AppLocker | 🟡 WIP |
| [[09-cloud/azure/avd---lateral-movement\|AVD - Lateral Movement]] | Pivoting desde session hosts a Azure y red interna | 🟡 WIP |
| [[09-cloud/azure/avd---persistencia\|AVD - Persistencia]] | FSLogix abuse, startup scripts, scheduled tasks | 🟡 WIP |

---

## Herramientas

| Herramienta | Uso |
|-------------|-----|
| `az cli` | Enumeración y gestión Azure |
| `Az` (PowerShell) | Módulo Azure PowerShell — más completo para AVD |
| `ROADtools` | Enumeración Entra ID (ex Azure AD) |
| `AADInternals` | Ataques contra Entra ID — token manipulation, PRT |
| `Impacket` | Ataques RDP, credential dumping |
| `Mimikatz` / `pypykatz` | LSASS dump, PRT extraction, certificate theft |
| `BloodHound CE` | Grafos de ataque AD + Azure |
| `GraphRunner` | Enumeración Microsoft Graph post-auth |
| `TokenTactics` | Refresh token manipulation para Azure/M365 |
| `Intune-PowerShell-SDK` | Reconocimiento de políticas Intune aplicadas |

---

## Recursos de aprendizaje

### Cursos / Labs

- [Azure Red Team Specialist (AzRTS) — CyberWarfare Labs](https://cyberwarfare.live/product/azure-red-team-specialist-azrts/) — lab práctico de red team en Azure incluyendo AVD
- [Hacking Azure: Recon to Domination — Claranet (BH/nullcon)](https://www.claranet.com/us/node/4329) — training ofensivo de Azure end-to-end
- [Cloud Red Team Tactics — nullcon 2026](https://nullcon.net/goa-2026/training/cloud-red-team-tactics-goa26) — tácticas red team cloud incluyendo Azure
- [PentesterAcademy — Azure Pentesting Labs](https://www.pentesteracademy.com/) — labs on-demand de Azure AD y cloud attacks
- [HackTheBox — Azure Machines](https://www.hackthebox.com/) — máquinas con entorno Azure/AD

### Blogs / Investigación

- [dirkjanm.io](https://dirkjanm.io/) — Dirk-jan Mollema: ROADtools, PRT abuse, Azure AD internals
- [SpecterOps Blog](https://posts.specterops.io/) — BloodHound, Azure attack paths, Certified Pre-Owned
- [AADInternals](https://aadinternals.com/) — Dr. Nestori Syynimaa: herramientas y research Entra ID
- [NetSPI Cloud Pentesting Blog](https://www.netspi.com/blog/technical/cloud-penetration-testing/) — técnicas ofensivas Azure
- [Karl Fosaaen (NetSPI) — Azure Pentesting Tools](https://github.com/NetSPI/MicroBurst)
- [Andy Robbins — Azure Privilege Escalation via Attack Paths](https://posts.specterops.io/)

### Documentación / Referencia

- [HackTricks — Azure Security](https://book.hacktricks.xyz/pentesting-cloud/azure-security) — metodología y técnicas compiladas
- [PayloadsAllTheThings — Azure](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Methodology%20and%20Resources) — cheatsheets y payloads
- [Microsoft — Azure Virtual Desktop Architecture](https://learn.microsoft.com/en-us/azure/virtual-desktop/service-architecture-resilience)
- [Microsoft — AVD Security Best Practices](https://learn.microsoft.com/en-us/azure/virtual-desktop/security-guide) — para entender qué debería estar protegido

---

## Referencias

- [HackTricks Azure AD](https://book.hacktricks.xyz/pentesting-cloud/azure-security)
- [Azure Virtual Desktop Security Best Practices — Microsoft](https://learn.microsoft.com/en-us/azure/virtual-desktop/security-guide)
- [Attacking Azure Virtual Desktop — SpecterOps](https://posts.specterops.io/)
- [AADInternals — Dr. Nestori Syynimaa](https://aadinternals.com/)
- [WAM Token Abuse — Dirk-jan Mollema](https://dirkjanm.io/)
