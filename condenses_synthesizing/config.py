from pydantic_settings import BaseSettings


class SynthesizingConfig(BaseSettings):
    min_tokens: int = 128
    max_tokens: int = 8192

class ServerConfig(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 9104


class Config(BaseSettings):
    synthesizing: SynthesizingConfig = SynthesizingConfig()
    server: ServerConfig = ServerConfig()

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


CONFIG = Config()
