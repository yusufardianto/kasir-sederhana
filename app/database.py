from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

ENV = "development"  # Ganti dengan "production" jika di server
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/kasir_db"
DATABASE_URL_PRODUCTION = "mysql+pymysql://root:root@mysql:3306/kasir_db"

engine = create_engine(ENV == "production" and DATABASE_URL_PRODUCTION or DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ✅ Ini harus ada
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
