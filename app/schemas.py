from pydantic import BaseModel
from typing import List

class ProdukBase(BaseModel):
    nama: str
    harga: int
    stok: int
    gambar: str | None = None  # ✅ optional

class ProdukCreate(ProdukBase):
    pass

class ProdukOut(BaseModel):
    id: int
    nama: str
    harga: int
    stok: int
    gambar_url: str  # akan dibuat dari field `gambar`

    class Config:
        from_attributes = True  # Pydantic v2 pengganti `orm_mode`
        
class Produk(ProdukBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2

class ItemTransaksiCreate(BaseModel):
    produk_id: int
    jumlah: int

class TransaksiCreate(BaseModel):
    items: List[ItemTransaksiCreate]