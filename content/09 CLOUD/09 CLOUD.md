---
tags: [cloud]
---

# CLOUD HACKING

> Ataques específicos contra entornos cloud.

---

## Índice

| Plataforma | Nota |
|------------|------|
| AWS | [[09-cloud/aws\|AWS]] |
| Azure | [[09-cloud/azure\|Azure]] |
| GCP | - |

---

## Herramientas

- **AWS:** `aws cli`, `pacu` (framework ofensivo AWS), `cloudmapper`, `prowler`
- **Azure:** `az cli`, `roadtools`, `AADInternals`, `GraphRunner`, `bloodhound-ce` (Azure integración)
- **GCP:** `gcloud`, `gcp_scanner`

---

## Por empezar

- SSRF → IMDSv1 (AWS metadata en 169.254.169.254)
- IAM privilege escalation
- S3 bucket misconfiguration
- ~~Azure AD attacks~~ → ver [[09-cloud/azure|Azure]]

