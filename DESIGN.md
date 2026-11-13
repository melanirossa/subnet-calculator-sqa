# Rancangan UI Kalkulator Subnet & VLSM

## Sasaran

Antarmuka ditujukan untuk guru dan siswa SMK TKJ. Prioritasnya adalah label yang jelas, hasil yang mudah diperiksa, dan pesan kesalahan yang membantu memperbaiki input.

## Arah Visual

- Tema terang, latar putih, permukaan kartu abu-abu sangat muda.
- Aksen biru untuk tombol utama, tab aktif, fokus, dan tautan.
- Tipografi sans-serif sistem agar cepat dimuat dan mudah dibaca.
- Kartu dengan sudut membulat, garis pembatas halus, dan ruang antarbagian yang cukup.
- Tidak menggunakan animasi yang mengganggu atau elemen dekoratif yang menutupi hasil.

## Struktur Halaman

1. Header dengan nama aplikasi dan deskripsi singkat.
2. Navigasi dua mode: **Subnet** dan **VLSM**.
3. Form input sesuai mode aktif.
4. Area hasil yang menampilkan data dalam urutan tetap.
5. Area pesan error dekat input terkait.

### Mode Subnet

- Input alamat IPv4 dan prefix dalam field terpisah.
- Prefix memiliki petunjuk rentang `0–32`.
- Tombol aksi utama berlabel **Hitung subnet**.
- Hasil ditampilkan dalam kartu berlabel: Mask, Network, Broadcast, First host, Last host, dan Host usable.
- Nilai hasil menggunakan font monospace agar alamat IP mudah dibandingkan.

### Mode VLSM

- Input network CIDR.
- Daftar kebutuhan host dengan satu input bilangan bulat per baris.
- Tombol tambah dan hapus kebutuhan.
- Tombol aksi utama berlabel **Alokasikan VLSM**.
- Hasil berupa tabel dengan kolom: kebutuhan host, network CIDR, mask, broadcast, rentang host, dan host usable.
- Tabel dapat digulir horizontal pada layar kecil tanpa memotong nilai.

## Keadaan Antarmuka

- **Kosong:** form siap diisi dan area hasil menampilkan petunjuk singkat; tidak ada hasil contoh yang dapat disalahartikan sebagai hasil pengguna.
- **Berhasil:** hasil muncul setelah form; label dan nilai tetap berpasangan serta mudah dibaca.
- **Error:** pesan singkat muncul dekat input yang bermasalah. Pesan menyebut koreksi yang diperlukan, bukan hanya “terjadi kesalahan”.

## Responsif dan Aksesibilitas

- Desktop menggunakan konten terpusat dengan lebar yang nyaman dibaca.
- Mobile menggunakan satu kolom; form, tombol, dan hasil memenuhi lebar layar yang tersedia.
- Setiap input memiliki label yang terlihat, bukan hanya placeholder.
- Urutan fokus mengikuti urutan visual; fokus keyboard terlihat jelas.
- Status error dan hasil dapat dikenali tanpa hanya mengandalkan warna.
- Tabel memiliki header kolom yang jelas; halaman mendukung pembesaran teks.

## Implementasi

Mode Subnet pada `index.html` memanggil `GET /api/subnet`; mode VLSM menyediakan kontrol tambah/hapus kebutuhan, mengirim alokasi ke `POST /api/vlsm`, dan menampilkan hasil API sebagai tabel. Kedua mode menampilkan pesan error dari API pada halaman.
