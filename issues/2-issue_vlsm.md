# [Feature] Alokasi VLSM

## Deskripsi

Tambahkan alokasi VLSM agar guru dan siswa SMK TKJ dapat membagi satu network IPv4 menjadi subnet sesuai kebutuhan host. Urutan alokasi, ukuran blok, validasi, dan hasil harus mengikuti `SPEC.md`.

Implementasi mengikuti struktur proyek yang sudah ada:

- Logika VLSM: `src/subnet_calculator_sqa/vlsm.py`
- Endpoint: `src/subnet_calculator_sqa/api.py`
- Test: direktori `tests/`
- Antarmuka: `index.html`

## Tugas

- Tulis test VLSM dan API terlebih dahulu berdasarkan `SPEC.md`.
- Implementasikan `alokasi_vlsm(network_cidr, kebutuhan_host)` dengan alokasi terbesar lebih dahulu dan urutan input stabil untuk kebutuhan yang sama besar.
- Tolak network CIDR yang tidak canonical, daftar kosong, kebutuhan host tidak positif, dan permintaan yang tidak muat dalam pool.
- Tambahkan `POST /api/vlsm` dengan body `{ "network": "...", "kebutuhan_host": [...] }`.
- Kembalikan HTTP 400 dan field JSON `detail` untuk input tidak valid atau kapasitas pool tidak cukup.
- Hubungkan mode VLSM pada `index.html`, termasuk kontrol tambah/hapus kebutuhan dan tabel hasil.

## Kriteria Penerimaan

- Semua test VLSM dan endpoint pada bagian **Tabel Test Case** di `SPEC.md` lulus.
- Pool `192.168.1.0/24` dengan kebutuhan `[100, 50, 20, 2]` menghasilkan urutan:
  - `192.168.1.0/25` dengan 126 host usable.
  - `192.168.1.128/26` dengan 62 host usable.
  - `192.168.1.192/27` dengan 30 host usable.
  - `192.168.1.224/30` dengan 2 host usable.
- Kebutuhan diurutkan menurun; kebutuhan yang sama besar mempertahankan urutan masukan.
- Tidak ada subnet yang tumpang tindih dan tidak ada alokasi di luar pool.
- Pool yang tidak cukup, kebutuhan kosong/nol/negatif, dan network CIDR yang tidak canonical ditolak.
- Endpoint mengembalikan HTTP 200 untuk alokasi valid dan HTTP 400 dengan field `detail` untuk input tidak valid.
- Mode VLSM menampilkan hasil dalam tabel serta pesan error yang jelas.
- Test ditulis sebelum implementasi dan tidak diubah hanya untuk membuat implementasi lulus.

## Alur Kerja

Issue -> branch dari `main` terbaru -> tulis test terlebih dahulu -> buat kerangka yang gagal -> jalankan test merah -> implementasi -> jalankan seluruh test -> commit -> pull request -> CI hijau -> merge.
