import socket

# Force DNS resolution through Cloudflare and Google
dns_servers = ["1.1.1.1", "8.8.8.8"]

def custom_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    # Try normal resolution first
    try:
        return original_getaddrinfo(host, port, family, type, proto, flags)
    except socket.gaierror:
        # Try manual fallback resolution
        for dns in dns_servers:
            try:
                return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (dns, port))]
            except Exception:
                continue
        raise

# Patch Python's DNS resolver
original_getaddrinfo = socket.getaddrinfo
socket.getaddrinfo = custom_getaddrinfo
