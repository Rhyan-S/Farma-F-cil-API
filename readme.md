#  API Farma Fácil

Uma API RESTful completa desenvolvida em Python (Flask) para o gerenciamento de um catálogo de medicamentos e controle de estoque distribuído em múltiplas farmácias.

Este projeto demonstra a construção de um Backend robusto, utilizando banco de dados relacional (MariaDB) e as melhores práticas de operações CRUD (Create, Read, Update, Delete).

---

##  Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Framework Web:** Flask (Microframework)
* **ORM:** Flask-SQLAlchemy (Mapeamento Objeto-Relacional)
* **Banco de Dados:** MariaDB / MySQL (via XAMPP)
* **Drivers e Extensões:** PyMySQL, Flask-CORS, Cryptography
* **Testes de API:** Insomnia / Postman

---

##  Pré-requisitos

Antes de começar, você precisará ter as seguintes ferramentas instaladas na sua máquina:
* [Python 3.x](https://www.python.org/downloads/)
* [XAMPP](https://www.apachefriends.org/pt_br/index.html) (para rodar o servidor local do MariaDB/MySQL)

---

##  Como Rodar o Projeto na Sua Máquina

Siga o passo a passo abaixo para configurar o ambiente e rodar a API localmente.

### Passo 1: Configurar o Banco de Dados (XAMPP)

A aplicação precisa de um banco de dados local para armazenar as informações.

1. Abra o **Painel de Controle do XAMPP** e inicie os módulos **Apache** e **MySQL** clicando em *Start*.
2. Clique no botão **Admin** do MySQL ou acesse `http://localhost/phpmyadmin` no seu navegador.
3. No menu lateral esquerdo, clique em **Novo** para criar um banco de dados.
4. Digite o nome do banco de dados exatamente como: **`farmafacil`**.
5. Selecione a codificação `utf8mb4_general_ci` (recomendado) e clique em **Criar**.

> ⚠️ **Nota:** Você **não precisa** criar as tabelas `medicamentos` e `estoqueexterno` manualmente. A aplicação Flask (através do SQLAlchemy) fará a criação das tabelas e a inserção de dados de teste automaticamente ao ser iniciada pela primeira vez!

### Passo 2: Preparar o Ambiente Python

Abra a pasta do projeto no seu editor de código (como o VS Code) e abra o terminal integrado (`Ctrl + '`).

1. **Crie um ambiente virtual** (para isolar as bibliotecas do projeto):
   ```bash
   python -m venv .venv
   ```

2. **Ative o ambiente virtual:**
   * No Windows (PowerShell):
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   * No Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

3. **Instale as dependências** necessárias do projeto:
   ```bash
   pip install flask flask-sqlalchemy pymysql flask-cors cryptography
   ```

### Passo 3: Iniciar o Servidor

Com o ambiente virtual ativado `(.venv)` e o XAMPP rodando, inicie a API com o comando:

```bash
python app.py
```

Você deverá ver no terminal as mensagens indicando que as tabelas foram verificadas e que o servidor está rodando em `http://127.0.0.1:5000`.

---

##  Endpoints da API

Abaixo estão as rotas disponíveis na aplicação. Você pode configurá-las no **Insomnia** para testar as requisições.

**URL Base:** `http://localhost:5000`

###  Medicamentos

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| **GET** | `/api/medicamentos` | Lista todos os medicamentos cadastrados. |
| **GET** | `/api/medicamentos/<id>` | Retorna os detalhes de um medicamento específico. |
| **POST** | `/api/medicamentos` | Cadastra um novo medicamento (requer JSON com todos os dados). |
| **PUT** | `/api/medicamentos/<id>` | Atualiza dados específicos de um medicamento existente. |
| **DELETE** | `/api/medicamentos/<id>` | Exclui um medicamento (bloqueado se houver estoque vinculado). |

###  Estoque Externo

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| **GET** | `/api/estoque` | Lista todo o estoque registrado em todas as farmácias. |
| **POST** | `/api/estoque` | Adiciona estoque de um medicamento em uma farmácia (`medicamento_id`, `farmacia_externa`, `quantidade`). |
| **PUT** | `/api/estoque/<id>` | Atualiza a quantidade de um registro de estoque. |
| **DELETE** | `/api/estoque/<id>` | Remove um registro de estoque específico. |

###  Utilitários

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| **GET** | `/api/health` | Verifica a saúde da API e o status de conexão com o Banco de Dados. |

---

## 📂 Estrutura de Arquivos

```text
FarmaAPI/
├── __pycache__/       # Ficheiros de cache gerados pelo Python
├── .venv/             # Ambiente virtual isolado com as dependências
├── app.py             # Ficheiro principal que inicializa o servidor Flask
├── config.py          # Configurações da aplicação (ex: ligação à base de dados)
├── FarmaFacil.html    # Ficheiro front-end para interface de utilizador
├── models.py          # Modelos de dados (Classes de Medicamento e EstoqueExterno)
├── readme.md          # Documentação principal do projeto
├── requirements.txt   # Lista de dependências e bibliotecas Python
└── routes.py          # Definição das rotas (Endpoints do CRUD)
```

---

## 🧑 Autor
Criado por **Rhyan Soares**