from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Estoque(Base):

    __tablename__ = "tb_estoque"

    id = Column(Integer, unique=True, primary_key=True)
    dt_cadastro = Column(Date)
    dt_validade = Column(Date)
    qt_estoque = Column(Integer)
    vl_unidade = Column(Float)
    unidade_medida = Column(String)
    id_produto = Column(Integer, ForeignKey("tb_produto.id"))

    produtos = relationship("Produto", back_populates="estoques")


class Pedido(Base):

    __tablename__ = "tb_pedido"

    id = Column(Integer, primary_key=True)
    id_pedido = Column(Integer)
    dt_cadastro = Column(Date)
    id_produto = Column(Integer, ForeignKey("tb_produto.id"))
    qtd_produto = Column(Integer)
    vl_unidade = Column(Float)
    vl_total_produto = Column(Float)

    produtos = relationship("Produto", back_populates="pedidos")


class Produto(Base):

    __tablename__ = "tb_produto"

    id = Column(Integer, unique=True)
    nome = Column(String, primary_key=True)
    is_perecivel = Column(Boolean)

    estoques = relationship("Estoque", back_populates="produtos")
    pedidos = relationship("Pedido", back_populates="produtos")


class Employee(Base):

    __tablename__ = "tb_employees"

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
