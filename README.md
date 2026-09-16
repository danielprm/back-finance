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

Com a aplicação rodando (`python app.py`), a forma mais rápida de testar é pelo **Swagger UI** em [http://127.0.0.1:5000](http://127.0.0.1:5000): expanda qualquer rota, clique em "Try it out", edite o corpo de exemplo e clique em "Execute".

Alternativamente, o fluxo completo pode ser testado via `curl`, **direto no terminal** (não cole estes comandos dentro dos campos do Swagger UI — lá o campo espera só o JSON do corpo, sem o `curl` e sem as aspas de shell):

```bash
# 1. Criar uma categoria
curl -X POST http://127.0.0.1:5000/categorias \
  -H "Content-Type: application/json" \
  -d '{"nome": "Moradia", "cor": "#4A90D9"}'

# 2. Listar categorias (confirme o id retornado acima)
curl http://127.0.0.1:5000/categorias

# 3. Cadastrar uma despesa fixa (use o categoria_id do passo 1)
curl -X POST http://127.0.0.1:5000/despesas-fixas \
  -H "Content-Type: application/json" \
  -d '{"descricao": "Aluguel", "valor": 1500, "dia_vencimento": 5, "categoria_id": 1, "ativo": true}'

# 4. Gerar os lançamentos do mês a partir das despesas fixas ativas
curl -X POST http://127.0.0.1:5000/transacoes/gerar-fixas

# 5. Gerar novamente: deve retornar {"geradas": 0}, provando que não duplica
curl -X POST http://127.0.0.1:5000/transacoes/gerar-fixas

# 6. Criar um lançamento manual (despesa ou receita avulsa)
curl -X POST http://127.0.0.1:5000/transacoes \
  -H "Content-Type: application/json" \
  -d '{"descricao": "Salário", "valor": 3000, "tipo": "receita", "data": "2026-09-05", "categoria_id": 1}'

# 7. Ver o resumo do mês (saldo, totais por categoria, fixo x eventual)
curl "http://127.0.0.1:5000/resumo?mes=9&ano=2026"
```

O banco (`gastos.db`) é recriado do zero apagando o arquivo e rodando `python app.py` novamente.
