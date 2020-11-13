import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize("name", ["git", "ssl-cert"])
def test_packages(host, name):
    p = host.package(name)
    assert p.is_installed


@pytest.mark.parametrize(
    "path",
    [
        "/etc/letsencrypt/hooks/deploy",
        "/etc/letsencrypt/hooks/post",
        "/etc/letsencrypt/hooks/pre",
        "/etc/ssl/certs/ssl-cert-snakeoil.pem",
        "/etc/ssl/private/ssl-cert-snakeoil-combined.pem",
        "/etc/ssl/private/ssl-cert-snakeoil.key",
        "/opt/certbot/certbot-auto",
        "/etc/letsencrypt/cli.ini",
    ],
)
def test_files(host, path):
    f = host.file(path)
    assert f.exists
