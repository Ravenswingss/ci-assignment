#!/usr/bin/env python3
"""
ip_utils.py

Utility functions for IP address analysis.
"""

import ipaddress


def is_private_ip(ip_address: str) -> bool:
    """
    Check if an IP address is in a private range (RFC 1918).

    Args:
        ip_address (str): IPv4 or IPv6 address

    Returns:
        bool: True if private, False otherwise
    """
    try:
        ip = ipaddress.ip_address(ip_address)
        return ip.is_private
    except ValueError:
        raise ValueError(f"Invalid IP address: {ip_address}")


def main():
    # Simple manual test
    test_ips = [
        "192.168.1.10",
        "10.0.0.5",
        "8.8.8.8",
        "256.1.1.1"
    ]

    for ip in test_ips:
        try:
            print(f"{ip:15} -> private={is_private_ip(ip)}")
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()

