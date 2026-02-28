import pandas as pd
from sqlalchemy import create_engine
import os

# Konfigurasi - Sesuaikan dengan password yang kita buat tadi
DB_URL = 'postgresql://postgres:abelganteng@localhost:5432/postgres'
CSV_FILE = 'data_spmb_83rb.csv'

def start_ingestion():
    if not os.path.exists(CSV_FILE):
        print(f"Error: File {CSV_FILE} tidak ditemukan!")
        return

    print(f"🚀 Memulai Ingest Data dari {CSV_FILE}...")
    engine = create_engine(DB_URL)

    # Membaca data secara bertahap (chunking) agar RAM tidak meledak
    # 83.000 data kita proses per 10.000 baris
    chunk_size = 10000
    batch = 1

    try:
        # Gunakan low_memory=False agar semua kolom terbaca tipenya dengan benar
        for chunk in pd.read_csv(CSV_FILE, chunksize=chunk_size, low_memory=False):
            # if_exists='replace' hanya untuk batch pertama, selanjutnya 'append'
            mode = 'replace' if batch == 1 else 'append'
            
            chunk.to_sql('ppdb_makassar', engine, if_exists=mode, index=False)
            print(f"✅ Berhasil memasukkan Batch {batch}...")
            batch += 1
            
        print("\n🔥 MANTAP! 83.000 data & semua kolom sudah aman di PostgreSQL.")
    except Exception as e:
        print(f"❌ Terjadi kesalahan: {e}")

if __name__ == "__main__":
    start_ingestion()