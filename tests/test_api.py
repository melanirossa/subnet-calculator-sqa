import pytest
from fastapi.testclient import TestClient

from subnet_calculator_sqa.api import app

client = TestClient(app)


@pytest.mark.parametrize(
    ("ip", "prefix", "expected"),
    [
        (
            "172.16.5.130",
            25,
            {
                "mask": "255.255.255.128",
                "network": "172.16.5.128",
                "broadcast": "172.16.5.255",
                "first_host": "172.16.5.129",
                "last_host": "172.16.5.254",
                "usable_hosts": 126,
            },
        ),
        (
            "192.168.1.0",
            31,
            {
                "mask": "255.255.255.254",
                "network": "192.168.1.0",
                "broadcast": None,
                "first_host": "192.168.1.0",
                "last_host": "192.168.1.1",
                "usable_hosts": 2,
            },
        ),
        (
            "192.168.1.5",
            32,
            {
                "mask": "255.255.255.255",
                "network": "192.168.1.5",
                "broadcast": None,
                "first_host": "192.168.1.5",
                "last_host": "192.168.1.5",
                "usable_hosts": 1,
            },
        ),
    ],
)
def test_api_subnet_sukses(ip, prefix, expected):
    response = client.get(
        "/api/subnet",
        params={"ip": ip, "prefix": prefix},
    )

    assert response.status_code == 200
    assert response.json() == expected


@pytest.mark.parametrize(
    ("params",),
    [
        ({"ip": "256.1.1.1", "prefix": 24},),
        ({"ip": "192.168.01.1", "prefix": 24},),
        ({"ip": " 192.168.1.1 ", "prefix": 24},),
        ({"ip": "10.0.0.1", "prefix": 33},),
        ({"ip": "10.0.0.1", "prefix": -1},),
        ({"ip": "10.0.0.1", "prefix": "abc"},),
        ({"ip": "10.0.0.1"},),
        ({"prefix": 24},),
        ({},),
    ],
)
def test_api_input_tidak_valid_mengembalikan_400_detail(params):
    response = client.get("/api/subnet", params=params)

    assert response.status_code == 400
    assert isinstance(response.json().get("detail"), str)
    assert response.json()["detail"]


def test_api_root_mengembalikan_halaman_html():
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Kalkulator Subnet" in response.text


def test_api_vlsm_sukses():
    response = client.post(
        "/api/vlsm",
        json={
            "network": "192.168.1.0/24",
            "kebutuhan_host": [100, 50, 20, 2],
        },
    )

    assert response.status_code == 200
    hasil = response.json()
    assert [blok["network_cidr"] for blok in hasil] == [
        "192.168.1.0/25",
        "192.168.1.128/26",
        "192.168.1.192/27",
        "192.168.1.224/30",
    ]
    assert [blok["usable_hosts"] for blok in hasil] == [126, 62, 30, 2]


@pytest.mark.parametrize(
    "body",
    [
        {"network": "192.168.1.5/24", "kebutuhan_host": [10]},
        {"network": "192.168.1.0/24", "kebutuhan_host": []},
        {"network": "192.168.1.0/24", "kebutuhan_host": [0]},
        {"network": "192.168.1.0/24", "kebutuhan_host": [200, 100]},
        {"network": "192.168.1.0/24", "kebutuhan_host": [True]},
        {},
    ],
)
def test_api_vlsm_input_tidak_valid_mengembalikan_400_detail(body):
    response = client.post("/api/vlsm", json=body)

    assert response.status_code == 400
    assert isinstance(response.json().get("detail"), str)
    assert response.json()["detail"]


@pytest.mark.parametrize(
    "content",
    ["{", "[]"],
)
def test_api_vlsm_body_bukan_objek_json_valid_mengembalikan_400_detail(content):
    response = client.post(
        "/api/vlsm",
        content=content,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 400
    assert isinstance(response.json().get("detail"), str)
    assert response.json()["detail"]
