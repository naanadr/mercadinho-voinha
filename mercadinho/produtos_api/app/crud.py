from datetime import datetime

from sqlalchemy.orm import Session

from . import models, schemas


def get_all_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).order_by("id").offset(skip).limit(limit).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_product_by_name(db: Session, name: str):
    return db.query(models.Product).filter(models.Product.nome == name).first()


def get_product_by_brand(
    db: Session, product_brand: str, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.Product)
        .filter(models.Product.marca == product_brand)
        .order_by("id")
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_product(db: Session, product: schemas.ProductCreate):
    product = product.dict()
    for key, value in dict(product).items():
        if type(value) == str:
            product[key] = value.lower()

    db_user = models.Product(**product)
    db_user.dt_cadastro = datetime.now().date()
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
