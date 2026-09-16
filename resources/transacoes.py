import calendar
from datetime import date

from flask import request
from flask_restx import Namespace, Resource, abort, fields
from sqlalchemy import extract

from extensions import db
from models.despesa_fixa import DespesaFixa
from models.transacao import Transacao

ns = Namespace("transacoes", description="Lançamentos de despesas e receitas")

transacao_model = ns.model("Transacao", {
    "id": fields.Integer(readonly=True),
    "descricao": fields.String(required=True),
    "valor": fields.Float(required=True),
    "tipo": fields.String(required=True, description='"despesa" ou "receita"'),
    "data": fields.String(required=True, description="Data no formato AAAA-MM-DD"),
    "categoria_id": fields.Integer(required=True),
    "despesa_fixa_id": fields.Integer(readonly=True),
})

geracao_model = ns.model("GeracaoFixas", {
    "geradas": fields.Integer(description="Quantidade de lançamentos criados"),
})


@ns.route("")
class TransacaoListResource(Resource):
    @ns.marshal_list_with(transacao_model)
    def get(self):
        """Lista transações, com filtro opcional por mês (?mes=) e ano (?ano=)."""
        query = Transacao.query
        mes = request.args.get("mes", type=int)
        ano = request.args.get("ano", type=int)
        if mes:
            query = query.filter(extract("month", Transacao.data) == mes)
        if ano:
            query = query.filter(extract("year", Transacao.data) == ano)
        return query.order_by(Transacao.data.desc()).all()

    @ns.expect(transacao_model, validate=True)
    @ns.marshal_with(transacao_model, code=201)
    def post(self):
        """Cria um lançamento manual de despesa ou receita."""
        dados = request.get_json()
        transacao = Transacao(
            descricao=dados["descricao"],
            valor=dados["valor"],
            tipo=dados["tipo"],
            data=date.fromisoformat(dados["data"]),
            categoria_id=dados["categoria_id"],
        )
        db.session.add(transacao)
        db.session.commit()
        return transacao, 201


@ns.route("/<int:transacao_id>")
@ns.response(404, "Transação não encontrada")
class TransacaoResource(Resource):
    @ns.marshal_with(transacao_model)
    def get(self, transacao_id):
        """Busca uma transação pelo id."""
        transacao = Transacao.query.get(transacao_id)
        if transacao is None:
            abort(404, "Transação não encontrada")
        return transacao

    def delete(self, transacao_id):
        """Remove uma transação."""
        transacao = Transacao.query.get(transacao_id)
        if transacao is None:
            abort(404, "Transação não encontrada")
        db.session.delete(transacao)
        db.session.commit()
        return "", 204


@ns.route("/gerar-fixas")
class GerarFixasResource(Resource):
    @ns.marshal_with(geracao_model, code=201)
    def post(self):
        """
        Gera as transações do mês atual a partir das despesas fixas ativas.

        Idempotente: se uma despesa fixa já tiver uma transação gerada para o
        mês/ano atual, ela não é duplicada.
        """
        hoje = date.today()
        despesas_ativas = DespesaFixa.query.filter_by(ativo=True).all()
        quantidade_gerada = 0

        for despesa in despesas_ativas:
            ja_gerada = Transacao.query.filter(
                Transacao.despesa_fixa_id == despesa.id,
                extract("month", Transacao.data) == hoje.month,
                extract("year", Transacao.data) == hoje.year,
            ).first()
            if ja_gerada is not None:
                continue

            # O dia de vencimento cadastrado pode não existir no mês atual
            # (ex: vencimento dia 31 em fevereiro), então usamos o último dia
            # válido do mês nesse caso.
            ultimo_dia_do_mes = calendar.monthrange(hoje.year, hoje.month)[1]
            dia = min(despesa.dia_vencimento, ultimo_dia_do_mes)

            transacao = Transacao(
                descricao=despesa.descricao,
                valor=despesa.valor,
                tipo="despesa",
                data=date(hoje.year, hoje.month, dia),
                categoria_id=despesa.categoria_id,
                despesa_fixa_id=despesa.id,
            )
            db.session.add(transacao)
            quantidade_gerada += 1

        db.session.commit()
        return {"geradas": quantidade_gerada}, 201
