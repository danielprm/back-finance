from datetime import date

from flask import request
from flask_restx import Namespace, Resource, fields
from sqlalchemy import extract

from models.categoria import Categoria
from models.transacao import Transacao

ns = Namespace("resumo", description="Totais e indicadores do mês")

por_categoria_model = ns.model("TotalPorCategoria", {
    "categoria": fields.String,
    "total": fields.Float,
})

resumo_model = ns.model("Resumo", {
    "mes": fields.Integer,
    "ano": fields.Integer,
    "saldo": fields.Float,
    "total_receitas": fields.Float,
    "total_despesas": fields.Float,
    "total_fixo": fields.Float,
    "total_eventual": fields.Float,
    "por_categoria": fields.List(fields.Nested(por_categoria_model)),
})


@ns.route("")
class ResumoResource(Resource):
    @ns.param("mes", "Mês (1-12); padrão: mês atual", type=int)
    @ns.param("ano", "Ano com 4 dígitos; padrão: ano atual", type=int)
    @ns.marshal_with(resumo_model)
    def get(self):
        """Retorna saldo, totais por categoria e fixo x eventual do mês informado (padrão: mês atual)."""
        hoje = date.today()
        mes = request.args.get("mes", type=int, default=hoje.month)
        ano = request.args.get("ano", type=int, default=hoje.year)

        transacoes = Transacao.query.filter(
            extract("month", Transacao.data) == mes,
            extract("year", Transacao.data) == ano,
        ).all()

        total_receitas = sum(t.valor for t in transacoes if t.tipo == "receita")
        total_despesas = sum(t.valor for t in transacoes if t.tipo == "despesa")
        total_fixo = sum(
            t.valor for t in transacoes if t.tipo == "despesa" and t.despesa_fixa_id is not None
        )
        total_eventual = total_despesas - total_fixo

        # Agrupa os gastos por categoria para alimentar os cards do dashboard.
        totais_por_categoria = {}
        for t in transacoes:
            if t.tipo != "despesa":
                continue
            categoria = Categoria.query.get(t.categoria_id)
            nome_categoria = categoria.nome if categoria else "Sem categoria"
            totais_por_categoria[nome_categoria] = totais_por_categoria.get(nome_categoria, 0) + t.valor

        return {
            "mes": mes,
            "ano": ano,
            "saldo": total_receitas - total_despesas,
            "total_receitas": total_receitas,
            "total_despesas": total_despesas,
            "total_fixo": total_fixo,
            "total_eventual": total_eventual,
            "por_categoria": [
                {"categoria": nome, "total": total} for nome, total in totais_por_categoria.items()
            ],
        }
