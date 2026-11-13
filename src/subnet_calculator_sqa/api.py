import re
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse

from subnet_calculator_sqa.subnet import SubnetError, calculate

app = FastAPI(title="Subnet Calculator")
INDEX_HTML = Path(__file__).resolve().parents[2] / "index.html"


@app.get("/api/subnet")
def subnet(ip: str | None = Query(None), prefix: str | None = Query(None)):
    if ip is None or prefix is None:
        raise HTTPException(status_code=400, detail="Parameter ip dan prefix wajib diisi.")

    try:
        if re.fullmatch(r"(?:0|[1-9][0-9]*)", prefix) is None:
            raise SubnetError("Prefix harus berupa bilangan bulat dari 0 sampai 32.")
        return calculate(ip, int(prefix))
    except SubnetError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/")
def home():
    return FileResponse(INDEX_HTML, media_type="text/html")


@app.post("/api/vlsm")
def vlsm(body: dict[str, object]):
    raise HTTPException(status_code=501, detail="VLSM belum diimplementasikan.")