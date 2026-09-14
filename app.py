from flask import Flask
from flask_cors import CORS

from config import Config
from extensions import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Libera CORS para toda origem: o front-end roda como arquivo local (file://),
# que o navegador trata como origem "null", então precisa ser aceito aqui.
CORS(app)

from models.categoria import Categoria
from models.despesa_fixa import DespesaFixa
from models.transacao import Transacao

from flask_restx import Api

api = Api(
    app,
    version="1.0",
    title="API Controle de Gastos",
    description="API para controle de gastos pessoais com despesas fixas recorrentes.",
    doc="/swagger",
)

from resources.categorias import ns as categorias_ns
from resources.despesas_fixas import ns as despesas_fixas_ns
from resources.transacoes import ns as transacoes_ns
from resources.resumo import ns as resumo_ns

api.add_namespace(categorias_ns, path="/categorias")
api.add_namespace(despesas_fixas_ns, path="/despesas-fixas")
api.add_namespace(transacoes_ns, path="/transacoes")
api.add_namespace(resumo_ns, path="/resumo")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
