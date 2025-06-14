from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Produk(Base):
    __tablename__ = "produk"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(100))
    harga = Column(Integer)
    stok = Column(Integer)
    gambar = Column(String(255))

class Transaksi(Base):
    __tablename__ = "transaksi"

    id = Column(Integer, primary_key=True, index=True)
    tanggal = Column(DateTime, default=datetime.utcnow)
    total = Column(Integer, nullable=False)

    items = relationship("ItemTransaksi", back_populates="transaksi", cascade="all, delete")

class ItemTransaksi(Base):
    __tablename__ = "item_transaksi"

    id = Column(Integer, primary_key=True, index=True)
    transaksi_id = Column(Integer, ForeignKey("transaksi.id"))
    produk_id = Column(Integer)
    nama_produk = Column(String(100))  # ✅ tambahkan panjang
    jumlah = Column(Integer)
    subtotal = Column(Integer)

    transaksi = relationship("Transaksi", back_populates="items")
