import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize("name", ["git"])
def test_packages(host, name):
    p = host.package(name)
    assert p.is_installed


@pytest.mark.parametrize(
    "path",
    [
        "/etc/letsencrypt/renewal-hooks/pre",
        "/etc/letsencrypt/renewal-hooks/post",
        "/etc/letsencrypt/renewal-hooks/deploy",
        "/opt/certbot/certbot-auto",
    ],
)
def test_files(host, path):
    f = host.file(path)
    assert f.exists
