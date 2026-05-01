# 🏦 API Bancária Assíncrona

API REST bancária construída com **FastAPI**, **SQLite** e **Python assíncrono**, com autenticação via **JWT**. Permite cadastro de clientes, criação de contas bancárias, depósitos, saques e extrato de transações.

---

## 🧱 Tecnologias utilizadas

| Tecnologia | Função |
|---|---|
| **FastAPI** | Framework web para construção da API |
| **aiosqlite** | Driver assíncrono para SQLite |
| **passlib + bcrypt** | Hash seguro de senhas |
| **python-jose** | Geração e validação de tokens JWT |
| **Pydantic v2** | Validação de dados de entrada e saída |
| **Poetry** | Gerenciamento de dependências e ambiente virtual |
| **Uvicorn** | Servidor ASGI para rodar a aplicação |

---

## 📁 Estrutura do projeto

```
Api_Bancaria_Assincrona/
│
├── app/
│   ├── main.py                  # Inicialização do FastAPI e lifespan
│   │
│   ├── api/
│   │   └── routes/
│   │       ├── clientes.py      # Rotas: cadastro e login
│   │       └── contas.py        # Rotas: conta, depósito, saque, extrato
│   │
│   ├── services/
│   │   ├── cliente_service.py   # Lógica de negócio do cliente
│   │   └── conta_service.py     # Lógica de negócio da conta (depósito, saque)
│   │
│   ├── repositories/
│   │   ├── clientes_repo.py     # Queries SQL de clientes
│   │   ├── conta_repo.py        # Queries SQL de contas
│   │   └── transacoes_repo.py   # Queries SQL de transações
│   │
│   ├── core/
│   │   └── auth.py              # JWT, hash de senha, verificação de token
│   │
│   └── db/
│       └── database.py          # Criação das tabelas no SQLite
│
├── pyproject.toml               # Dependências gerenciadas pelo Poetry
└── README.md
```

---

## ⚙️ Como rodar o projeto

### Pré-requisitos

- Python 3.11 ou superior
- [Poetry](https://python-poetry.org/docs/#installation) instalado

### Passo a passo

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/api-bancaria-assincrona.git
cd api-bancaria-assincrona
```

**2. Instale as dependências**
```bash
poetry install
```

**3. Suba o servidor**
```bash
poetry run uvicorn app.main:app --reload
```

**4. Acesse a documentação interativa**

Abra no navegador: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

O banco de dados SQLite (`clientes.db`) é criado automaticamente na primeira execução.

---

## 🔐 Como funciona a autenticação

A API usa **JWT (JSON Web Token)**. O fluxo é:

1. O cliente se **cadastra** com nome, email e senha
2. A senha é convertida em **hash bcrypt** — a senha original nunca é salva
3. O cliente faz **login** com email e senha
4. A API verifica o hash e, se correto, retorna um **token JWT** com validade de 60 minutos
5. Nas rotas protegidas, o token deve ser enviado no header: `Authorization: Bearer <token>`

---

## 📋 Endpoints

### Clientes

#### `POST /clientes` — Cadastrar cliente
Não requer autenticação.

**Body:**
```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "senha": "minhasenha123"
}
```

**Resposta (201):**
```json
{
  "msg": "Cliente criado com sucesso"
}
```

---

#### `POST /login` — Autenticar cliente
Não requer autenticação.

**Body:**
```json
{
  "email": "joao@email.com",
  "senha": "minhasenha123"
}
```

**Resposta (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "nome": "João Silva"
}
```

---

### Contas *(todas requerem token JWT)*

#### `POST /contas` — Criar conta bancária
Cria uma conta com saldo zero para o cliente autenticado.

**Resposta (201):**
```json
{
  "message": "Conta criada com sucesso"
}
```

---

#### `POST /contas/depositar` — Depositar
**Body:**
```json
{
  "valor": 500.00
}
```

**Resposta (200):**
```json
{
  "message": "Depósito realizado",
  "novo_saldo": 500.00
}
```

---

#### `POST /contas/sacar` — Sacar
**Body:**
```json
{
  "valor": 200.00
}
```

**Resposta (200):**
```json
{
  "message": "Saque realizado",
  "novo_saldo": 300.00
}
```

---

#### `GET /contas/extrato` — Ver extrato
Retorna todas as transações da conta do cliente autenticado.

**Resposta (200):**
```json
{
  "transacoes": [
    ["deposito", 500.00, "2025-01-15 14:32:00"],
    ["saque", 200.00, "2025-01-15 15:10:00"]
  ]
}
```

---

## 🗄️ Banco de dados

O projeto usa **SQLite** com três tabelas:

**`usuarios`** — armazena os clientes
| Coluna | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Chave primária |
| nome | TEXT | Nome do cliente |
| email | TEXT | Email único |
| senha | TEXT | Hash bcrypt da senha |

**`contas`** — uma conta por cliente
| Coluna | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Chave primária |
| cliente_id | INTEGER | Chave estrangeira → usuarios |
| saldo | REAL | Saldo atual (padrão: 0) |

**`transacoes`** — histórico de movimentações
| Coluna | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Chave primária |
| conta_id | INTEGER | Chave estrangeira → contas |
| tipo | TEXT | `deposito` ou `saque` |
| valor | REAL | Valor da operação |
| data | TIMESTAMP | Data/hora automática |

---

---

## ⚠️ Observações importantes

- O arquivo `clientes.db` é gerado automaticamente na raiz do projeto na primeira execução
- A `SECRET_KEY` usada para assinar os tokens JWT deve ser trocada por uma string longa e aleatória em produção, preferencialmente lida de uma variável de ambiente
- Tokens JWT expiram em **60 minutos** — após isso é necessário fazer login novamente
- Cada cliente pode ter **apenas uma conta bancária**

---

## 👨‍💻 Autor

Desenvolvido por **Guilherme** como projeto de aprendizado de APIs assíncronas com FastAPI e Python.
