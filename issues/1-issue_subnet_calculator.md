# [Feature] Kalkulator Subnet

## Deskripsi

Bangun dan rapikan mode kalkulator subnet IPv4 agar guru dan siswa SMK TKJ dapat memeriksa hasil subnetting melalui halaman web dan API. Hasil serta aturan validasi harus mengikuti `SPEC.md`.

Proyek ini sudah memiliki kode dan test di bawah `src/subnet_calculator_sqa/` dan `tests/`. Implementasi harus mempertahankan struktur tersebut dan menyelaraskan perilaku yang ada dengan spesifikasi, bukan memindahkan modul ke root.

## Tugas

- Selaraskan fungsi subnet yang sudah ada dengan kontrak pada `SPEC.md`.
- Pastikan validasi IPv4 dan prefix mengikuti aturan spesifikasi, termasuk penolakan spasi dan oktet dengan nol di depan.
- Sajikan hasil subnet melalui `GET /api/subnet`; input tidak valid harus mengembalikan HTTP 400 dan field JSON `detail`.
- Sajikan halaman `index.html` melalui `GET /`.
- Hubungkan mode Subnet pada halaman web ke endpoint API dan tampilkan hasil serta pesan error yang mudah dipahami.
- Pertahankan dukungan RFC 3021 untuk `/31` dan aturan satu alamat untuk `/32` sesuai keputusan dalam `SPEC.md`.
- Tambahkan atau sesuaikan test lebih dahulu di direktori `tests/`, mencakup kasus subnet dan API pada `SPEC.md`.

## Kriteria Penerimaan

- Semua test subnet dan endpoint yang relevan di bagian **Tabel Test Case** pada `SPEC.md` lulus.
- `172.16.5.130/25` menghasilkan network `172.16.5.128`, broadcast `172.16.5.255`, rentang host `172.16.5.129–172.16.5.254`, dan 126 host usable.
- `10.0.0.0/30` menghasilkan network `10.0.0.0`, broadcast `10.0.0.3`, rentang host `10.0.0.1–10.0.0.2`, dan 2 host usable.
- `/31` dan `/32` mengikuti nilai broadcast dan jumlah host yang ditetapkan pada `SPEC.md`.
- Input IPv4 atau prefix yang tidak valid ditolak oleh fungsi dan API; API mengembalikan HTTP 400 dengan field `detail`.
- `GET /` mengembalikan halaman HTML dengan HTTP 200.
- Mode Subnet menampilkan keadaan kosong, hasil berhasil, dan pesan error tanpa mengubah perhitungan yang ditetapkan.
- Test ditulis sebelum implementasi diperbaiki. Test tidak diubah hanya untuk membuat implementasi lulus.
- Implementasi dan test tetap berada pada struktur `src/` dan `tests/` proyek.

## Di Luar Cakupan

- Implementasi alokasi VLSM dan endpoint `POST /api/vlsm`; dikerjakan pada issue fitur VLSM berikutnya.
- CI, Docker, dan deployment Vercel; dikerjakan pada tahap berikutnya sesuai `PROMPT-INTEGRATE.md`.

## Alur Kerja

Issue -> branch dari `main` -> tulis/rapikan test terlebih dahulu -> implementasi -> jalankan seluruh test -> commit -> pull request -> CI hijau -> merge.
