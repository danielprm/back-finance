from flask import request
from flask_restx import Namespace, Resource, abort, fields

from extensions import db
from models.categoria import Categoria

ns = Namespace("categorias", description="Cadastro de categorias de gastos")

categoria_model = ns.model("Categoria", {
    "id": fields.Integer(readonly=True),
    "nome": fields.String(required=True, description="Nome da categoria"),
    "cor": fields.String(required=True, description="Cor em hexadecimal, ex: #FF6B6B"),
})


@ns.route("")
class CategoriaListResource(Resource):
    @ns.marshal_list_with(categoria_model)
    def get(self):
        """Lista todas as categorias cadastradas."""
        return Categoria.query.all()

    @ns.expect(categoria_model, validate=True)
    @ns.marshal_with(categoria_model, code=201)
    def post(self):
        """Cadastra uma nova categoria."""
        dados = request.get_json()
        categoria = Categoria(nome=dados["nome"], cor=dados["cor"])
        db.session.add(categoria)
        db.session.commit()
        return categoria, 201


@ns.route("/<int:categoria_id>")
@ns.response(404, "Categoria não encontrada")
class CategoriaResource(Resource):
    @ns.marshal_with(categoria_model)
    def get(self, categoria_id):
        """Busca uma categoria pelo id."""
        categoria = Categoria.query.get(categoria_id)
        if categoria is None:
            abort(404, "Categoria não encontrada")
        return categoria

    def delete(self, categoria_id):
        """Remove uma categoria pelo id."""
        categoria = Categoria.query.get(categoria_id)
        if categoria is None:
            abort(404, "Categoria não encontrada")
        db.session.delete(categoria)
        db.session.commit()
        return "", 204
