from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import get_db

app = FastAPI(title="API PPDB Makassar - AbelDev")

@app.get("/")
def root():
    return {"message": "API PPDB Makassar Aktif!", "owner": "Abel Eka Putra"}

@app.get("/data")
def read_data(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    # Kita ambil data dari tabel yang dibuat oleh script ingest_csv.py
    # Menggunakan manual query agar 'Zero Column Loss' tetap terjaga
    query = text(f"SELECT * FROM ppdb_makassar LIMIT {limit} OFFSET {skip}")
    result = db.execute(query)
    
    # Mengubah hasil query menjadi list of dictionary agar jadi JSON
    rows = [dict(row._mapping) for row in result]
    
    return {
        "total_tampil": len(rows),
        "offset": skip,
        "limit": limit,
        "data": rows
    }