from sqlalchemy.orm import Session
from app import models, schemas

# Ambil semua produk
def get_all_produk(db: Session):
    return db.query(models.Produk).all()

# Tambah produk
def create_produk(db: Session, produk: schemas.ProdukCreate):
    db_produk = models.Produk(**produk.dict())
    db.add(db_produk)
    db.commit()
    db.refresh(db_produk)
    return db_produk

# Ambil produk berdasarkan ID
def get_produk_by_id(db: Session, produk_id: int):
    return db.query(models.Produk).filter(models.Produk.id == produk_id).first()

# Update produk
def update_produk(db: Session, produk_id: int, produk_data: schemas.ProdukCreate):
    produk = get_produk_by_id(db, produk_id)
    if produk:
        produk.nama = produk_data.nama
        produk.harga = produk_data.harga
        produk.stok = produk_data.stok
        db.commit()
        db.refresh(produk)
    return produk

# Hapus produk
def delete_produk(db: Session, produk_id: int):
    produk = get_produk_by_id(db, produk_id)
    if produk:
        db.delete(produk)
        db.commit()
    return produk
