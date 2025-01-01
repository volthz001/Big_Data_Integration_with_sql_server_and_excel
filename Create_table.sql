-- 1. Membuat tabel baru dengan urutan kolom yang benar
CREATE TABLE nilai (
    id INT IDENTITY(1,1) PRIMARY KEY,  -- id menjadi kolom pertama
    nim NVARCHAR(50),
    id_mk INT,
    nilai DECIMAL(5, 2)
);
CREATE TABLE matakuliah (
    id INT PRIMARY KEY IDENTITY(1,1),      -- ID mata kuliah, auto increment
    kode_mk VARCHAR(10) NOT NULL,           -- Kode mata kuliah (contoh: "CS101")
    nama_mk VARCHAR(100) NOT NULL,          -- Nama mata kuliah (contoh: "Algoritma dan Pemrograman")
    sks INT NOT NULL,                       -- Jumlah SKS (contoh: 3)
    semester INT NOT NULL,                  -- Semester (contoh: 1, 2, dst)
    tahun_akademik VARCHAR(20) NOT NULL     -- Tahun akademik (contoh: "2025/2026")
);

