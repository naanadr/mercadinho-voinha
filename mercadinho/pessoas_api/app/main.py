from datetime import datetime, date

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import SessionLocal, engine
from .utils.docs import DESCRIPTION, TAGS_METADATA


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PessoasAPI",
    description=DESCRIPTION,
    version="0.0.1",
    openapi_tags=TAGS_METADATA,
    docs_url="/",
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/employee/", response_model=schemas.Employee, tags=["employees"])
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = crud.get_employee_by_cpf(db, cpf=employee.cpf)
    if db_employee:
        raise HTTPException(
            status_code=400, detail="User already save! Try again with another user."
        )
    return crud.create_employee(db=db, employee=employee)


@app.post(
    "/employee/{employee_id}/fires/",
    response_model=schemas.Employee,
    tags=["employees"],
)
def fires_employee(
    employee_id: int,
    date_fires: date = datetime.now().date(),
    db: Session = Depends(get_db),
):
    db_employee = crud.get_employee_by_id(db, id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=400, detail="User not found!")
    elif db_employee.dt_desligamento != date(1900, 1, 1):
        raise HTTPException(status_code=400, detail="User already fires!")

    db_employee.dt_desligamento = date_fires
    db_employee.dt_atualizacao = datetime.now().date()
    db_employee.is_ativo = False
    return crud.fires_employee(db=db, employee=db_employee)


@app.post(
    "/employee/{employee_id}/update/",
    response_model=schemas.Employee,
    tags=["employees"],
)
def update_employee(
    employee_id: int, employee: schemas.EmployeeUpdate, db: Session = Depends(get_db)
):
    employee = employee.dict()
    db_employee = crud.get_employee_by_id(db, id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="User not found!")

    for key, value in dict(employee).items():
        if value is None:
            del employee[key]

    new_employee = db_employee._asdict()
    new_employee.update(employee)
    del new_employee["id"]
    return crud.update_employee(db=db, employee=new_employee, id=employee_id)


@app.get("/employee/", response_model=List[schemas.Employee], tags=["employees"])
def get_all_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employee = crud.get_all_employee(db, skip=skip, limit=limit)
    return employee


@app.get(
    "/employee/id/{employee_id}",
    response_model=schemas.Employee,
    tags=["employees"],
)
def get_employee_by_id(employee_id: int, db: Session = Depends(get_db)):
    employee = crud.get_employee_by_id(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="User not found")
    return employee


@app.get(
    "/employee/cpf/{employee_cpf}",
    response_model=schemas.Employee,
    tags=["employees"],
)
def get_employee_by_cpf(employee_cpf: str, db: Session = Depends(get_db)):
    employee = crud.get_employee_by_cpf(db, employee_cpf)
    if employee is None:
        raise HTTPException(status_code=404, detail="User not found")
    return employee


@app.get(
    "/employee/status/{employee_status}",
    response_model=List[schemas.Employee],
    tags=["employees"],
)
def get_employee_by_status(employee_status: bool, db: Session = Depends(get_db)):
    employee = crud.get_employee_by_status(db, employee_status)
    return employee


@app.get(
    "/employee/setor/{employee_setor}",
    response_model=List[schemas.Employee],
    tags=["employees"],
)
def get_employee_by_setor(employee_setor: str, db: Session = Depends(get_db)):
    employee = crud.get_employee_by_setor(db, employee_setor)
    return employee


@app.get(
    "/employee/cargo/{employee_cargo}",
    response_model=List[schemas.Employee],
    tags=["employees"],
)
def get_employee_by_cargo(employee_cargo: str, db: Session = Depends(get_db)):
    employee = crud.get_employee_by_cargo(db, employee_cargo)
    return employee
