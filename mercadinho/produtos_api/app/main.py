from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .utils.docs import DESCRIPTION, TAGS_METADATA

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ProdutosAPI",
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


@app.post("/product/", response_model=schemas.Product, tags=["product"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_name(db, name=product.nome)
    if db_product is not None and db_product.marca == product.marca:
        raise HTTPException(
            status_code=400,
            detail="Product already save! Try again with another product.",
        )
    return crud.create_product(db=db, product=product)


@app.get("/product/", response_model=List[schemas.Product], tags=["product"])
def get_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_all_products(db, skip=skip, limit=limit)
    return products


@app.get(
    "/product/id/{product_id}",
    response_model=schemas.Product,
    tags=["product"],
)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found!")
    return product


@app.get(
    "/product/name/{product_name}",
    response_model=schemas.Product,
    tags=["product"],
)
def get_product_by_name(product_name: str, db: Session = Depends(get_db)):
    product = crud.get_product_by_name(db, product_name.lower())
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found!")
    return product


@app.get(
    "/product/brand/{product_brand}",
    response_model=List[schemas.Product],
    tags=["product"],
)
def get_product_by_brand(product_brand: str, db: Session = Depends(get_db)):
    product = crud.get_product_by_brand(db, product_brand.lower())
    if product is None:
        raise HTTPException(status_code=404, detail="Brand not found!")
    return product
