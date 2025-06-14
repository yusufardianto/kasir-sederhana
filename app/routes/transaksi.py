from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/transaksi",
    tags=["Transaksi"]
)

# Buat transaksi baru
@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_transaksi(payload: schemas.TransaksiCreate, db: Session = Depends(get_db)):
    total = 0
    items = []

    for item in payload.items:
        produk = db.query(models.Produk).filter(models.Produk.id == item.produk_id).first()
        if not produk:
            raise HTTPException(status_code=404, detail=f"Produk ID {item.produk_id} tidak ditemukan")
        if produk.stok < item.jumlah:
            raise HTTPException(status_code=400, detail=f"Stok produk '{produk.nama}' tidak mencukupi")

        subtotal = produk.harga * item.jumlah
        total += subtotal

        # Kurangi stok
        produk.stok -= item.jumlah

        items.append(models.ItemTransaksi(
            produk_id=item.produk_id,
            nama_produk=produk.nama,
            jumlah=item.jumlah,
            subtotal=subtotal
        ))

    transaksi = models.Transaksi(
        tanggal=datetime.utcnow(),
        total=total,
        items=items
    )

    db.add(transaksi)
    db.commit()
    db.refresh(transaksi)

    return {
        "success": True,
        "message": "Transaksi berhasil dibuat",
        "data": {
            "id": transaksi.id,
            "total": transaksi.total,
            "tanggal": transaksi.tanggal,
            "items": [
                {
                    "produk_id": item.produk_id,
                    "nama_produk": item.nama_produk,
                    "jumlah": item.jumlah,
                    "subtotal": item.subtotal
                } for item in transaksi.items
            ]
        }
    }

# Get semua transaksi
@router.get("/", response_model=dict)
def get_all_transaksi(db: Session = Depends(get_db)):
    transaksi_list = db.query(models.Transaksi).all()

    hasil = []
    for trx in transaksi_list:
        hasil.append({
            "id": trx.id,
            "tanggal": trx.tanggal,
            "total": trx.total,
            "items": [
                {
                    "produk_id": item.produk_id,
                    "nama_produk": item.nama_produk,
                    "jumlah": item.jumlah,
                    "subtotal": item.subtotal
                } for item in trx.items
            ]
        })

    return {
        "success": True,
        "message": "Daftar transaksi",
        "data": hasil
    }
