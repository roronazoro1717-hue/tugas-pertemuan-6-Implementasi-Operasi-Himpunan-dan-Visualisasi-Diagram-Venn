# Sistem Klasifikasi Data dengan Himpunan (PJBL-2)

Operasi himpunan (union, intersection, difference, complement), Diagram Venn otomatis (2-3 himpunan), dan Prinsip Inklusi-Eksklusi (PIE).

## Cara pakai
    pip install -r requirements.txt
    python klasifikasi_himpunan.py --demo
    python klasifikasi_himpunan.py --data data/dataset1_keahlian_mahasiswa.csv --op union --sets Desain Programming
    python klasifikasi_himpunan.py --data data/dataset1_keahlian_mahasiswa.csv --pie --sets Desain Programming Video --venn output/venn.png
    python test_himpunan.py

Format dataset CSV: id,nama,kategori (kategori dipisah titik koma).

## Pembagian kontribusi
- [Nama 1]: operasi himpunan + tes
- [Nama 2]: Diagram Venn
- [Nama 3]: PIE, dataset, dokumentasi
