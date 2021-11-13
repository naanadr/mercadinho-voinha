from sqlalchemy import Boolean, Column, Date, inspect, Integer, String

from .database import Base


class Employee(Base):

    __tablename__ = "tb_funcionarios"

    id = Column(Integer, primary_key=True)
    cpf = Column(String)
    nome = Column(String)
    dt_nascimento = Column(Date)
    dt_entrada = Column(Date)
    dt_desligamento = Column(Date)
    dt_atualizacao = Column(Date)
    setor = Column(String)
    cargo = Column(String)
    is_ativo = Column(Boolean)

    def _asdict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
