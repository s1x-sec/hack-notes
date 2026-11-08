---
tags: [ad, kerberos, delegation]
status: pendiente
---

# Unconstrained Delegation

---
## Concepto

Cuando un equipo o cuenta tiene Unconstrained Delegation, cualquier usuario que se autentique a un servicio en ese host deposita su TGT en la memoria de LSASS del servidor delegado. El atacante con acceso a ese host puede extraer esos TGTs y usarlos para impersonar a los usuarios.

Permite a un principal solicitar acceso a recursos en nombre de otro principal.

Es la delegación más peligrosa y se activa seteando una flag **TRUSTED_FOR_DELEGATION** en el UAC del objeto computer.

Si un atacante obtiene acceso a un ordenador con esta flag activada puede extraer todos los TGTs de memoria y usarlos para pedir tickets de servicios e ir pivotando por el dominio.

--- 
## Escenario

Un usuario se autentica en una web usando Kerberos y esa web se conecta a suvez con otro servicio back-end. Cuando el usuario realiza alguna acción que necesita ser procesada en el backend, la web necesita alguna forma de autenticarse contra el back-end. Como la web no conoce el **secret** del usuario no puede solicitar un ticket de servicio al KDC, por eso se ha creado la delegación.

---

```c
# Se pueden buscar la cuentas con esta flag TRUSTED_FOR_DELEGATION activada
beacon> ldapsearch (&(samAccountType=805306369)(userAccountControl:1.2.840.113556.1.4.803:=524288)) --attributes samaccountname
```

Con rubeus podemos estar constantemente monitorizando para capturar y mostrar los TGTs de los usuarios que se autentiquen contra un servicio.

```c
beacon> execute-assembly C:\Tools\Rubeus\Rubeus\bin\Release\Rubeus.exe monitor /nowrap
```



## Referencias

- [HackTricks — Unconstrained Delegation](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/unconstrained-delegation)

