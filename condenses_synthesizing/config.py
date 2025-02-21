from pydantic_settings import BaseSettings
from pydantic import Extra


class SynthesizingConfig(BaseSettings):
    min_tokens: int = 128
    max_tokens: int = 8192

    model_config = {
        "extra": "ignore"  # Allow extra fields
    }


class ServerConfig(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 9105

    model_config = {
        "extra": "ignore"  # Allow extra fields
    }


class Config(BaseSettings):
    synthesizing: SynthesizingConfig = SynthesizingConfig()
    server: ServerConfig = ServerConfig()

    model_config = {
        "env_file": ".synthesizing.env",
        "env_nested_delimiter": "__",
        "extra": "ignore",  # Allow extra fields globally
    }


CONFIG = Config()
