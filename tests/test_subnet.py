import pytest

from subnet_calculator_sqa.subnet import calculate


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
            "10.0.0.0",
            30,
            {
                "mask": "255.255.255.252",
                "network": "10.0.0.0",
                "broadcast": "10.0.0.3",
                "first_host": "10.0.0.1",
                "last_host": "10.0.0.2",
                "usable_hosts": 2,
            },
        ),
        (
            "1.2.3.4",
            0,
            {
                "mask": "0.0.0.0",
                "network": "0.0.0.0",
                "broadcast": "255.255.255.255",
                "first_host": "0.0.0.1",
                "last_host": "255.255.255.254",
                "usable_hosts": 4294967294,
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
def test_calculate_matches_spec(ip, prefix, expected):
    assert calculate(ip, prefix) == expected


@pytest.mark.parametrize(
    "ip",
    [
        "256.1.1.1",
        "1.2.3",
        "abc",
        "",
        "1.2.3.4.5",
        "192.168.01.1",
        " 192.168.1.1",
        "192.168.1.1 ",
        "192.168. 1.1",
    ],
)
def test_ip_tidak_valid(ip):
    with pytest.raises(ValueError):
        calculate(ip, 24)


@pytest.mark.parametrize("prefix", [-1, 33, 100, 24.5, True])
def test_prefix_tidak_valid(prefix):
    with pytest.raises(ValueError):
        calculate("10.0.0.1", prefix)


def test_ip_dengan_host_bits_menghasilkan_network_canonical():
    result = calculate("172.16.5.130", 25)

    assert result["network"] == "172.16.5.128"
