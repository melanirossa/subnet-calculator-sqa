import pytest

from subnet_calculator_sqa.subnet import SubnetError, calculate


def test_slash_26():
    r = calculate("192.168.10.77", 26)
    assert r["network"] == "192.168.10.64"
    assert r["broadcast"] == "192.168.10.127"
    assert r["first_host"] == "192.168.10.65"
    assert r["last_host"] == "192.168.10.126"
    assert r["usable_hosts"] == 62


def test_slash_24():
    r = calculate("192.168.1.10", 24)
    assert r["network"] == "192.168.1.0"
    assert r["broadcast"] == "192.168.1.255"
    assert r["usable_hosts"] == 254
    assert r["netmask"] == "255.255.255.0"
    assert r["wildcard"] == "0.0.0.255"


def test_slash_30():
    r = calculate("10.0.0.5", 30)
    assert (r["network"], r["broadcast"]) == ("10.0.0.4", "10.0.0.7")
    assert (r["first_host"], r["last_host"]) == ("10.0.0.5", "10.0.0.6")
    assert r["usable_hosts"] == 2


def test_slash_31_point_to_point():
    r = calculate("10.0.0.0", 31)
    assert (r["first_host"], r["last_host"]) == ("10.0.0.0", "10.0.0.1")
    assert r["usable_hosts"] == 2


def test_slash_32_single_host():
    r = calculate("10.0.0.9", 32)
    assert r["network"] == r["broadcast"] == r["first_host"] == r["last_host"] == "10.0.0.9"
    assert r["usable_hosts"] == 1


def test_slash_0():
    r = calculate("1.2.3.4", 0)
    assert r["network"] == "0.0.0.0"
    assert r["total_addresses"] == 2**32
    assert r["usable_hosts"] == 2**32 - 2


@pytest.mark.parametrize("ip", ["256.1.1.1", "1.2.3", "abc", "", "1.2.3.4.5"])
def test_ip_tidak_valid(ip):
    with pytest.raises(SubnetError):
        calculate(ip, 24)


@pytest.mark.parametrize("prefix", [-1, 33, 100])
def test_prefix_tidak_valid(prefix):
    with pytest.raises(SubnetError):
        calculate("10.0.0.1", prefix)