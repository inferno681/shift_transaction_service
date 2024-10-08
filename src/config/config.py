from pathlib import Path

import yaml
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class _SettingsModel(BaseSettings):
    """Base settings."""

    @classmethod
    def from_yaml(cls, config_path: str) -> '_SettingsModel':
        return cls(
            **yaml.safe_load(Path(config_path).read_text(encoding='utf-8')),
        )

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix='EMP_',
        env_nested_delimiter='__',
    )

    @classmethod
    def customise_sources(
        cls,
        init_settings,
        env_settings,
        file_secret_settings,
    ):
        """Variables priority."""
        return init_settings, env_settings, file_secret_settings


class _ServiceSettings(_SettingsModel):
    """Service settings validation."""

    title: str
    description: str
    host: str
    port: int
    debug: bool
    db_hostname: str
    db_port: int
    db_name: str
    db_username: str
    db_echo: bool
    tags_metadata_transaction: dict[str, str]
    tags_metadata_health: dict[str, str]


class _SettingsSecret(BaseSettings):
    """Secret settings validation."""

    db_password: SecretStr = SecretStr('password')

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )


class _JaegerSettings(_SettingsModel):
    """Jaeger settings validation."""

    service_name: str
    host: str
    port: int
    logging: bool
    sampler_type: str
    sampler_param: float | int


class _RedisSettings(_SettingsModel):
    """Redis settings validation."""

    url: str
    db: int
    decode_responses: bool


class Settings(_SettingsModel, _SettingsSecret):
    """Service settings."""

    service: _ServiceSettings
    jaeger: _JaegerSettings
    redis: _RedisSettings

    @property
    def database_url(self):
        """Database async link."""
        return (
            f'postgresql+asyncpg://{self.service.db_username}:'
            f'{self.db_password.get_secret_value()}@'
            f'{self.service.db_hostname}:'
            f'{self.service.db_port}/{self.service.db_name}'
        )

    @property
    def sync_database_url(self):
        """Database async link."""
        return (
            f'postgresql://{self.service.db_username}:'
            f'{self.db_password.get_secret_value()}@'
            f'{self.service.db_hostname}:'
            f'{self.service.db_port}/{self.service.db_name}'
        )


config = Settings.from_yaml('./src/config/config.yaml')
