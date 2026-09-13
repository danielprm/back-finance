from extensions import db


class DespesaFixa(db.Model):
    __tablename__ = "despesa_fixa"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(140), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    dia_vencimento = db.Column(db.Integer, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    # Cada despesa fixa pode gerar várias transações ao longo dos meses (uma
    # por mês em que foi lançada). Isso permite consultar, a partir da
    # despesa fixa, todo o seu histórico de lançamentos já gerados.
    transacoes = db.relationship("Transacao", backref="despesa_fixa", lazy=True)

    def __init__(self, descricao: str, valor: float, dia_vencimento: int, categoria_id: int, ativo: bool = True):
        """
        Cria uma DespesaFixa.

        Arguments:
            descricao: nome da despesa recorrente (ex: "Aluguel").
            valor: valor mensal esperado da despesa.
            dia_vencimento: dia do mês (1-31) em que a despesa normalmente vence.
            categoria_id: id da categoria à qual a despesa pertence.
            ativo: se False, a despesa fixa não é considerada na geração mensal de lançamentos.
        """
        self.descricao = descricao
        self.valor = valor
        self.dia_vencimento = dia_vencimento
        self.categoria_id = categoria_id
        self.ativo = ativo

    def to_dict(self):
        """Retorna a representação da despesa fixa como dicionário, para depuração e uso fora da serialização automática da API."""
        return {
            "id": self.id,
            "descricao": self.descricao,
            "valor": self.valor,
            "dia_vencimento": self.dia_vencimento,
            "categoria_id": self.categoria_id,
            "ativo": self.ativo,
        }
