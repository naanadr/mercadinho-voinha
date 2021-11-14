from datetime import datetime, date

from typing import List
from pydantic import BaseModel


# ---- Start Estoque Classes ----
class EstoqueBase(BaseModel):
    title: str
    dt_cadastro: date
    dt_validade: date
    qt_estoque: int
    vl_unidade: float
    unidade_medida: float


class EstoqueCreate(EstoqueBase):
    pass


class Estoque(EstoqueBase):
    id: int
    id_produto: int

    class Config:
        orm_mode = True


# ---- End Estoque Classes ----


# ---- Start Pedido Classes ----
class PedidoBase(BaseModel):
    id_pedido: int
    dt_cadastro: date
    qtd_produto: int
    vl_unidade: float
    vl_total_produto: float


class PedidoCreate(PedidoBase):
    pass


class Pedido(PedidoBase):
    id: int
    id_produto: int

    class Config:
        orm_mode = True


# ---- End Pedido Classes ----


# ---- Start Produto Classes ----
class ProdutoBase(BaseModel):
    nome: str
    is_perecivel: bool


class ProdutoCreate(ProdutoBase):
    pass


class Produto(ProdutoBase):
    id: int
    estoques: List[Estoque] = []
    pedidos: List[Pedido] = []

    class Config:
        orm_mode = True


# ---- End Produto Classes ----


# ---- Start Employee Classes ----
class EmployeeBase(BaseModel):
    cpf: str
    nome: str
    dt_nascimento: date
    dt_entrada: date
    dt_desligamento: date = None
    setor: str
    cargo: str


class EmployeeCreate(EmployeeBase):
    is_ativo: bool = True
    dt_atualizacao: date = datetime.now().date()


class Employee(EmployeeBase):
    id: int
    is_ativo: bool
    dt_atualizacao: date

    class Config:
        orm_mode = True


# ---- End Employee Classes ----
