# Integrasi_Big_Data_dengan_SQL_Server_dan_Excel

Proyek ini menunjukkan integrasi SQL Server dan Excel untuk menangani dan memproses dataset besar. Proyek ini berfokus pada impor data, kueri, dan penyajian data melalui API.

---

## Gambaran Umum

Proyek ini menggunakan:
- **SQL Server** untuk menyimpan dan mengkueri dataset hingga 10 juta data.
- **Excel** untuk mengimpor data hingga 1 juta baris.
- **FastAPI** sebagai kerangka kerja backend untuk melayani permintaan API.
- **Uvicorn** untuk menjalankan server FastAPI.

---

## Fitur

1. Impor file Excel dan simpan data ke SQL Server.
2. Kueri data secara efisien menggunakan query SQL yang dioptimalkan.
3. Sajikan data melalui API untuk aplikasi eksternal.
4. Dokumentasi API interaktif secara otomatis.

---

## Persyaratan

- Python 3.8+
- SQL Server
- Excel (untuk mengimpor data)
- Pustaka Python yang diperlukan (tercantum dalam `requirements.txt`):
  - FastAPI
  - Uvicorn
  - pyodbc (untuk koneksi SQL Server)
  - openpyxl (untuk pengolahan Excel)

---

## Instalasi dan Konfigurasi

### 1. Clone Repositori
```bash
git clone https://github.com/volthz001/Integrasi_Big_Data_dengan_SQL_Server_dan_Excel.git
cd Integrasi_Big_Data_dengan_SQL_Server_dan_Excel
