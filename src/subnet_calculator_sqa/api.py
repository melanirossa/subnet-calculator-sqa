from fastapi import FastAPI, HTTPException, Query

from subnet_calculator_sqa.subnet import SubnetError, calculate

app = FastAPI(title="Subnet Calculator")


@app.get("/api/subnet")
def subnet(ip: str, prefix: int = Query(..., ge=0, le=32)):
    try:
        return calculate(ip, prefix)
    except SubnetError as e:
        raise HTTPException(status_code=422, detail=str(e))