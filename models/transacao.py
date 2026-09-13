from datetime import date

from extensions import db


class Transacao(db.Model):
    __tablename__ = "transacao"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(140), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # "despesa" ou "receita"
    data = db.Column(db.Date, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)

    # Nulo quando o lançamento foi criado manualmente pelo usuário; preenchido
    # quando foi gerado automaticamente a partir de uma despesa fixa (rota
    # /transacoes/gerar-fixas), permitindo diferenciar a origem do lançamento.
    despesa_fixa_id = db.Column(db.Integer, db.ForeignKey("despesa_fixa.id"), nullable=True)

    def __init__(self, descricao: str, valor: float, tipo: str, data: date, categoria_id: int, despesa_fixa_id: int = None):
        """
        Cria uma Transacao.

        Arguments:
            descricao: descrição do lançamento.
            valor: valor do lançamento.
            tipo: "despesa" ou "receita".
            data: data em que o lançamento ocorreu.
            categoria_id: id da categoria do lançamento.
            despesa_fixa_id: id da despesa fixa de origem, se o lançamento foi gerado automaticamente.
        """
        self.descricao = descricao
        self.valor = valor
        self.tipo = tipo
        self.data = data
        self.categoria_id = categoria_id
        self.despesa_fixa_id = despesa_fixa_id

    def to_dict(self):
        """Retorna a representação da transação como dicionário, para depuração e uso fora da serialização automática da API."""
        return {
            "id": self.id,
            "descricao": self.descricao,
            "valor": self.valor,
            "tipo": self.tipo,
            "data": self.data.isoformat(),
            "categoria_id": self.categoria_id,
            "despesa_fixa_id": self.despesa_fixa_id,
        }
