"""
This module contains tests for the fawlty.sensu_server module
"""

from fawlty.sensu_server import SensuServer

def test_sensu_server_default_values():
    server = SensuServer(host="localhost")
    assert server.host == "localhost"
    assert server.port == 8080
    assert not server.use_ssl
    assert not server.ignore_cert
    assert server.api_url == "http://localhost:8080"

def test_sensu_server_custom_values():
    server = SensuServer(host="example.com", port=443, use_ssl=True, ignore_cert=True)
    assert server.host == "example.com"
    assert server.port == 443
    assert server.use_ssl
    assert server.ignore_cert
    assert server.api_url == "https://example.com:443"