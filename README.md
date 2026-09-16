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

## Como testar

Com a aplicação rodando (`python app.py`), acesse o **Swagger UI** em [http://127.0.0.1:5000](http://127.0.0.1:5000). Para cada rota abaixo: expanda o bloco, clique em **"Try it out"**, cole apenas o JSON indicado no campo "payload" (sem `curl`, sem aspas de shell) e clique em **"Execute"**.

Sequência sugerida para testar o fluxo completo:

1. **`POST /categorias`** — cria uma categoria:
   ```json
   {"nome": "Moradia", "cor": "#4A90D9"}
   ```

2. **`GET /categorias`** — não precisa de payload, só "Execute". Confirme o `id` retornado (normalmente `1`).

3. **`POST /despesas-fixas`** — cadastra uma despesa fixa (use o `categoria_id` do passo 1):
   ```json
   {"descricao": "Aluguel", "valor": 1500, "dia_vencimento": 5, "categoria_id": 1, "ativo": true}
   ```

4. **`POST /transacoes/gerar-fixas`** — sem payload, só "Execute". Gera os lançamentos do mês a partir das despesas fixas ativas.

5. **`POST /transacoes/gerar-fixas`** de novo — deve retornar `{"geradas": 0}`, provando que não duplica lançamentos já gerados.

6. **`POST /transacoes`** — cria um lançamento manual (despesa ou receita avulsa):
   ```json
   {"descricao": "Salário", "valor": 3000, "tipo": "receita", "data": "2026-09-05", "categoria_id": 1}
   ```

7. **`GET /resumo`** — preencha os parâmetros `mes` e `ano` (ex: `9` e `2026`) e clique "Execute". Mostra saldo, totais por categoria e comparação fixo x eventual.

O banco (`gastos.db`) é recriado do zero apagando o arquivo e rodando `python app.py` novamente.
