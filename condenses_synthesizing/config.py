from pydantic_settings import BaseSettings


class SynthesizingConfig(BaseSettings):
    min_tokens: int = 128
    max_tokens: int = 8192


class ServerConfig(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 9105


class Config(BaseSettings):
    synthesizing: SynthesizingConfig = SynthesizingConfig(extra="ignore")
    server: ServerConfig = ServerConfig(extra="ignore")

    class Config:
        env_file = ".synthesizing.env"
        env_nested_delimiter = "__"
        extra = "ignore"

CONFIG = Config()
