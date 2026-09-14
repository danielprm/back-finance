from flask import request
from flask_restx import Namespace, Resource, abort, fields

from extensions import db
from models.categoria import Categoria
from models.despesa_fixa import DespesaFixa

ns = Namespace("despesas-fixas", description="Cadastro de despesas fixas recorrentes")

despesa_fixa_model = ns.model("DespesaFixa", {
    "id": fields.Integer(readonly=True),
    "descricao": fields.String(required=True),
    "valor": fields.Float(required=True, min=0),
    "dia_vencimento": fields.Integer(required=True, min=1, max=31, description="Dia do mês (1-31) em que a despesa vence"),
    "categoria_id": fields.Integer(required=True),
    "ativo": fields.Boolean(default=True),
})


@ns.route("")
class DespesaFixaListResource(Resource):
    @ns.marshal_list_with(despesa_fixa_model)
    def get(self):
        """Lista todas as despesas fixas cadastradas."""
        return DespesaFixa.query.all()

    @ns.expect(despesa_fixa_model, validate=True)
    @ns.marshal_with(despesa_fixa_model, code=201)
    def post(self):
        """Cadastra uma nova despesa fixa."""
        dados = request.get_json()
        if Categoria.query.get(dados["categoria_id"]) is None:
            abort(400, "Categoria informada não existe")
        despesa = DespesaFixa(
            descricao=dados["descricao"],
            valor=dados["valor"],
            dia_vencimento=dados["dia_vencimento"],
            categoria_id=dados["categoria_id"],
            ativo=dados.get("ativo", True),
        )
        db.session.add(despesa)
        db.session.commit()
        return despesa, 201


@ns.route("/<int:despesa_id>")
@ns.response(404, "Despesa fixa não encontrada")
@ns.response(409, "Despesa fixa em uso")
class DespesaFixaResource(Resource):
    @ns.expect(despesa_fixa_model, validate=True)
    @ns.marshal_with(despesa_fixa_model)
    def put(self, despesa_id):
        """Atualiza uma despesa fixa (inclui ativar/desativar)."""
        despesa = DespesaFixa.query.get(despesa_id)
        if despesa is None:
            abort(404, "Despesa fixa não encontrada")
        dados = request.get_json()
        despesa.descricao = dados["descricao"]
        despesa.valor = dados["valor"]
        despesa.dia_vencimento = dados["dia_vencimento"]
        despesa.categoria_id = dados["categoria_id"]
        despesa.ativo = dados.get("ativo", despesa.ativo)
        db.session.commit()
        return despesa

    def delete(self, despesa_id):
        """Remove uma despesa fixa."""
        despesa = DespesaFixa.query.get(despesa_id)
        if despesa is None:
            abort(404, "Despesa fixa não encontrada")
        if despesa.transacoes:
            abort(409, "Despesa fixa já gerou lançamentos; desative-a em vez de excluir")
        db.session.delete(despesa)
        db.session.commit()
        return "", 204
