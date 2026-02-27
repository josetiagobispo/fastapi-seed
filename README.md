# API de Gerenciamento de Leads

API para gerenciamento de Leads com Python, FastAPI e MongoDB.

## Arquitetura

Projeto organizado em camadas com injeção de dependência (injector):

- `modules/lead/` — router, use cases, repository, schemas, errors
- `src/core/` — base de DI, exceções, decorators
- `src/database/` — ports e adapters para MongoDB
- `src/providers/` — cliente HTTP para chamadas externas

Cada camada tem responsabilidade única: o router só recebe a request e delega pro use case, que orquestra a lógica e chama o repository pra persistir.

## Como Rodar

```bash
cp example.env .env
make up
```

Outros comandos:

| Comando | Descrição |
|---------|-----------|
| `make up` | Sobe o projeto (build + containers) |
| `make down` | Para os containers |
| `make rebuild` | Derruba e sobe do zero |
| `make logs` | Acompanha logs da API |
| `make test` | Roda os testes |
| `make clean` | Remove containers e volumes |

API: `http://localhost:8000` — Docs: `http://localhost:8000/docs`

## Endpoints

As rotas usam versionamento (`/api/v1`) pra facilitar evolução futura sem quebrar clientes.

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/v1/leads` | Cria lead |
| GET | `/api/v1/leads` | Lista leads |
| GET | `/api/v1/leads/{id}` | Busca lead por ID |

### Exemplo de request (POST)

```bash
curl -X POST http://localhost:8000/api/v1/leads \
  -H "Content-Type: application/json" \
  -d '{"name": "João", "email": "joao@email.com", "phone": "11999998888"}'
```

### Validações

- **name**: apenas letras, mínimo 2 caracteres
- **email**: formato válido, único por lead (retorna `409` se já existir)
- **phone**: apenas dígitos (aceita formatação, ex: `+55 (11) 99999-8888`), entre 8 e 15 dígitos

## Integração Externa

Na criação do lead, o sistema consulta `https://dummyjson.com/users/1` e extrai o campo `birthDate`, salvando como `birth_date` no documento.

A busca é feita em **background** (`asyncio.create_task`) — o POST responde imediatamente com `birth_date = null` e o valor é atualizado no MongoDB assim que a API externa responder. O `HttpClient` faz até 3 retries com intervalo de 1s entre tentativas.

Se todas as tentativas falharem, o lead permanece com `birth_date = null`. Optei por não bloquear o cadastro por causa de um serviço de terceiro.

## Testes

```bash
pytest tests/ -v
```
