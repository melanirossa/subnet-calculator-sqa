# Spesifikasi Kalkulator Subnet & VLSM

## Tujuan

Kalkulator ini membantu guru dan siswa SMK TKJ memeriksa perhitungan subnet IPv4 dan alokasi VLSM. Hasil ditampilkan dengan istilah dan angka yang dapat diverifikasi tanpa membaca kode.

Aplikasi menggunakan Python 3.12, FastAPI, dan satu halaman HTML. Struktur `src/` dan `tests/` yang sudah ada dipertahankan:

- Logika subnet: `src/subnet_calculator_sqa/subnet.py`
- Logika VLSM: `src/subnet_calculator_sqa/vlsm.py`
- Aplikasi dan endpoint FastAPI: `src/subnet_calculator_sqa/api.py`
- Halaman web: `index.html` di root proyek
- Test: direktori `tests/`

## Aturan Validasi

### Alamat IPv4 dan prefix

- Alamat IPv4 harus berupa tepat empat oktet desimal, masing-masing `0` sampai `255`.
- Oktet tidak boleh memiliki nol di depan, kecuali nilai oktet itu sendiri adalah `0`. Contoh `192.168.01.1` tidak valid.
- Spasi di awal, akhir, atau di dalam alamat tidak diperbolehkan.
- Prefix harus bilangan bulat dari `0` sampai `32`.
- Boolean tidak dianggap sebagai bilangan bulat yang valid untuk prefix atau kebutuhan host.
- Input yang tidak valid pada fungsi logika menghasilkan `ValueError` atau turunannya.

### Network VLSM

- `network_cidr` harus berisi alamat IPv4 network yang canonical dan prefix valid.
- Alamat dengan host bits menyala bukan network input yang valid. Contoh `192.168.1.5/24` ditolak; gunakan `192.168.1.0/24`.
- Daftar kebutuhan host harus berisi minimal satu nilai.
- Setiap kebutuhan host harus berupa bilangan bulat positif.
- VLSM mencadangkan alamat network dan broadcast pada setiap subnet; karena itu ukuran blok harus dapat memuat kebutuhan host ditambah dua alamat.
- Ukuran blok minimum adalah 4 alamat (`/30`). Prefix `/31` dan `/32` tidak digunakan untuk alokasi VLSM.
- Jika seluruh subnet tidak muat dalam pool, seluruh permintaan ditolak; hasil parsial tidak dikembalikan.

## Kontrak Fungsi

Nama fungsi subnet `calculate` dipertahankan agar sesuai dengan kode dan pemanggil yang sudah ada. Secara perilaku fungsi ini memenuhi peran `hitung_subnet` dalam alur awal.

### `calculate(ip: str, prefix: int) -> dict`

Menghasilkan tepat kunci berikut:

| Kunci | Tipe | Arti |
|---|---|---|
| `mask` | `str` | Subnet mask dalam dotted decimal |
| `network` | `str` | Network address |
| `broadcast` | `str` atau `None` | Broadcast address; `None` untuk `/31` dan `/32` |
| `first_host` | `str` | Alamat host usable pertama |
| `last_host` | `str` | Alamat host usable terakhir |
| `usable_hosts` | `int` | Jumlah alamat host usable |

Aturan per prefix:

- `/0` sampai `/30`: `usable_hosts = 2 ** (32 - prefix) - 2`; `first_host` adalah network + 1 dan `last_host` adalah broadcast - 1.
- `/31`: mengikuti aturan point-to-point RFC 3021; kedua alamat dapat dipakai, `usable_hosts = 2`, `first_host` adalah network, `last_host` adalah alamat berikutnya, dan `broadcast = None`.
- `/32`: satu alamat dapat dipakai; `usable_hosts = 1`, `first_host = last_host = ip`, dan `broadcast = None`.
- Network address dihitung berdasarkan IP AND subnet mask.
- IP yang valid tetapi memiliki host bits menyala tetap menghasilkan network sesuai prefix.

### `alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]`

- Mengurutkan kebutuhan dari terbesar ke terkecil.
- Jika beberapa kebutuhan sama besar, urutan input dipertahankan.
- Mengalokasikan blok berurutan dari alamat network terendah yang tersedia.
- Memilih ukuran blok pangkat dua terkecil yang memenuhi `kebutuhan_host + 2`, dengan minimum 4 alamat.
- Setiap elemen hasil memuat `kebutuhan`, `network_cidr`, serta seluruh kunci hasil `calculate`.
- Hasil berurutan menurut alokasi subnet, yaitu dari kebutuhan terbesar. Tidak ada blok yang tumpang tindih.
- Menghasilkan error jika input tidak valid atau kapasitas pool tidak mencukupi.

## Kontrak API

### `GET /api/subnet?ip=&prefix=`

- Memanggil fungsi subnet dan mengembalikan objek JSON dengan kunci hasil `calculate`.
- Input valid menghasilkan HTTP `200`.
- Input tidak valid, termasuk parameter hilang atau tidak dapat dikonversi, menghasilkan HTTP `400` dengan objek JSON yang memiliki field `detail` berisi pesan yang dapat dibaca.

### `POST /api/vlsm`

Body JSON:

```json
{
  "network": "192.168.1.0/24",
  "kebutuhan_host": [100, 50, 20, 2]
}
```

- Input valid menghasilkan HTTP `200` dan array objek hasil alokasi.
- Input tidak valid atau pool tidak cukup menghasilkan HTTP `400` dengan field `detail`.

### `GET /`

- Mengembalikan halaman `index.html`.
- Halaman tersedia menghasilkan HTTP `200` dengan konten HTML.

## Halaman Web

- Satu halaman berbahasa Indonesia dengan dua mode: **Subnet** dan **VLSM**.
- Mode Subnet memiliki field alamat IPv4, prefix `0–32`, dan tombol hitung.
- Mode VLSM memiliki field network CIDR, daftar kebutuhan host, serta kontrol tambah dan hapus kebutuhan.
- Hasil Subnet menampilkan mask, network, broadcast, first host, last host, dan usable hosts.
- Hasil VLSM ditampilkan sebagai tabel alokasi subnet.
- Mendukung tiga keadaan tampilan: kosong, berhasil, dan error.
- Pesan error ditampilkan dekat input yang bermasalah dan tetap jelas dibaca.
- Halaman responsif untuk desktop dan perangkat seluler.
- Halaman tidak menyimpan data pengguna.

## Tabel Test Case

### Fungsi subnet

| Kasus | Input | Hasil yang diharapkan |
|---|---|---|
| Prefix `/25` | `172.16.5.130`, prefix `25` | Mask `255.255.255.128`; network `172.16.5.128`; broadcast `172.16.5.255`; first `172.16.5.129`; last `172.16.5.254`; usable `126` |
| Prefix `/30` | `10.0.0.0`, prefix `30` | Network `10.0.0.0`; broadcast `10.0.0.3`; first `10.0.0.1`; last `10.0.0.2`; usable `2` |
| Prefix `/0` | `1.2.3.4`, prefix `0` | Network `0.0.0.0`; broadcast `255.255.255.255`; usable `4294967294` |
| Prefix `/31` | `192.168.1.0`, prefix `31` | Network `192.168.1.0`; broadcast `None`; first `192.168.1.0`; last `192.168.1.1`; usable `2` |
| Prefix `/32` | `192.168.1.5`, prefix `32` | Network `192.168.1.5`; broadcast `None`; first dan last `192.168.1.5`; usable `1` |
| Oktet di luar rentang | `256.1.1.1`, prefix `24` | Ditolak |
| Nol di depan | `192.168.01.1`, prefix `24` | Ditolak |
| IPv4 tidak lengkap | `192.168.1`, prefix `24` | Ditolak |
| Teks, alamat kosong, atau spasi | `abc`, `""`, atau `" 192.168.1.1 "`, prefix `24` | Ditolak |
| Prefix di luar batas | Prefix `-1` atau `33` | Ditolak |
| Prefix bukan integer | Prefix `24.5` | Ditolak |

### Fungsi VLSM

| Kasus | Input | Hasil yang diharapkan |
|---|---|---|
| Alokasi bertingkat | Pool `192.168.1.0/24`, kebutuhan `[100, 50, 20, 2]` | Berurutan: `192.168.1.0/25` (126 usable), `192.168.1.128/26` (62), `192.168.1.192/27` (30), `192.168.1.224/30` (2) |
| Kapasitas tidak cukup | Pool `192.168.1.0/24`, kebutuhan `[200, 100]` | Ditolak; kedua kebutuhan tidak dapat dialokasikan seluruhnya |
| Daftar kosong | Pool `192.168.1.0/24`, kebutuhan `[]` | Ditolak |
| Kebutuhan nol atau negatif | Pool `192.168.1.0/24`, kebutuhan `[0]` atau `[-1]` | Ditolak |
| Pool bukan network canonical | `192.168.1.5/24`, kebutuhan `[10]` | Ditolak |

### Endpoint

| Kasus | Permintaan | Hasil yang diharapkan |
|---|---|---|
| Halaman utama | `GET /` | HTTP `200`, konten HTML |
| Subnet valid | `GET /api/subnet?ip=172.16.5.130&prefix=25` | HTTP `200`, nilai network dan usable hosts sesuai tabel fungsi |
| Subnet invalid | `GET /api/subnet?ip=256.1.1.1&prefix=24` | HTTP `400`, JSON memiliki field `detail` |
| VLSM valid | `POST /api/vlsm` dengan contoh alokasi bertingkat | HTTP `200`, urutan dan CIDR sesuai tabel fungsi |
| VLSM invalid | `POST /api/vlsm` dengan kebutuhan yang tidak muat | HTTP `400`, JSON memiliki field `detail` |

## Di Luar Cakupan

- IPv6.
- Penyimpanan atau riwayat perhitungan.
- Akun pengguna dan autentikasi.
- Konfigurasi perangkat jaringan atau pemindaian jaringan.
- Perubahan arsitektur proyek dari `src/` dan `tests/` ke modul di root.
- Detail build Docker dan konfigurasi runtime Vercel; keduanya dibahas pada tahap deployment dan dokumentasi terkait.
