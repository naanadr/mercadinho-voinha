from datetime import date

from typing import List
from pydantic import BaseModel


# ---- Start Inventory Classes ----
class InventoryBase(BaseModel):
    is_ativo: bool


class InventoryStaticFields(InventoryBase):
    dt_validade: date
    qt_estoque: int
    vl_unidade: float
    unidade_medida: str


class InventoryCreate(InventoryStaticFields):
    is_ativo: bool = True


class InventoryDeactivate(InventoryBase):
    pass


class Inventory(InventoryStaticFields):
    id: int
    id_produto: int
    dt_cadastro: date

    class Config:
        orm_mode = True


# ---- End Inventory Classes ----


# ---- Start Product Classes ----
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


# ---- End Product Classes ----
