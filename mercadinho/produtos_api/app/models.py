from sqlalchemy import (
    Boolean,
    Column,
    Date,
    inspect,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from .database import Base


class Product(Base):

    __tablename__ = "tb_produto"

    id = Column(Integer, unique=True, primary_key=True)
    nome = Column(String, primary_key=True)
    marca = Column(String, primary_key=True)
    dt_cadastro = Column(Date)
    is_perecivel = Column(Boolean)

    estoques = relationship("Inventory", back_populates="produtos")

    def _asdict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
