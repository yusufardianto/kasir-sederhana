from fastapi import FastAPI
from app.routes import produk
from app import models
from app.database import engine
from app.routes import transaksi
# from app.routes import gambar
from fastapi.staticfiles import StaticFiles

app = FastAPI()
# CREATE DATABASE kasir_db;

models.Base.metadata.create_all(bind=engine)
print("Starting FastAPI App 1 ...")
app.include_router(produk.router, tags=["Produk"])
# app.include_router(gambar.router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="static")
app.include_router(transaksi.router)
# Mount folder uploads/
print("Starting FastAPI App 2...")
@app.get("/")
def read_root():
    return {"message": "Aplikasi Kasir Sederhana"}
