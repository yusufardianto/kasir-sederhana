from fastapi import APIRouter, HTTPException, Depends, UploadFile, File,Form
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db
from fastapi import Query
from typing import Optional
from fastapi import Request
from fastapi.responses import FileResponse
import shutil
import os
import uuid

router = APIRouter(prefix="/produk", tags=["Produk"])

UPLOAD_DIR = "uploads"

@router.get("/", response_model=dict)
def get_produk_list(
    request: Request,
    q: str = Query(default=None, description="Pencarian produk berdasarkan nama"),
    db: Session = Depends(get_db)
):
    if q:
        produk_list = db.query(models.Produk).filter(models.Produk.nama.ilike(f"%{q}%")).all()
    else:
        produk_list = db.query(models.Produk).all()

    result = []
    for p in produk_list:
        gambar_url = str(request.url_for("get_gambar", filename=p.gambar)) if p.gambar else None
        result.append({
            "id": p.id,
            "nama": p.nama,
            "harga": p.harga,
            "stok": p.stok,
            "gambar_url": gambar_url
        })

    return {
        "success": True,
        "data": result
    }

@router.get("/uploads/{filename}", name="get_gambar")
def get_gambar(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"detail": "File not found"}

# POST produk baru
@router.post("/", response_model=dict)
def create_produk(
    nama: str = Form(...),
    harga: int = Form(...),
    stok: int = Form(...),
    gambar: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Simpan gambar
    ext = gambar.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(gambar.file, buffer)

    # Simpan ke DB
    new_produk = models.Produk(
        nama=nama,
        harga=harga,
        stok=stok,
        gambar=filename
    )
    db.add(new_produk)
    db.commit()
    db.refresh(new_produk)

    return {
        "success": True,
        "message": "Produk berhasil ditambahkan",
        "data": {
            "id": new_produk.id,
            "nama": new_produk.nama,
            "harga": new_produk.harga,
            "stok": new_produk.stok,
            "gambar": new_produk.gambar
        }
    }

@router.put("/{produk_id}", response_model=dict)
def update_produk(
    produk_id: int,
    nama: str = Form(...),
    harga: int = Form(...),
    stok: int = Form(...),
    gambar: UploadFile = File(None),  # opsional, tidak wajib dikirim
    db: Session = Depends(get_db)
):
    db_produk = db.query(models.Produk).filter(models.Produk.id == produk_id).first()
    if not db_produk:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")

    # Update data basic
    db_produk.nama = nama
    db_produk.harga = harga
    db_produk.stok = stok

    # Kalau ada gambar baru dikirim, simpan dan ganti
    if gambar:
        ext = gambar.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(gambar.file, buffer)

        # (Opsional) Hapus file lama kalau perlu
        if db_produk.gambar:
            lama = os.path.join(UPLOAD_DIR, db_produk.gambar)
            if os.path.exists(lama):
                os.remove(lama)

        db_produk.gambar = filename

    db.commit()
    db.refresh(db_produk)

    return {
        "success": True,
        "message": "Produk berhasil diupdate",
        "data": {
            "id": db_produk.id,
            "nama": db_produk.nama,
            "harga": db_produk.harga,
            "stok": db_produk.stok,
            "gambar": db_produk.gambar
        }
    }

# Hapus produk
@router.delete("/{produk_id}", response_model=dict)
def delete_produk(produk_id: int, db: Session = Depends(get_db)):
    db_produk = db.query(models.Produk).filter(models.Produk.id == produk_id).first()
    if not db_produk:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")

    db.delete(db_produk)
    db.commit()
    return {
        "success": True,
        "message": "Produk berhasil dihapus"
    }
