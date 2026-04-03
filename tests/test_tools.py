import pytest
from polish.openclaw.tools.system_tools import run_shell, disk_clean, restart_service
from polish.openclaw.tools.docker_tools import docker_ps, restart_container

def test_run_shell_allowed_command():
    result = run_shell("echo hello", capture_output=True)
    assert result["status"] == "success"
    assert "hello" in result.get("stdout", "")

def test_run_shell_not_allowed():
    result = run_shell("rm -rf /", capture_output=False)
    assert result["status"] == "error"
    assert "not allowed" in result["error"]

def test_disk_clean_dry_run():
    result = disk_clean(limit_mb=500)
    assert result["status"] == "success"
    assert "dry-run" in result["note"].lower()

def test_docker_ps():
    result = docker_ps()
    assert "status" in result
    if result["status"] == "success":
        assert "containers" in result

def test_restart_container_no_docker():
    result = restart_container("nonexistent")
    assert result["status"] == "error"

def test_restart_service_not_whitelisted():
    result = restart_service("nginx")
    assert result["status"] == "error"
    assert "not in whitelist" in result["error"]
