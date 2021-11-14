from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


user = "admin_mercadinho"
pwd = "super_senha"
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{pwd}@localhost:5432/db_mercadinho"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
