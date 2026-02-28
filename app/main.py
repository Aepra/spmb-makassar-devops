import pandas as pd
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text, inspect
from .database import engine, get_db

app = FastAPI(title="API PPDB Makassar - AbelDev")

# --- PROSES OTOMATISASI DATABASE ---
@app.on_event("startup")
def startup_event():
    inspector = inspect(engine)
    # 1. Cek apakah tabel 'ppdb_makassar' sudah ada di Postgres kantor
    if not inspector.has_table("ppdb_makassar"):
        print("Tabel belum ada! Memulai proses import 83rb data dari CSV...")
        try:
            # Pastikan file CSV ada di folder yang sama dengan docker-compose.yml
            # Kita baca pakai Pandas
            df = pd.read_csv("data_spmb_83rb.csv")
            
            # 2. Masukkan ke Postgres (otomatis buat tabel)
            df.to_sql("ppdb_makassar", engine, if_exists="replace", index=False)
            print("Berhasil! 83.000 data sudah siap di database.")
        except Exception as e:
            print(f"Gagal import data: {e}")
    else:
        print("Tabel sudah ada, siap melayani request!")

# --- ENDPOINT API ---
@app.get("/")
def root():
    return {"message": "API PPDB Makassar Aktif!", "owner": "Abel Eka Putra"}

@app.get("/data")
def read_data(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    # Mengambil data dengan manual query agar aman
    query = text(f"SELECT * FROM ppdb_makassar LIMIT {limit} OFFSET {skip}")
    result = db.execute(query)
    
    rows = [dict(row._mapping) for row in result]
    
    return {
        "total_tampil": len(rows),
        "offset": skip,
        "limit": limit,
        "data": rows
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # trigger update server.