import ipaddress


class SubnetError(ValueError):
    """Dilempar saat input IP atau prefix tidak valid."""


def calculate(ip: str, prefix: int) -> dict:
    if isinstance(prefix, bool) or not isinstance(prefix, int) or not 0 <= prefix <= 32:
        raise SubnetError("Prefix harus berupa angka 0 sampai 32.")

    try:
        addr = ipaddress.IPv4Address(ip.strip())
    except ipaddress.AddressValueError:
        raise SubnetError("Alamat IP tidak valid.")

    net = ipaddress.IPv4Network((addr, prefix), strict=False)
    total = net.num_addresses

    if prefix == 32:
        first = last = net.network_address
        usable = 1
    elif prefix == 31:
        first, last = net.network_address, net.broadcast_address
        usable = 2
    else:
        first = net.network_address + 1
        last = net.broadcast_address - 1
        usable = total - 2

    return {
        "ip": str(addr),
        "prefix": prefix,
        "network": str(net.network_address),
        "broadcast": str(net.broadcast_address),
        "netmask": str(net.netmask),
        "wildcard": str(net.hostmask),
        "first_host": str(first),
        "last_host": str(last),
        "total_addresses": total,
        "usable_hosts": usable,
    }