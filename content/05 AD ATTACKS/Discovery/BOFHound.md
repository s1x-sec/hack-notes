---
tags: [ad, discovery, bloodhound, bofhound, ldap, opsec]
status: done
platform: windows
---

# BOFHound — Enumeración AD OPSEC

> Alternativa sigilosa a SharpHound. Construir el grafo de BloodHound via ldapsearch (BOF) + BOFHound (parser Python).

---

## Por qué NO usar SharpHound directamente

SharpHound ejecuta cientos de consultas LDAP + SMB en ráfaga → muy detectable por:
- Correlación de volumen de consultas LDAP en tiempo corto
- NetSession enum por SMB (Event ID 4624 masivo)
- Proceso `SharpHound.exe` conocido por firmas AV/EDR

---

## BOFHound — Metodología

BOFHound **no es un BOF**. Es un script Python que parsea el output de ldapsearch (el BOF integrado de CS) para convertirlo en formato ingestible por BloodHound.

### 1. Enumeración Progresiva (días/semanas)

```
# Objetos básicos del dominio
beacon> ldapsearch (|(objectClass=domain)(objectClass=organizationalUnit)(objectClass=groupPolicyContainer)) --attributes *,ntsecuritydescriptor

# Usuarios, equipos, grupos
beacon> ldapsearch (|(samAccountType=805306368)(samAccountType=805306369)(samAccountType=268435456)) --attributes *,ntsecuritydescriptor
```

**Clave:** Distribuir las queries en el tiempo, no en ráfaga.

### 2. Extraer logs del Team Server

```bash
# Desde tu máquina atacante
scp -r attacker@<TEAMSERVER>:/opt/cobaltstrike/logs .
```

### 3. Parsear con BOFHound

```bash
bofhound -i logs/
# Genera archivos JSON en el directorio actual
```

### 4. Ingestar en BloodHound

```
BloodHound UI → Administration → File Ingest → Subir los JSON
```

---

## Restricted Groups — Bordes Perdidos

BloodHound no captura automáticamente qué grupos de dominio son Admins Locales vía GPO. Hay que extraerlo manualmente de SYSVOL.

### Proceso

```
1. Identificar GPO objetivo → atributo gPCFileSysPath
2. Leer el archivo:
   \\dominio\SysVol\dominio\Policies\{GUID-GPO}\Machine\Microsoft\Windows NT\SecEdit\GptTmpl.inf

3. Sección [Group Membership]:
   *S-1-5-21-...-1107__Memberof = *S-1-5-32-544
   # SID-1107 = grupo de dominio
   # S-1-5-32-544 = Built-in Administrators
```

### Añadir borde manualmente a Neo4j

```cypher
MATCH (x:Computer{objectid:'S-1-5-21-[...]-1110'}) 
MATCH (y:Group{objectid:'S-1-5-21-[...]-1107'}) 
MERGE (y)-[:AdminTo]->(x)
```

---

## Filtros WMI en GPOs — Falsos Positivos

BloodHound no evalúa filtros WMI → puede mostrar bordes que no existen realmente.

```bash
# Verificar filtro WMI de una GPO
beacon> ldapsearch (objectClass=groupPolicyContainer) --attributes displayname,gPCWQLFilter
beacon> ldapsearch (objectClass=msWMI-Som) --attributes name,msWMI-Name,msWMI-Parm2

# El atributo msWMI-Parm2 contiene la query WQL real:
# "SELECT * from Win32_OperatingSystem WHERE Version like '10.%'"
# → GPO solo aplica a Win10/11
```

Verificar **manualmente** antes de confiar en un borde de BloodHound.

