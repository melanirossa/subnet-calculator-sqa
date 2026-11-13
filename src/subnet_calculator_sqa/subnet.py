import ipaddress
import re


class SubnetError(ValueError):
    """Dilempar saat input IP atau prefix tidak valid."""


def calculate(ip: str, prefix: int) -> dict:
    if isinstance(prefix, bool) or not isinstance(prefix, int) or not 0 <= prefix <= 32:
        raise SubnetError("Prefix harus berupa angka 0 sampai 32.")

    if not isinstance(ip, str) or re.fullmatch(
        r"(?:0|[1-9][0-9]{0,2})(?:\.(?:0|[1-9][0-9]{0,2})){3}",
        ip,
    ) is None:
        raise SubnetError("Alamat IP harus berupa IPv4 tanpa spasi atau nol di depan.")

    octets = [int(octet) for octet in ip.split(".")]
    if any(octet > 255 for octet in octets):
        raise SubnetError("Setiap oktet alamat IPv4 harus bernilai 0 sampai 255.")

    ip_value = int(ipaddress.IPv4Address(ip))
    mask_value = 0 if prefix == 0 else (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    network_value = ip_value & mask_value
    network = ipaddress.IPv4Address(network_value)
    mask = ipaddress.IPv4Address(mask_value)

    if prefix == 32:
        first = last = network
        broadcast = None
        usable = 1
    elif prefix == 31:
        first = network
        last = ipaddress.IPv4Address(network_value + 1)
        broadcast = None
        usable = 2
    else:
        broadcast_value = network_value | (~mask_value & 0xFFFFFFFF)
        broadcast = ipaddress.IPv4Address(broadcast_value)
        first = ipaddress.IPv4Address(network_value + 1)
        last = ipaddress.IPv4Address(broadcast_value - 1)
        usable = (1 << (32 - prefix)) - 2

    return {
        "mask": str(mask),
        "network": str(network),
        "broadcast": str(broadcast) if broadcast is not None else None,
        "first_host": str(first),
        "last_host": str(last),
        "usable_hosts": usable,
    }