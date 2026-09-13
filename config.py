import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuração da aplicação Flask, incluindo a conexão com o SQLite."""

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'gastos.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
