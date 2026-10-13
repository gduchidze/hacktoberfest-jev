"""Single source of config: ``config.toml`` (overridable via ``ROUTER_*`` env vars)."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

CONFIG_FILE = Path(__file__).with_name("config.toml")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        toml_file=CONFIG_FILE,
        env_prefix="ROUTER_",
        frozen=True,
    )

    log_level: str = "INFO"

    human_threshold: float = Field(default=0.8, ge=0, le=1)
    abstain_below: float = Field(default=0.3, ge=0, le=1)
    frontier_from: float = Field(default=1.0, ge=0)

    small_model: str = "small-llm"
    frontier_model: str = "frontier-llm"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # Priority: explicit kwargs > env vars > config.toml > field defaults.
        return (init_settings, env_settings, TomlConfigSettingsSource(settings_cls))


settings = Settings()
