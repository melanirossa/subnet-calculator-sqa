from fastapi.testclient import TestClient

from subnet_calculator_sqa.api import app

client = TestClient(app)


def test_api_sukses():
    r = client.get("/api/subnet", params={"ip": "192.168.10.77", "prefix": 26})
    assert r.status_code == 200
    body = r.json()
    assert body["network"] == "192.168.10.64"
    assert body["usable_hosts"] == 62


def test_api_ip_salah():
    r = client.get("/api/subnet", params={"ip": "999.1.1.1", "prefix": 24})
    assert r.status_code == 422


def test_api_prefix_di_luar_range():
    r = client.get("/api/subnet", params={"ip": "10.0.0.1", "prefix": 33})
    assert r.status_code == 422


def test_api_prefix_bukan_angka():
    r = client.get("/api/subnet", params={"ip": "10.0.0.1", "prefix": "abc"})
    assert r.status_code == 422


def test_api_parameter_hilang():
    assert client.get("/api/subnet").status_code == 422