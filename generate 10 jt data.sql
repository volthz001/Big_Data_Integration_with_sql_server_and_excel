-- Pastikan Anda berada di database yang benar
USE W_api;
GO

-- Periksa apakah tabel nilai sudah ada
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'nilai')
BEGIN
    PRINT 'Tabel nilai tidak ditemukan. Pastikan tabel nilai sudah dibuat sebelum menambahkan data.';
    RETURN;
END;

-- Variabel untuk Batch Processing
DECLARE @batch_size INT = 100000;      -- Ukuran data per batch
DECLARE @total BIGINT = 10000000;      -- Total data yang akan ditambahkan
DECLARE @current_id BIGINT = 1;        -- Awal ID baru
DECLARE @max_id BIGINT;                -- ID terakhir dalam tabel

-- Ambil ID terakhir dari tabel
SELECT @max_id = ISNULL(MAX(id), 0) FROM nilai;

-- Temporary table untuk menyimpan NIM unik
CREATE TABLE #TempNIM (
    nim NVARCHAR(8) PRIMARY KEY
);

-- Generate NIM unik untuk semua data yang dibutuhkan
WITH NIMGen AS (
    SELECT TOP (@total) 
        ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) + 10000000 AS NIM
    FROM master.dbo.spt_values t1
    CROSS JOIN master.dbo.spt_values t2
)
INSERT INTO #TempNIM (nim)
SELECT CAST(NIM AS NVARCHAR(8)) FROM NIMGen;

-- Aktifkan IDENTITY_INSERT untuk tabel 'nilai'
SET IDENTITY_INSERT nilai ON;

-- Loop untuk Batch Processing
WHILE @current_id <= @total
BEGIN
    -- Tambahkan data dalam batch
    INSERT INTO nilai (id, nim, id_mk, nilai)
    SELECT 
        @max_id + ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS id,            -- ID unik
        nim,                                                                  -- NIM unik
        FLOOR(RAND(CHECKSUM(NEWID())) * (10 - 1 + 1) + 1) AS id_mk,            -- ID Mata Kuliah (1-10)
        CAST(FLOOR((RAND(CHECKSUM(NEWID())) * (87.00 - 40.00) + 40.00) * 100) / 100 AS DECIMAL(5, 2)) -- Nilai (40-87)
    FROM 
        (SELECT TOP (@batch_size) nim FROM #TempNIM ORDER BY NEWID()) AS t;

    -- Update ID dan batch counter
    SET @max_id = @max_id + @batch_size;
    SET @current_id = @current_id + @batch_size;

    PRINT CAST(@current_id AS NVARCHAR(50)) + ' records processed.';
END;

-- Nonaktifkan IDENTITY_INSERT untuk tabel 'nilai'
SET IDENTITY_INSERT nilai OFF;

-- Hapus temporary table
DROP TABLE #TempNIM;

-- Tampilkan jumlah data akhir di tabel
SELECT COUNT(*) AS TotalData FROM nilai;
