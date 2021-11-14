from datetime import datetime, date

from typing import Optional

from pydantic import BaseModel


class EmployeeBase(BaseModel):
    nome: str
    dt_nascimento: date
    dt_entrada: date


class EmployeeStaticFields(EmployeeBase):
    cpf: str
    setor: str
    cargo: str


class EmployeeCreate(EmployeeStaticFields):
    is_ativo: bool = True
    dt_entrada: date = datetime.now().date()
    dt_desligamento: date = date(1900, 1, 1)


class EmployeeUpdate(EmployeeBase):
    nome: Optional[str]
    dt_nascimento: Optional[date]
    dt_entrada: Optional[date]
    dt_desligamento: Optional[date]
    is_ativo: Optional[bool]


class Employee(EmployeeStaticFields):
    id: int
    is_ativo: bool
    dt_atualizacao: date
    dt_desligamento: date

    class Config:
        orm_mode = True
