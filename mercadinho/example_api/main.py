from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .utils.docs import DESCRIPTION, TAGS_METADATA

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MercadinhoVoinhaAPP",
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
def create_employee(
    employee: schemas.EmployeeCreate, db: Session = Depends(get_db)
):
    db_employee = crud.get_employee_by_cpf(db, cpf=employee.cpf)
    if db_employee:
        raise HTTPException(status_code=400, detail="Funcionário já cadastrado!")
    return crud.create_employee(db=db, employee=employee)


@app.get(
    "/employee/", response_model=List[schemas.Employee], tags=["employees"]
)
def read_all_employees(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    employee = crud.get_all_employee(db, skip=skip, limit=limit)
    return employee


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
#
#
# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
#
#
# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
