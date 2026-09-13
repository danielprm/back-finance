from extensions import db


class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    cor = db.Column(db.String(7), nullable=False)

    # Uma categoria pode ter várias despesas fixas e transações associadas.
    # Esse relacionamento não existe como coluna na tabela 'categoria': é o
    # SQLAlchemy quem reconstrói essa lista a partir da foreign key nas
    # tabelas filhas.
    despesas_fixas = db.relationship("DespesaFixa", backref="categoria", lazy=True)
    transacoes = db.relationship("Transacao", backref="categoria", lazy=True)

    def __init__(self, nome: str, cor: str):
        """
        Cria uma Categoria.

        Arguments:
            nome: nome de exibição da categoria (ex: "Alimentação").
            cor: cor em hexadecimal usada para identificar a categoria na interface (ex: "#FF6B6B").
        """
        self.nome = nome
        self.cor = cor

    def to_dict(self):
        """Retorna a representação da categoria como dicionário, para depuração e uso fora da serialização automática da API."""
        return {"id": self.id, "nome": self.nome, "cor": self.cor}
