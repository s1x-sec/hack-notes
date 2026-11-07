---
tags: [ports, snmp, udp]
status: done
---

# 161 UDP — SNMP

---

## Enumeración

```bash
sudo nmap -sU -p 161 <IP>
sudo nmap -sU -p 161 --script snmp-* <IP>
sudo nmap -sU --open -p 161 192.168.50.1-254 -oG open-snmp.txt
sudo nmap -Pn -n <IP> -sU --top-ports=100 --reason

# snmpwalk — recorrer árbol OID
snmpwalk -v2c -c public <IP>
snmpwalk -v1 -c public <IP> -Oa     # decodifica hex a ASCII
snmpbulkwalk -c public -v2c <IP> .  # más rápido

# Buscar credenciales
snmpwalk -v2c -c public <IP> | grep -iE "login|fail|user|pass|key"
```

---

## Fuerza Bruta de Community Strings

```bash
onesixtyone <IP> -c /usr/share/wordlists/seclists/Discovery/SNMP/snmp-onesixtyone.txt
sudo nmap -sU -p161 --script snmp-brute --script-args snmp-brute.communitiesdb='<wordlist>' <IP>
```

---

## OIDs Útiles

```
Sistema operativo:        1.3.6.1.2.1.1.1.0
Hostname:                 1.3.6.1.2.1.1.5.0
Contacto del sistema:     1.3.6.1.2.1.1.4.0
Procesos en ejecución:    1.3.6.1.2.1.25.4.2.1.2
Parámetros de procesos:   1.3.6.1.2.1.25.4.2.1.5
Software instalado:       1.3.6.1.2.1.25.6.3.1.2
Cuentas de usuario:       1.3.6.1.4.1.77.1.2.25
Puertos TCP en escucha:   1.3.6.1.2.1.6.13.1.3
Puertos UDP en escucha:   1.3.6.1.2.1.7.5.1.2
IPs:                      1.3.6.1.2.1.4.20
netSnmpExtendMIB (RCE):   1.3.6.1.4.1.8072.1.3.2
```

---

## Verificar Escritura + RCE

```bash
# Comprobar si tiene permisos de escritura
snmpget -Oqv -r 0 -v1 -c <community> <IP> 1.3.6.1.2.1.1.4.0
snmpset -r 0 -v1 -c <community> <IP> 1.3.6.1.2.1.1.4.0 str "test"

# RCE via NET-SNMP-EXTEND-MIB
snmpwalk -v2c -c <community> <IP> 1.3.6.1.4.1.8072.1.3.2
snmpbulkwalk -c <community> -v2c <IP> NET-SNMP-EXTEND-MIB::nsExtendObjects
```

