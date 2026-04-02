"""Load OpenClaw settings from environment and YAML."""
import os
from dataclasses import dataclass, field

@dataclass
class DatabaseConfig:
    url: str = field(default_factory=lambda: os.getenv("OPENCLAW_DATABASE_URL", "sqlite:///openclaw.db"))

@dataclass
class PermissionsConfig:
    path: str = field(default_factory=lambda: os.getenv("OPENCLAW_PERMISSIONS", "polish/openclaw/config/permissions.yaml"))

@dataclass
class LoggingConfig:
    level: str = field(default_factory=lambda: os.getenv("OPENCLAW_LOG_LEVEL", "INFO"))
    format: str = field(default_factory=lambda: os.getenv("OPENCLAW_LOG_FORMAT", "json"))
    dir: str = field(default_factory=lambda: os.getenv("OPENCLAW_LOG_DIR", "logs"))

@dataclass
class GatewayConfig:
    port: int = field(default_factory=lambda: int(os.getenv("OPENCLAW_PORT", "8080")))
    cors_origins: list = None
    rate_limit_per_minute: int = field(default_factory=lambda: int(os.getenv("OPENCLAW_RATE_LIMIT", "60")))
    secret: str = field(default_factory=lambda: os.getenv("OPENCLAW_SECRET", "change-me"))

    def __post_init__(self):
        if self.cors_origins is None:
            self.cors_origins = ["*"]

@dataclass
class Settings:
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    permissions: PermissionsConfig = field(default_factory=PermissionsConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    gateway: GatewayConfig = field(default_factory=GatewayConfig)
    ENV: str = field(default_factory=lambda: os.getenv("OPENCLAW_ENV", "production"))

settings = Settings()
