import pytest

from subnet_calculator_sqa.vlsm import alokasi_vlsm


def test_alokasi_vlsm_mengurutkan_dan_mengembalikan_detail_subnet():
    hasil = alokasi_vlsm("192.168.1.0/24", [100, 50, 20, 2])

    assert hasil == [
        {
            "kebutuhan": 100,
            "network_cidr": "192.168.1.0/25",
            "mask": "255.255.255.128",
            "network": "192.168.1.0",
            "broadcast": "192.168.1.127",
            "first_host": "192.168.1.1",
            "last_host": "192.168.1.126",
            "usable_hosts": 126,
        },
        {
            "kebutuhan": 50,
            "network_cidr": "192.168.1.128/26",
            "mask": "255.255.255.192",
            "network": "192.168.1.128",
            "broadcast": "192.168.1.191",
            "first_host": "192.168.1.129",
            "last_host": "192.168.1.190",
            "usable_hosts": 62,
        },
        {
            "kebutuhan": 20,
            "network_cidr": "192.168.1.192/27",
            "mask": "255.255.255.224",
            "network": "192.168.1.192",
            "broadcast": "192.168.1.223",
            "first_host": "192.168.1.193",
            "last_host": "192.168.1.222",
            "usable_hosts": 30,
        },
        {
            "kebutuhan": 2,
            "network_cidr": "192.168.1.224/30",
            "mask": "255.255.255.252",
            "network": "192.168.1.224",
            "broadcast": "192.168.1.227",
            "first_host": "192.168.1.225",
            "last_host": "192.168.1.226",
            "usable_hosts": 2,
        },
    ]


def test_kebutuhan_sama_besar_mempertahankan_urutan_input():
    hasil = alokasi_vlsm("192.168.1.0/24", [10, 10])

    assert [blok["network_cidr"] for blok in hasil] == [
        "192.168.1.0/28",
        "192.168.1.16/28",
    ]


@pytest.mark.parametrize(
    ("network_cidr", "kebutuhan_host"),
    [
        ("192.168.1.5/24", [10]),
        ("192.168.1.0/33", [10]),
        ("abc", [10]),
    ],
)
def test_network_cidr_tidak_valid(network_cidr, kebutuhan_host):
    with pytest.raises(ValueError):
        alokasi_vlsm(network_cidr, kebutuhan_host)


@pytest.mark.parametrize("kebutuhan_host", [[], [0], [-1], [True], [1.5], ["2"]])
def test_kebutuhan_host_tidak_valid(kebutuhan_host):
    with pytest.raises(ValueError):
        alokasi_vlsm("192.168.1.0/24", kebutuhan_host)


def test_alokasi_ditolak_jika_seluruh_kebutuhan_tidak_muat():
    with pytest.raises(ValueError):
        alokasi_vlsm("192.168.1.0/24", [200, 100])
