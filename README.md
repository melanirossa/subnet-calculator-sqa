## Docker

Build image dari root proyek:

```sh
docker build -t subnet-calculator .
```

Jalankan container di port `8000`:

```sh
docker run -d --name subnet-app -p 8000:8000 subnet-calculator
```

Verifikasi halaman, kalkulator subnet, validasi input, dan alokasi VLSM:

```sh
uv run python scripts/smoke_test.py http://127.0.0.1:8000
```

Lihat log aplikasi atau hentikan dan hapus container setelah selesai:

```sh
docker logs subnet-app
docker rm -f subnet-app
```