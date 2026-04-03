import os
import tempfile
from polish.openclaw.config.settings import Settings, PermissionsConfig

def test_settings_defaults(monkeypatch):
    monkeypatch.delenv("OPENCLAW_PORT", raising=False)
    monkeypatch.delenv("OPENCLAW_DATABASE_URL", raising=False)
    settings = Settings()
    assert settings.gateway.port == 8080
    assert settings.database.url.startswith("sqlite")
    assert settings.logging.level == "INFO"

def test_settings_from_env(monkeypatch):
    monkeypatch.setenv("OPENCLAW_PORT", "9999")
    monkeypatch.setenv("OPENCLAW_DATABASE_URL", "postgresql://...")
    settings = Settings()
    assert settings.gateway.port == 9999
    assert settings.database.url == "postgresql://..."

def test_permissions_config_path(monkeypatch, tmp_path):
    perms_file = tmp_path / "perms.yaml"
    perms_file.write_text("tools: {}")
    monkeypatch.setenv("OPENCLAW_PERMISSIONS", str(perms_file))
    cfg = PermissionsConfig()
    assert cfg.path == str(perms_file)
