# Image dasar: Python 3.12 versi ramping
FROM python:3.12-slim

# Salin program uv dari image resminya (versi dikunci agar hasil build selalu sama)
COPY --from=ghcr.io/astral-sh/uv:0.11.32 /uv /uvx /bin/

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Pasang dependency dulu (lapisan ini di-cache selama uv.lock tidak berubah)
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-dev --no-install-project

# Salin kode aplikasi dari layout src/ proyek ini
COPY src ./src
COPY index.html ./

# Layanan hosting biasanya mengisi variabel PORT; di laptop dipakai 8000
ENV PORT=8000
EXPOSE 8000
CMD ["sh", "-c", "/app/.venv/bin/uvicorn subnet_calculator_sqa.api:app --app-dir /app/src --host 0.0.0.0 --port ${PORT}"]
