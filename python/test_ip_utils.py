import pytest
from ip_utils import is_private_ip


def test_private_ips():
    assert is_private_ip("192.168.1.1") is True
    assert is_private_ip("10.0.0.1") is True
    assert is_private_ip("172.16.0.1") is True


def test_public_ips():
    assert is_private_ip("8.8.8.8") is False
    assert is_private_ip("1.1.1.1") is False


def test_invalid_ip():
    with pytest.raises(ValueError):
        is_private_ip("999.999.999.999")

