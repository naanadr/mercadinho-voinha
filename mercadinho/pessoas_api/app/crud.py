from datetime import datetime

from sqlalchemy.orm import Session

from . import models, schemas


def get_all_employee(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employee).order_by("id").offset(skip).limit(limit).all()


def get_employee_by_id(db: Session, id: int):
    return db.query(models.Employee).filter(models.Employee.id == id).first()


def get_employee_by_cpf(db: Session, cpf: str):
    return db.query(models.Employee).filter(models.Employee.cpf == cpf).first()


def get_employee_by_status(db: Session, status: bool):
    return db.query(models.Employee).filter(models.Employee.is_ativo == status).all()


def get_employee_by_setor(db: Session, setor: str):
    return db.query(models.Employee).filter(models.Employee.setor == setor).all()


def get_employee_by_cargo(db: Session, cargo: str):
    return db.query(models.Employee).filter(models.Employee.cargo == cargo).all()


def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_user = models.Employee(**employee.dict())
    db_user.dt_atualizacao = datetime.now().date()
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def fires_employee(db: Session, employee: schemas.EmployeeCreate):
    db.add(employee)
    db.commit()
    return employee


def update_employee(db: Session, employee: dict, id: int):
    db.query(models.Employee).filter(models.Employee.id == id).update(employee)
    db.commit()

    employee["id"] = id
    db_user = models.Employee(**employee)
    return db_user
