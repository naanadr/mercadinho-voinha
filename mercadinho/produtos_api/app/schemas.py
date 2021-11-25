from datetime import date

from typing import List
from pydantic import BaseModel


class ProductBase(BaseModel):
    nome: str
    marca: str
    is_perecivel: bool


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    estoques: List[Inventory] = []
    dt_cadastro: date
    # Como linkar dois microsserviços?
    # pedidos: List[Pedido] = []

    class Config:
        orm_mode = True
