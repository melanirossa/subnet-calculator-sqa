import ipaddress
import re

from subnet_calculator_sqa.subnet import calculate

_NETWORK_CIDR_RE = re.compile(
    r"((?:0|[1-9][0-9]{0,2})(?:\.(?:0|[1-9][0-9]{0,2})){3})/([0-9]+)"
)


def alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]:
    if not isinstance(network_cidr, str):
        raise ValueError("Network harus berupa IPv4 CIDR.")

    match = _NETWORK_CIDR_RE.fullmatch(network_cidr)
    if match is None:
        raise ValueError("Network harus berupa IPv4 CIDR tanpa spasi atau nol di depan.")

    address, prefix_text = match.groups()
    octets = [int(octet) for octet in address.split(".")]
    if any(octet > 255 for octet in octets):
        raise ValueError("Setiap oktet alamat IPv4 harus bernilai 0 sampai 255.")

    prefix = int(prefix_text)
    if not 0 <= prefix <= 32:
        raise ValueError("Prefix network harus berupa bilangan bulat dari 0 sampai 32.")

    try:
        pool = ipaddress.IPv4Network(network_cidr, strict=True)
    except ValueError as exc:
        raise ValueError("Network CIDR harus merupakan alamat network yang canonical.") from exc

    if not isinstance(kebutuhan_host, list) or not kebutuhan_host:
        raise ValueError("Daftar kebutuhan host tidak boleh kosong.")

    for kebutuhan in kebutuhan_host:
        if (
            isinstance(kebutuhan, bool)
            or not isinstance(kebutuhan, int)
            or kebutuhan < 1
        ):
            raise ValueError("Setiap kebutuhan host harus berupa bilangan bulat positif.")
        if kebutuhan + 2 > pool.num_addresses:
            raise ValueError("Kebutuhan host tidak muat dalam network yang diberikan.")

    current_address = int(pool.network_address)
    pool_last_address = int(pool.broadcast_address)
    hasil = []

    for kebutuhan in sorted(kebutuhan_host, reverse=True):
        required_addresses = kebutuhan + 2
        block_size = max(4, 1 << (required_addresses - 1).bit_length())
        host_bits = block_size.bit_length() - 1
        subnet_prefix = 32 - host_bits

        subnet_address = (current_address + block_size - 1) & ~(block_size - 1)
        subnet_last_address = subnet_address + block_size - 1
        if subnet_last_address > pool_last_address:
            raise ValueError("Seluruh subnet tidak muat dalam network yang diberikan.")

        subnet = ipaddress.IPv4Network((subnet_address, subnet_prefix))
        hasil.append(
            {
                "kebutuhan": kebutuhan,
                "network_cidr": str(subnet),
                **calculate(str(subnet.network_address), subnet.prefixlen),
            }
        )
        current_address = subnet_last_address + 1

    return hasil
