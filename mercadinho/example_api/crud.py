from sqlalchemy.orm import Session

from . import models, schemas


# ---- Start Estoque Section
def get_estoque_by_id(db: Session, estoque_id: int):
    return db.query(models.Estoque).filter(models.Estoque.id == estoque_id).first()


def get_all_estoque_by_produto(db: Session, produto_id: int):
    return (
        db.query(models.Estoque).filter(models.Estoque.id_produto == produto_id).all()
    )


def get_estoque_by_unidade_medida(db: Session, unidade_medida: str):
    return (
        db.query(models.Estoque)
        .filter(models.Estoque.unidade_medida == unidade_medida)
        .first()
    )


def get_estoque(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Estoque).offset(skip).limit(limit).all()


def create_estoque(db: Session, estoque: schemas.EstoqueCreate, id_produto: int):
    db_user = models.Estoque(**estoque.dict(), id_produto=id_produto)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ---- End Estoque Section


# ---- Start Pedido Section
def get_pedido_by_id(db: Session, pedido_id: int):
    return db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()


def get_pedido_by_produto(db: Session, id_produto: int):
    return db.query(models.Pedido).filter(models.Pedido.id_pedido == id_produto).first()


def create_pedido(db: Session, pedido: schemas.PedidoCreate):
    db_user = models.Pedido(**pedido.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ---- End Pedido Section


# ---- Start Produto Section
def get_produto_by_id(db: Session, produto_id: int):
    return db.query(models.Produto).filter(models.Produto.id == produto_id).first()


def get_produto_by_nome(db: Session, nome: str):
    return db.query(models.Produto).filter(models.Produto.nome == nome).first()


def create_produto(db: Session, produto: schemas.ProdutoCreate):
    db_user = models.Produto(**produto.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ---- End Produto Section


# ---- Start Employee Section
def get_employee_by_id(db: Session, employee_id: int):
    return (
        db.query(models.Employee)
        .filter(models.Employee.id == employee_id)
        .first()
    )


def get_employee_by_cpf(db: Session, cpf: str):
    return db.query(models.Employee).filter(models.Employee.cpf == cpf).first()


def get_all_employee(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employee).offset(skip).limit(limit).all()


def get_employee_by_status(db: Session, status: bool):
    return (
        db.query(models.Employee).filter(models.Employee.is_ativo == status).all()
    )


def get_employee_by_setor(db: Session, setor: str):
    return db.query(models.Employee).filter(models.Employee.setor == setor).all()


def get_employee_by_cargo(db: Session, cargo: str):
    return db.query(models.Employee).filter(models.Employee.cargo == cargo).all()


def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_user = models.Employee(**employee.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ---- End Employee Section
