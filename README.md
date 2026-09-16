# API — Controle de Gastos Pessoais

API REST para controle de gastos pessoais com suporte a despesas fixas recorrentes (aluguel, streaming, etc). Construída com Flask, Flask-SQLAlchemy e Flask-RESTX, como parte do MVP da disciplina de Desenvolvimento Full Stack Básico.

## Funcionalidades

- Cadastro de categorias de gastos.
- Cadastro de despesas fixas recorrentes, com geração automática dos lançamentos do mês.
- Lançamentos manuais de despesas e receitas.
- Resumo mensal com saldo, totais por categoria e comparação entre gastos fixos e eventuais.

## Tecnologias

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-RESTX (Swagger/OpenAPI)
- Flask-Cors
- SQLite

## Instalação e execução

1. Clone o repositório e entre na pasta:

   ```bash
   git clone <url-deste-repositorio>
   cd back-finance
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Rode a aplicação:

   ```bash
   python app.py
   ```

5. Acesse a documentação interativa (Swagger UI) em [http://127.0.0.1:5000](http://127.0.0.1:5000).

O banco SQLite (`gastos.db`) é criado automaticamente na primeira execução.

## Rotas principais

| Recurso | Rota | Métodos |
|---|---|---|
| Categorias | `/categorias` | GET, POST |
| Categorias | `/categorias/<id>` | GET, DELETE |
| Despesas Fixas | `/despesas-fixas` | GET, POST |
| Despesas Fixas | `/despesas-fixas/<id>` | PUT, DELETE |
| Transações | `/transacoes` | GET, POST |
| Transações | `/transacoes/<id>` | GET, DELETE |
| Transações | `/transacoes/gerar-fixas` | POST |
| Resumo | `/resumo` | GET |

Detalhes completos de cada rota (parâmetros, corpo de requisição, respostas) estão documentados no Swagger UI.
