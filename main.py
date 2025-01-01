from fastapi import FastAPI, HTTPException, Query,Path
import pandas as pd
import pyodbc

app = FastAPI()

def get_db_connection():
    server = r'DESKTOP-11804QR\SQLEXPRESS'  
    database = 'W_api'  
    connection_string = (
        "DRIVER={SQL Server Native Client 11.0};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
    )
    conn = pyodbc.connect(connection_string)
    return conn
@app.get("/matakuliah/{kode_mk}")
async def get_matakuliah(kode_mk: str):
    # Menghubungkan ke database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "SELECT id, kode_mk, nama_mk, sks, semester, tahun_akademik FROM matakuliah WHERE kode_mk = ?"
        cursor.execute(query, (kode_mk,))
        
        matakuliah_data = cursor.fetchall()
        
        if not matakuliah_data:
            raise HTTPException(status_code=404, detail="Mata kuliah tidak ditemukan")
        
        column_names = [col[0] for col in cursor.description]
        matakuliah_data = [dict(zip(column_names, row)) for row in matakuliah_data]
        
        return matakuliah_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan pada server: {str(e)}")
    
    finally:
        cursor.close()
        conn.close()
@app.get("/nilai/{nim}")
async def get_nilai(nim: str = Path(..., title="NIM Mahasiswa", description="Input Nim untuk melihat data nilai")):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "SELECT id, id_mk, nilai FROM nilai WHERE nim = ?"
        cursor.execute(query, (nim,))
        
        mahasiswa_data_db = cursor.fetchall()
        
        if not mahasiswa_data_db:
            raise HTTPException(status_code=404, detail="Data mahasiswa tidak ditemukan")
        
        column_names = [col[0] for col in cursor.description]
        
        mahasiswa_data_db = [dict(zip(column_names, row)) for row in mahasiswa_data_db]
        
        return mahasiswa_data_db
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan pada server: {str(e)}")
    
    finally:
        cursor.close()
        conn.close()

@app.get("/mahasiswa/{nim}")
async def get_mahasiswa(nim: str = Path(..., title="NIM Mahasiswa", description="Nomor Induk Mahasiswa yang ingin dicari")):
    # Membaca file CSV
    try:
        df = pd.read_csv("mhs_updated.csv", dtype={'nim': str})  # Pastikan nim dalam format string
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan saat membaca file CSV: {str(e)}")
    
    mahasiswa_csv = df[df['nim'] == nim]
    
    if mahasiswa_csv.empty:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan di file CSV")
    
    result_csv = mahasiswa_csv.to_dict(orient="records")[0]
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "SELECT id, id_mk, nilai FROM nilai WHERE nim = ?"
        cursor.execute(query, (nim,))
        
        mahasiswa_db = cursor.fetchall()
        
        if not mahasiswa_db:
            raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan di database")
        
        column_names = [col[0] for col in cursor.description]
        
        mahasiswa_data_db = [dict(zip(column_names, row)) for row in mahasiswa_db]
    
    except Exception as e:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan saat mengakses database: {str(e)}")
    
    finally:
        cursor.close()
        conn.close()
    
    return {"result": (f"""id:{mahasiswa_data_db[0]['id']}|nama:,{result_csv['nama']}|nim:{result_csv['nim']}|Kelas:{result_csv['kelas']}|id_mk: {mahasiswa_data_db[0]['id_mk']}|nilai{mahasiswa_data_db[0]['nilai']}""")}#id:",mahasiswa_data_db[0],"id_mk:",mahasiswa_data_db[1],"nilai:",mahasiswa_data_db[-1])}
