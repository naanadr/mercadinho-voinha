from datetime import datetime

from sqlalchemy.orm import Session

from . import models, schemas


# ---- Start Inventory Section


def get_all_inventorys(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Inventory).offset(skip).limit(limit).all()


def get_inventory_by_id(db: Session, inventory_id: int):
    return (
        db.query(models.Inventory).filter(models.Inventory.id == inventory_id).first()
    )


def get_all_inventory_by_product_id(db: Session, product_id: int):
    return (
        db.query(models.Inventory)
        .filter(models.Inventory.id_produto == product_id)
        .all()
    )


def get_all_inventory_by_status_by_product_id(
    db: Session, product_id: int, status: bool = True
):
    return (
        db.query(models.Inventory)
        .filter(models.Inventory.id_produto == product_id)
        .filter(models.Inventory.is_ativo == status)
        .all()
    )


def get_all_inventory_by_status(db: Session, status: bool = True):
    return db.query(models.Inventory).filter(models.Inventory.is_ativo == status).all()


def create_inventory(db: Session, inventory: schemas.InventoryCreate, id_product: int):
    db_user = models.Inventory(**inventory.dict(), id_produto=id_product)
    db_user.dt_cadastro = datetime.now().date()
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def deactivate_inventory(db: Session, inventory: schemas.InventoryCreate, id: int):
    db.query(models.Inventory).filter(models.Inventory.id == id).update(inventory)
    db.commit()

    inventory["id"] = id
    db_user = models.Inventory(**inventory)
    return db_user


# ---- End Inventory Section


# ---- Start Product Section
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


# ---- End Product Section
